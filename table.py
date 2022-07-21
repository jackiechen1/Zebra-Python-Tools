from parse import *
import numpy as np
from numpy import mod

colorMap = {
    0: "#C5c5c5",  # Background
    1: "#F73f3a",  # Source1
    2: "#73f550",  # Source2
    3: "#50e1f5",  # Destination
    4: "12",  # S1 S2 conflict
    5: "13",  # S1 D1 conflict
    6: "23",  # S2 D1 conflict
}


# Debug purpose only, used to print table
def PrinTable(table, tableReg, bits):
    start, end, rest = tableReg
    for i in range(bits):
        if i >= 10:
            print(int(i), end=" ")
        else:
            print(i, end="  ")
    print('\n')
    M, N = table.shape
    for i in range(M):
        for j in range(N):
            print(int(table[i, j]), end="  ")
        print("r" + str(start + i))
        print('\n')
    print('\n')


# Assign the tabel array based on assembly rules
# s: offset,
# v: vertical stride,
# w: width,
# h: height,
# t: datasize(unit in bytes),
# bits: 32 or 64,
# row: assigning row index in table,
# SourceOrDestination: 1->source1, 2->source2, 3->destination
def AssignArray(ExecSize, s, v, w, h, t, table, bits, row, SourceOrDestination):
    # Assign Array value based on Gen assembly rules
    for i in range(ExecSize):
        if SourceOrDestination <= 2:  # Source case
            position = int((s + (i // w) * v + mod(i, w) * h) * t)
        else:
            position = (s + i * h) * t
        rowPos = position // bits  # Index of rows
        startPos = position % bits

        right_index = bits - startPos
        left_index = right_index - t
        temp_table = table[row + rowPos, left_index:right_index]
        if SourceOrDestination == 1:  # Source1 case
            temp_table = np.where(temp_table == colorMap[0], colorMap[SourceOrDestination],temp_table)
            if colorMap[SourceOrDestination] not in temp_table:
                temp_table = np.where(temp_table == colorMap[1], colorMap[SourceOrDestination],temp_table)
            if colorMap[SourceOrDestination] not in temp_table:
                temp_table = np.where(temp_table == colorMap[2],
                                      colorMap[4], colorMap[6])
        elif SourceOrDestination == 2:  # Source2 case
            temp_table = np.where(temp_table == colorMap[0], colorMap[SourceOrDestination],temp_table)
            if colorMap[SourceOrDestination] not in temp_table:
                temp_table = np.where(temp_table == colorMap[2], colorMap[SourceOrDestination], temp_table)
            if colorMap[SourceOrDestination] not in temp_table:
                temp_table = np.where(temp_table == colorMap[1],
                                      colorMap[4], colorMap[6])
        else: # Destination case
            temp_table = np.where(temp_table == colorMap[0], colorMap[SourceOrDestination],temp_table)
            if colorMap[SourceOrDestination] not in temp_table:
                temp_table = np.where(temp_table == colorMap[3], colorMap[SourceOrDestination], temp_table)
            if colorMap[SourceOrDestination] not in temp_table:
                temp_table = np.where(temp_table == colorMap[1],
                                      colorMap[5], colorMap[6])
        table[row + rowPos, left_index:right_index] = temp_table
    return table


# Update the table based on type, just a helper
def UpdateTable(obj, regionType, table, row, bits):
    if regionType == 1:  # Source1
        if obj.source1.constant:
            return table
        update = AssignArray(obj.execinfo.ExecSize, obj.source1.offset, obj.source1.V, obj.source1.W, obj.source1.H,
                             obj.source1.datatype, table, bits, row, 1)
    elif regionType == 2:  # Source2
        if obj.source2.constant:
            return table
        update = AssignArray(obj.execinfo.ExecSize, obj.source1.offset, obj.source1.V, obj.source1.W, obj.source1.H,
                             obj.source1.datatype, table, bits, row, 2)
    else:  # destination
        update = AssignArray(obj.execinfo.ExecSize, obj.destination.offset, 0, 0, obj.destination.H,
                             obj.destination.datatype, table, bits, row, 3)
    return update


# Sort the table list so that the table array will order from small registers to large registers
def sortTable(tableArray, tableTuple):
    def simpleSwap(swapList, pos1, pos2, reg):
        get = swapList[pos1], swapList[pos2]
        swapList[pos2], swapList[pos1] = get
        if reg:  # keep the regeister table index
            reg1 = swapList[pos2][2]
            swapList[pos2][2] = swapList[pos1][2]
            swapList[pos1][2] = reg1

    i = 0
    while i < len(tableArray):
        # One giant table
        if not tableTuple[i][2]:
            i += 1

        # Two tables
        elif tableTuple[i][2] == 1:
            order = np.array([tableTuple[i][0], tableTuple[i + 1][0]])
            ArgMin = np.argmin(order)
            if ArgMin:
                simpleSwap(tableArray, i, i + 1, False)
                simpleSwap(tableTuple, i, i + 1, True)
            i += 2

        # Three table
        else:
            order = np.array([tableTuple[i][0], tableTuple[i + 1][0], tableTuple[i + 2][0]])
            ArgMin = np.argmin(order)
            if ArgMin != 0:
                simpleSwap(tableArray, i, i + ArgMin, False)
                simpleSwap(tableTuple, i, i + ArgMin, True)
                order = np.array([tableTuple[i + 1][0], tableTuple[i + 2][0]])
                ArgMin = np.argmin(order)
                if ArgMin:
                    simpleSwap(tableArray, i + 1, i + 2, False)
                    simpleSwap(tableTuple, i + 1, i + 2, True)
            i += 3


# Main Table class, take one GenAssembly object and generate numpy array table chart
class TableChart:
    element_size = 4  # unit in bytes
    bits = 32
    square_width = 25  # if 64 width = 12.5
    square_height = 25
    tableNpArray = []  # contain the numpy array list
    tableRegNumber = []  # contain a list of tuple of start reg, end index reg, # of table remain
    genAssemblyObj = GenAssembly()
    numberOfSource = 1

    def __init__(self):
        self.genAssemblyObj = GenAssembly()

    # Assign a new GenAssembly object to generate table
    def AssignNewObj(self, genObj, bits):
        global numberOfBits
        numberOfBits = bits
        self.tableNpArray = []
        self.tableRegNumber = []
        self.numberOfSource = 1
        self.bits = bits
        if self.bits == 64:
            self.square_width = 12.5
        else:
            self.square_width = 25
        self.genAssemblyObj = genObj

        self.element_size = max(genObj.source1.datatype, genObj.source2.datatype,
                                genObj.destination.datatype)
        if not genObj.source2.constant and genObj.source2.datatype!=-1:
            self.numberOfSource = 2
        '''
        # Two Source case
        if genObj.mnemonic in MnemonicList2:
            self.element_size = max(genObj.source1.datatype, genObj.source2.datatype,
                                    genObj.destination.datatype)
            
            self.numberOfSource = 2

        # One Source case
        else:
            self.element_size = max(genObj.source1.datatype, genObj.destination.datatype)
        '''
        # Prevent any other cases
        if self.element_size <= 0:
            self.element_size = 1

        self.GenerateArray()
        sortTable(self.tableNpArray, self.tableRegNumber)

    # Generate numpy array based on the rules
    def GenerateArray(self):
        # At most Two region case
        if self.numberOfSource == 1:
            difference = abs(self.genAssemblyObj.source1.reg - self.genAssemblyObj.destination.reg)
            if self.genAssemblyObj.source1.constant:
                difference = 0
            if difference <= 5:  # close enough so only generate one table
                GeneratedTable = np.full((difference + 4, self.bits), colorMap[0])
                StartIndex = min(self.genAssemblyObj.source1.reg, self.genAssemblyObj.destination.reg) - 1

                if self.genAssemblyObj.source1.reg < self.genAssemblyObj.destination.reg:
                    # Source region goes first
                    sourceRow = 1
                    destinationRow = sourceRow + difference
                else:
                    destinationRow = 1
                    sourceRow = destinationRow + difference

                GeneratedTable = UpdateTable(self.genAssemblyObj, 1, GeneratedTable, sourceRow, self.bits)
                GeneratedTable = UpdateTable(self.genAssemblyObj, 3, GeneratedTable, destinationRow, self.bits)

                self.tableNpArray.append(GeneratedTable)
                self.tableRegNumber.append([StartIndex, StartIndex + difference + 2, 0])

            else:  # Two regions
                Table1 = np.full((4, self.bits), colorMap[0])
                Table2 = np.full((4, self.bits), colorMap[0])

                Table1 = UpdateTable(self.genAssemblyObj, 1, Table1, 1, self.bits)
                Table2 = UpdateTable(self.genAssemblyObj, 3, Table2, 1, self.bits)

                self.tableNpArray.append(Table1)
                self.tableNpArray.append(Table2)
                self.tableRegNumber.append([self.genAssemblyObj.source1.reg - 1,
                                            self.genAssemblyObj.source1.reg + 4, 1])
                # Start index leave one more extra row before the first row
                self.tableRegNumber.append(
                    [self.genAssemblyObj.destination.reg - 1, self.genAssemblyObj.destination.reg + 4, 0])

        # At most three tables case
        else:
            differenceS1S2 = abs(self.genAssemblyObj.source1.reg - self.genAssemblyObj.source2.reg)
            differenceS1D1 = abs(self.genAssemblyObj.source1.reg - self.genAssemblyObj.destination.reg)
            differenceS2D1 = abs(self.genAssemblyObj.destination.reg - self.genAssemblyObj.source2.reg)
            if self.genAssemblyObj.source1.constant:
                differenceS1S2 = 0
                differenceS1D1 = 0
            elif self.genAssemblyObj.source2.constant:
                differenceS1S2 = 0
                differenceS2D1 = 0
            if differenceS2D1 + differenceS1D1 <= 10 or differenceS1S2 + differenceS1D1 <= 10 or differenceS1S2 + differenceS2D1 <= 10:
                # One huge table
                startIndex = min(self.genAssemblyObj.source1.reg, self.genAssemblyObj.source2.reg,
                                 self.genAssemblyObj.destination.reg) - 1
                MaxDiff = max(self.genAssemblyObj.source1.reg, self.genAssemblyObj.source2.reg,
                              self.genAssemblyObj.destination.reg) - startIndex
                # Fulfill the numpy array by the color map value
                GeneratedTable = np.full((MaxDiff + 4, self.bits), colorMap[0])
                GeneratedTable = UpdateTable(self.genAssemblyObj, 3, GeneratedTable,
                                             self.genAssemblyObj.destination.reg - startIndex, self.bits)
                GeneratedTable = UpdateTable(self.genAssemblyObj, 1, GeneratedTable,
                                             self.genAssemblyObj.source1.reg - startIndex, self.bits)
                GeneratedTable = UpdateTable(self.genAssemblyObj, 2, GeneratedTable,
                                             self.genAssemblyObj.source2.reg - startIndex, self.bits)
                self.tableNpArray.append(GeneratedTable)
                self.tableRegNumber.append([startIndex, startIndex + MaxDiff + 3, 0])
            elif differenceS1S2 <= 5 or differenceS2D1 <= 5 or differenceS1D1 <= 5:
                # Two tables, one contains two regions, the other contains one region
                MinDiff = min(differenceS1S2, differenceS2D1, differenceS1D1)
                Table1 = np.full((MinDiff + 4, self.bits), colorMap[0])
                Table2 = np.full((4, self.bits), colorMap[0])

                if differenceS1S2 <= 5:
                    MinIndex = min(self.genAssemblyObj.source1.reg, self.genAssemblyObj.source2.reg)
                    Table1 = UpdateTable(self.genAssemblyObj, 1, Table1,
                                         self.genAssemblyObj.source1.reg - MinIndex + 1, self.bits)
                    Table1 = UpdateTable(self.genAssemblyObj, 2, Table1,
                                         self.genAssemblyObj.source2.reg - MinIndex + 1, self.bits)
                    self.tableRegNumber.append([MinIndex - 1, MinIndex + differenceS1S2, 1])

                    Table2 = UpdateTable(self.genAssemblyObj, 3, Table2,
                                         1, self.bits)
                    self.tableRegNumber.append(
                        [self.genAssemblyObj.destination.reg - 1, self.genAssemblyObj.destination.reg + 3, 0])

                elif differenceS1D1 <= 5:
                    MinIndex = min(self.genAssemblyObj.source1.reg, self.genAssemblyObj.destination.reg)
                    Table1 = UpdateTable(self.genAssemblyObj, 1, Table1,
                                         self.genAssemblyObj.source1.reg - MinIndex + 1, self.bits)
                    Table1 = UpdateTable(self.genAssemblyObj, 3, Table1,
                                         self.genAssemblyObj.destination.reg - MinIndex + 1, self.bits)
                    self.tableRegNumber.append([MinIndex - 1, MinIndex + differenceS1D1, 1])

                    Table2 = UpdateTable(self.genAssemblyObj, 2, Table2,
                                         1, self.bits)
                    self.tableRegNumber.append(
                        [self.genAssemblyObj.source2.reg - 1, self.genAssemblyObj.source2.reg + 3, 0])
                else:
                    MinIndex = min(self.genAssemblyObj.source2.reg, self.genAssemblyObj.destination.reg)
                    Table1 = UpdateTable(self.genAssemblyObj, 2, Table1,
                                         self.genAssemblyObj.source2.reg - MinIndex + 1, self.bits)
                    Table1 = UpdateTable(self.genAssemblyObj, 3, Table1,
                                         self.genAssemblyObj.destination.reg - MinIndex + 1, self.bits)
                    self.tableRegNumber.append([MinIndex - 1, MinIndex + differenceS2D1, 1])

                    Table2 = UpdateTable(self.genAssemblyObj, 1, Table2,
                                         1, self.bits)
                    self.tableRegNumber.append(
                        [self.genAssemblyObj.source1.reg - 1, self.genAssemblyObj.source1.reg + 3, 0])
                self.tableNpArray.append(Table1)
                self.tableNpArray.append(Table2)
            else:
                # Three separate tables
                Table1 = np.full((4, self.bits), colorMap[0])
                Table2 = np.full((4, self.bits), colorMap[0])
                Table3 = np.full((4, self.bits), colorMap[0])

                Table1 = UpdateTable(self.genAssemblyObj, 1, Table1,
                                     1, self.bits)
                Table2 = UpdateTable(self.genAssemblyObj, 2, Table2,
                                     1, self.bits)
                Table3 = UpdateTable(self.genAssemblyObj, 3, Table3,
                                     1, self.bits)

                self.tableNpArray.append(Table1)
                self.tableNpArray.append(Table2)
                self.tableNpArray.append(Table3)

                self.tableRegNumber.append(
                    [self.genAssemblyObj.source1.reg - 1, self.genAssemblyObj.source1.reg + 4, 2])
                self.tableRegNumber.append(
                    [self.genAssemblyObj.source2.reg - 1, self.genAssemblyObj.source2.reg + 4, 1])
                self.tableRegNumber.append(
                    [self.genAssemblyObj.destination.reg - 1, self.genAssemblyObj.destination.reg + 4, 0])
