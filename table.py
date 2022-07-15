from parse import *
import numpy as np
from numpy import mod

colorMap = {
    0: "#C5c5c5", # Background
    1: "#F73f3a", # Source1
    2: "#73f550", # Source2
    3: "#50e1f5", # Destination
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


# Assign the tabel array based on assembly rules s: offset, v: vertical stride, w: width, h: height, t: datasize(unit
# in bytes), bits: 32 or 64, row: assigning row in table, Source: True for source and false for destination
def AssignArray(ExecSize, s, v, w, h, t, table, bits, row, SourceOrDestination):
    # Assign Array value based on Gen assembly rules
    for i in range(ExecSize):
        if SourceOrDestination<=2:  # True for Source, False for Destination
            position = int((s + (i // w) * v + mod(i, w) * h) * t)
        else:
            position = (s + i * h) * t
        # print(position)
        if position >= bits:
            position -= bits  # second row
            right_index = bits - position
            left_index = right_index - t
            table[row + 1, left_index:right_index] = colorMap[SourceOrDestination]
        else:
            right_index = bits - position
            left_index = right_index - t
            table[row, left_index:right_index] = colorMap[SourceOrDestination]
    return table


# Update the table based on type, just a helper
def UpdateTable(obj, regionType, table, row, bits):
    if regionType == 1:  # Source1
        update = AssignArray(obj.execinfo.ExecSize, obj.source1.offset, obj.source1.V, obj.source1.W, obj.source1.H,
                             obj.source1.datatype, table, bits, row, 1)
    elif regionType == 2:  # Source2
        update = AssignArray(obj.execinfo.ExecSize, obj.source1.offset, obj.source1.V, obj.source1.W, obj.source1.H,
                             obj.source1.datatype, table, bits, row, 2)
    else:  # destination
        update = AssignArray(obj.execinfo.ExecSize, obj.destination.offset, 0, 0, obj.destination.H,
                             obj.destination.datatype, table, bits, row, 3)
    return update


# Sort the table list so that the table array will order from small registers to large registers
def sortTable(tableArray, tableTuple):
    def simpleSwap(swapList, pos1, pos2):
        get = swapList[pos1], swapList[pos2]
        swapList[pos2], swapList[pos1] = get

    i = 0
    while i < len(tableArray):
        if not tableTuple[i][2]:  # One giant table
            i += 1
        elif tableTuple[i][2] == 1:  # Two tables
            order = np.array([tableTuple[i][0], tableTuple[i + 1][0]])
            ArgMin = np.argmin(order)
            if ArgMin:
                simpleSwap(tableArray, i, i + 1)
                simpleSwap(tableTuple, i, i + 1)
            i += 2
        else:  # Three table
            order = np.array([tableTuple[i][0], tableTuple[i + 1][0], tableTuple[i + 2][0]])
            ArgMin = np.argmin(order)
            if ArgMin != 0:
                simpleSwap(tableArray, i, i + ArgMin)
                simpleSwap(tableTuple, i, i + ArgMin)
                order = np.array([tableTuple[i + 1][0], tableTuple[i + 2][0]])
                ArgMin = np.argmin(order)
                if ArgMin:
                    simpleSwap(tableArray, i + 1, i + 2)
                    simpleSwap(tableTuple, i + 1, i + 2)
            i += 3


# Main Table class, take one GenAssembly object and generate numpy array table chart
class TableChart:
    element_size = 4  # unit in bytes
    bits = 32
    square_width = 25  # if 64 width =15
    square_height = 25
    tableNpArray = []  # contain the numpy array list
    tableRegNumber = []  # contain a list of tuple of start reg, end index reg, # of table remain
    genAssemblyObj = GenAssembly()
    numberOfSource = 1

    def __init__(self):
        self.genAssemblyObj = GenAssembly()
    def AssignNewObj(self, genObj):
        self.tableNpArray = []
        self.tableRegNumber = []
        self.numberOfSource = 1
        self.bits = numberOfBits
        if self.bits == 64:
            self.square_width = 15
        self.genAssemblyObj = genObj

        if genObj.source2.datatype != -1:
            self.element_size = min(genObj.source1.datatype, genObj.source2.datatype,
                                    genObj.destination.datatype)
            self.numberOfSource = 2
        else:
            self.element_size = min(genObj.source1.datatype, genObj.destination.datatype)
        self.GenerateArray()
        sortTable(self.tableNpArray, self.tableRegNumber)

    def GenerateArray(self):
        if self.numberOfSource == 1:  # At most Two region case
            difference = abs(self.genAssemblyObj.source1.reg - self.genAssemblyObj.destination.reg)
            if difference <= 5:  # close enough so only generate one table
                GeneratedTable = np.full((difference + 4, self.bits),colorMap[0])
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
                self.tableRegNumber.append((StartIndex, StartIndex + difference + 2, 0))

            else:  # Two regions
                Table1 = np.full((4, self.bits),colorMap[0])
                Table2 = np.full((4, self.bits),colorMap[0])

                Table1 = AssignArray(self.genAssemblyObj.execinfo.ExecSize, self.genAssemblyObj.source1.offset,
                                     self.genAssemblyObj.source1.V, self.genAssemblyObj.source1.W,
                                     self.genAssemblyObj.source1.H,
                                     self.element_size, Table1, self.bits, 1, True)
                Table2 = AssignArray(self.genAssemblyObj.execinfo.ExecSize, self.genAssemblyObj.destination.offset,
                                     0, 0, self.genAssemblyObj.destination.H,
                                     self.element_size, Table2, self.bits, 1, False)

                self.tableNpArray.append(Table1)
                self.tableNpArray.append(Table2)
                self.tableRegNumber.append((self.genAssemblyObj.source1.reg - 1,
                                            self.genAssemblyObj.source1.reg + 4, 1))
                # Start index leave one more extra row before
                self.tableRegNumber.append(
                    (self.genAssemblyObj.destination.reg - 1, self.genAssemblyObj.destination.reg + 4, 0))
        else:  # Three tables case
            differenceS1S2 = abs(self.genAssemblyObj.source1.reg - self.genAssemblyObj.source2.reg)
            differenceS1D1 = abs(self.genAssemblyObj.source1.reg - self.genAssemblyObj.destination.reg)
            differenceS2D1 = abs(self.genAssemblyObj.destination.reg - self.genAssemblyObj.source2.reg)
            if differenceS2D1 + differenceS1D1 <= 10 or differenceS1S2 + differenceS1D1 <= 10 or differenceS1S2 + differenceS2D1 <= 10:
                # One huge table
                startIndex = min(self.genAssemblyObj.source1.reg, self.genAssemblyObj.source2.reg,
                                 self.genAssemblyObj.destination.reg) - 1
                MaxDiff = max(self.genAssemblyObj.source1.reg, self.genAssemblyObj.source2.reg,
                              self.genAssemblyObj.destination.reg) - startIndex
                GeneratedTable = np.full((MaxDiff + 4, self.bits),colorMap[0])
                GeneratedTable = UpdateTable(self.genAssemblyObj, 3, GeneratedTable,
                                             self.genAssemblyObj.destination.reg - startIndex, self.bits)
                GeneratedTable = UpdateTable(self.genAssemblyObj, 1, GeneratedTable,
                                             self.genAssemblyObj.source1.reg - startIndex, self.bits)
                GeneratedTable = UpdateTable(self.genAssemblyObj, 2, GeneratedTable,
                                             self.genAssemblyObj.source2.reg - startIndex, self.bits)
                self.tableNpArray.append(GeneratedTable)
                self.tableRegNumber.append((startIndex, startIndex + MaxDiff + 3, 0))
            elif differenceS1S2 <= 5 or differenceS2D1 <= 5 or differenceS1D1 <= 5:
                # Two tables, one contains two regions, the other contains one region
                MinDiff = min(differenceS1S2, differenceS2D1, differenceS1D1)
                Table1 = np.full((MinDiff + 4, self.bits),colorMap[0])
                Table2 = np.full((4, self.bits),colorMap[0])

                if differenceS1S2 <= 5:
                    MinIndex = min(self.genAssemblyObj.source1.reg, self.genAssemblyObj.source2.reg)
                    Table1 = UpdateTable(self.genAssemblyObj, 1, Table1,
                                         self.genAssemblyObj.source1.reg - MinIndex + 1, self.bits)
                    Table1 = UpdateTable(self.genAssemblyObj, 2, Table1,
                                         self.genAssemblyObj.source2.reg - MinIndex + 1, self.bits)
                    self.tableRegNumber.append((MinIndex - 1, MinIndex + differenceS1S2, 1))

                    Table2 = UpdateTable(self.genAssemblyObj, 3, Table2,
                                         1, self.bits)
                    self.tableRegNumber.append(
                        (self.genAssemblyObj.destination.reg - 1, self.genAssemblyObj.destination.reg + 3, 0))

                elif differenceS1D1 <= 5:
                    MinIndex = min(self.genAssemblyObj.source1.reg, self.genAssemblyObj.destination.reg)
                    Table1 = UpdateTable(self.genAssemblyObj, 1, Table1,
                                         self.genAssemblyObj.source1.reg - MinIndex + 1, self.bits)
                    Table1 = UpdateTable(self.genAssemblyObj, 3, Table1,
                                         self.genAssemblyObj.destination.reg - MinIndex + 1, self.bits)
                    self.tableRegNumber.append((MinIndex - 1, MinIndex + differenceS1D1, 1))

                    Table2 = UpdateTable(self.genAssemblyObj, 2, Table2,
                                         1, self.bits)
                    self.tableRegNumber.append(
                        (self.genAssemblyObj.source2.reg - 1, self.genAssemblyObj.source2.reg + 3, 0))
                else:
                    MinIndex = min(self.genAssemblyObj.source2.reg, self.genAssemblyObj.destination.reg)
                    Table1 = UpdateTable(self.genAssemblyObj, 2, Table1,
                                         self.genAssemblyObj.source2.reg - MinIndex + 1, self.bits)
                    Table1 = UpdateTable(self.genAssemblyObj, 3, Table1,
                                         self.genAssemblyObj.destination.reg - MinIndex + 1, self.bits)
                    self.tableRegNumber.append((MinIndex - 1, MinIndex + differenceS2D1, 1))

                    Table2 = UpdateTable(self.genAssemblyObj, 1, Table2,
                                         1, self.bits)
                    self.tableRegNumber.append(
                        (self.genAssemblyObj.source1.reg - 1, self.genAssemblyObj.source1.reg + 3, 0))
                self.tableNpArray.append(Table1)
                self.tableNpArray.append(Table2)
            else:
                # Three separate tables
                Table1 = np.full((4, self.bits),colorMap[0])
                Table2 = np.full((4, self.bits),colorMap[0])
                Table3 = np.full((4, self.bits),colorMap[0])

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
                    (self.genAssemblyObj.source1.reg - 1, self.genAssemblyObj.source1.reg + 4, 2))
                self.tableRegNumber.append(
                    (self.genAssemblyObj.source2.reg - 1, self.genAssemblyObj.source2.reg + 4, 1))
                self.tableRegNumber.append(
                    (self.genAssemblyObj.destination.reg - 1, self.genAssemblyObj.destination.reg + 4, 0))
