
datatype_bits_conversion = {
    "b": 8,
    "ub": 8,
    "w": 16,
    "uw": 16,
    "d": 32,
    "ud": 32,
    "q": 64,
    "uq": 64,
    "hf": 16,
    "f": 32,
    "df": 64,
    "uv": -1,  # These three types are special type which needs to define seperately
    "v": -1,
    "vf": -1
}
immediateSourceOperands = {
    "-3.14159:f": 1,  # Immediate 32-bit float
    "-1234:d": 2,  # Immediate 32-bit integer
    "0x7654321:v": 3  # Packed integer vector
}
MnemonicList = ["add", "mov", "math.div"]
conditionValueList = ["ze", "eq", "nz", "ne", "gt", "ge", "lt", "le"]
numberOfBits = 32  # 32 bits or 64 bits

def ThrowGrammerError(line, error):
    message = "Unknow grammer sytax at " + line + "\n" + error
    ThrowErrorMessage(message)

def ThrowErrorMessage(message):
    print(message)
    return

class Source:
    # e.g. -r5.0<0;1,0>:f
    modifiers = ''  # Source modifiers could be -,~,abs and so on
    reg = 5  # reg number
    offset = 0  # aka S
    V = 1  # Vertical stride
    W = 1  # Width
    H = 0  # Horizontal stride
    datatype = -1  # units in bits


class Destination:
    # e.g. -r1.0<1>:f
    modifiers = ''  # Source modifiers could be -,~,abs,sat and so on
    reg = 1  # reg number
    offset = 0  # aka S
    H = 1  # Horizontal stride
    datatype = 32  # units in bits


class ExecInfo:
    # e.g. (8|M0)
    ExecSize = 8
    mask = 0  # Idle for now


class FlagModif:  # Or Condition modifiers
    # e.g. (lt)f0.0
    condition = ''  # Options: ze,eq,nz,ne,gt,ge,lt,le
    offset = 0


def parsePrediction(line, obj):  # Not require
    if line[0] != '[':
        return line
    rightBracket = line.find(']')
    if rightBracket==-1:
        ThrowGrammerError(line,"Can't recognize prediction pattern")
    obj.predAndMask = line[1:rightBracket]
    return line[rightBracket+1:]


def parseMnemonic(line, obj):
    bracket = line.find('(')
    if bracket==-1:
        ThrowGrammerError(line,"Can't find ExecutionMask")
    if line[0:bracket] in MnemonicList:
        obj.mnemonic = line[0:bracket]
        return line[bracket:]
    else:
        ThrowGrammerError(line, "Fail parsing Mnemonic operator")


def parseExecutionMask(line, obj):
    leftbracket = line.find('(')
    rightbracket = line.find(')')
    bar = line.find('|')
    try:
        obj.execinfo.ExecSize = int(line[leftbracket+1:bar])
        obj.execinfo.mask = int(line[bar+2:rightbracket])
        return line[rightbracket+1:]
    except:
        ThrowGrammerError(line, "Fail parsing ExecutionMask")


def parseFlagModifier(line, obj):  # Not require
    if line[0] != '[':
        return line
    leftbracket = line.find('(')
    rightbracket = line.find(']')
    try:
        conditionValue = line[leftbracket+1:leftbracket+3]

        if conditionValue not in conditionValueList:
            ThrowGrammerError(line, "Unknow condition value")

        obj.flag.condition = conditionValue
        obj.flag.offset = line[leftbracket+4:rightbracket]
        return line[rightbracket+1:]
    except:
        ThrowGrammerError(line,"Can't parse Flag Modifier")


def parseDestination(line, obj):
    regexStart = line.find('r')
    leftBracket = line.find('<')
    rightBracket = line.find('>')
    dotPos = line.find('.')
    colon = line.find(':')
    endIndex = -1
    if regexStart == -1 or leftBracket ==-1 or rightBracket ==-1 or dotPos ==-1 or colon ==-1:
        ThrowGrammerError(line,"Fail to recognize region pattern")
    if line[0] == '-' or line[0] == '(' or line[0] == '~':
        obj.destination.modifiers = line[0,regexStart]
    if line[regexStart+1] == '[':
        # TODO: Indirct Source Operands
        ThrowGrammerError(line,"Indirct Source Operands unsupported yet")
    else:
        try:
            obj.destination.reg = int(line[regexStart+1:dotPos])
            obj.destination.offset = int(line[dotPos+1:leftBracket])
            obj.destination.H = int(line[leftBracket+1:rightBracket])
            if line[colon+1:colon+2] in datatype_bits_conversion.keys(): # one char data type
                obj.destination.datatype = datatype_bits_conversion[line[colon+1:colon+2]]
                endIndex = colon + 1
            elif line[colon+1:colon+3] in datatype_bits_conversion.keys(): # two char data type
                obj.destination.datatype = datatype_bits_conversion[line[colon+1:colon+3]]
                endIndex = colon + 2
            else:
                ThrowGrammerError(line,"Can't recognize datatype")
        except:
            ThrowGrammerError(line, "Can't recognize register number")
    return line[endIndex+1:]


def parseSource(line, obj, order):  # Second source not require
    regexStart = line.find('r')
    leftBracket = line.find('<')
    rightBracket = line.find('>')
    semiconlon = line.find(';')
    dotPos = line.find('.')
    colon = line.find(':')
    comma = line.find(',')
    endIndex = -1
    if regexStart == -1 or leftBracket ==-1 or rightBracket ==-1 or dotPos ==-1 or colon ==-1 or semiconlon == -1 or comma == -1:
        if order==2:
            return line
        else:
            ThrowGrammerError(line,"Fail to recognize region pattern")
    if line[0] == '-' or line[0] == '(' or line[0] == '~':
        if order==1:
            obj.source1.modifiers = line[0:regexStart]
        else:
            obj.source2.modifiers = line[0: regexStart]
    if line[regexStart+1] == '[':
        # TODO: Indirct Source Operands
        ThrowGrammerError(line,"Indirct Source Operands unsupported yet")
    else:
        try:
            if order==1:
                obj.source1.reg = int(line[regexStart + 1: dotPos])
                obj.source1.offset = int(line[dotPos + 1: leftBracket])
                obj.source1.V = int(line[leftBracket+1: semiconlon])
                obj.source1.W = int(line[semiconlon+1: comma])
                obj.source1.H = int(line[comma+1: rightBracket])
                if line[colon + 1: colon + 2] in datatype_bits_conversion.keys():  # one char data type
                    obj.source1.datatype = datatype_bits_conversion[line[colon + 1: colon + 2]]
                    endIndex = colon + 1
                elif line[colon + 1: colon + 3] in datatype_bits_conversion.keys():  # two char data type
                    obj.source1.datatype = datatype_bits_conversion[line[colon + 1: colon + 3]]
                    endIndex = colon + 2
                else:
                    ThrowGrammerError(line, "Can't recognize datatype")
            else:
                obj.source2.reg = int(line[regexStart + 1: dotPos])
                obj.source2.offset = int(line[dotPos + 1: leftBracket])
                obj.source2.V = int(line[leftBracket + 1: semiconlon])
                obj.source2.W = int(line[semiconlon + 1: comma])
                obj.source2.H = int(line[comma + 1: rightBracket])
                if line[colon + 1: colon + 2] in datatype_bits_conversion.keys():  # one char data type
                    obj.source2.datatype = datatype_bits_conversion[line[colon + 1: colon + 2]]
                    endIndex = colon + 1
                elif line[colon + 1: colon + 3] in datatype_bits_conversion.keys():  # two char data type
                    obj.source2.datatype = datatype_bits_conversion[line[colon + 1: colon + 3]]
                    endIndex = colon + 2
                else:
                    ThrowGrammerError(line, "Can't recognize datatype")

        except:
            ThrowGrammerError(line, "Can't recognize register number")
    return line[endIndex + 1:]


def parseImmediateSourceOperands(line, obj):
    comment = line.find("//")
    if comment!=-1:
        line = line[0:comment]
    colon = line.find(':')

    # Don't have an immediate Source Operands
    if colon ==-1:
        return ""
    if line[0:colon+2] not in immediateSourceOperands.keys():
        obj.immediateSourceOperands = immediateSourceOperands[line[0:colon+2]]
    else:
        ThrowGrammerError(line,"Can't recognize immediate source operands")
    return ""


def parse_one_line(line):
    # remove space
    line = line.replace(" ", "")

    # skip comments
    if line[0] == '/' and line[1] == '/':
        return

    genAssemblyObj = GenAssembly()

    # parse line in order
    line = parsePrediction(line, genAssemblyObj)
    line = parseMnemonic(line, genAssemblyObj)
    line = parseExecutionMask(line, genAssemblyObj)
    line = parseFlagModifier(line, genAssemblyObj)
    line = parseDestination(line, genAssemblyObj)
    line = parseSource(line, genAssemblyObj, 1)
    line = parseSource(line, genAssemblyObj, 2)
    if line:
        parseImmediateSourceOperands(line, genAssemblyObj)


def parse_lines(lines):
    lines_list = lines.split('\n')
    for line in lines_list:
        parse_one_line(line)

class GenAssembly:
    source1 = Source()  # First source (defualt one for one source mnemonic)
    source2 = Source()  # Second source
    destination = Destination()
    immediateSourceOperands = 0  # defualt none
    predAndMask = ""
    mnemonic = "mov"
    execinfo = ExecInfo()
    flag = FlagModif()

    def CheckConstraint(self):
        n = max(self.source1.datatype, self.source2.datatype, self.destination.datatype)
        if self.execinfo.ExecSize * n > 64:
            ThrowErrorMessage(
                "Where n is the largest element size in bytes for any source or destination operand type, ExecSize * n must be <= 64. For PVC, RLT, MAR,ExecSize * n must be <= 128 ")
            return

        # When the Execution Data Type is wider than the destination data type, the destination must be aligned as required by the wider execution data type and specify a HorzStride equal to the ratio in sizes of the two data types. For example, a mov with a D source and B destination must use a 4-byte aligned destination and a Dst.HorzStride of 4.
        # ??? if ExecSize>destination.datatype and destination.H!=destination.datatype/source1.datatype # ratio?
        def CheckSourceRegion(W, H, V, datatype):
            # Region restrictions:
            if self.execinfo.ExecSize < W:
                ThrowErrorMessage("ExecSize must be greater than or equal to Width.")
            elif self.execinfo.ExecSize == W and H and V != W * H:
                ThrowErrorMessage(
                    "If ExecSize = Width and HorzStride != 0, VertStride must be set to Width * HorzStride.")
            elif W == 1 and H != 0:
                ThrowErrorMessage(
                    "If Width = 1, HorzStride must be 0 regardless of the values of ExecSize and VertStride.")
            elif self.execinfo.ExecSize == 1 and W == 1 and (V or H):
                ThrowErrorMessage("If ExecSize = Width = 1, both VertStride and HorzStride must be 0.")
            elif V == 0 and H == 0 and W != 1:
                ThrowErrorMessage(
                    "If VertStride = HorzStride = 0, Width must be 1 regardless of the value of ExecSize.")
            elif self.destination.H == 0:
                ThrowErrorMessage("Dst.HorzStride must not be 0.")
            elif ((self.execinfo.ExecSize / W) * V + self.execinfo.ExecSize % W * H) * datatype > numberOfBits * 2:
                ThrowErrorMessage(" Crossing more than 2 registers")

        # ??? VertStride must be used to cross GRF register boundaries. This rule implies that elements within a 'Width' cannot cross GRF boundaries.
        CheckSourceRegion(self.source1.W, self.source1.H, self.source1.V, self.source1.datatype)
        CheckSourceRegion(self.source2.W, self.source2.H, self.source2.V, self.source2.datatype)
    # Project specific



import numpy as np
class table:
    element_size = 4
    source1_color = "#D97E4A"
    source2_color = "#D97E4A"
    destination_color = "#D97E4A"
    default_color = "#D97E4A"
    bits = 32
    square_width = 30  # if 64 width =15
    square_height = 30
    table_array = []
    table_index = [] # start index of table1 (option: start of table 2, start of table 3)
    genAssemblyobj = GenAssembly()
    numberOfSource = 1
    def __int__(self,genAssemblyObj):
        self.bits = numberOfBits
        if self.bits ==64:
            self.square_width = 15
        self.genAssemblyObj = genAssemblyObj
        if genAssemblyObj.source2.datatype!=-1:
            self.element_size = min(genAssemblyObj.source1.datatype,genAssemblyObj.source2.datatype,genAssemblyObj.desniation.datatype)
            numerOfSource=2
        else:
            self.element_size = min(genAssemblyObj.source1.datatype,genAssemblyObj.desniation.datatype)
    def GenerateArray(self):
        if self.numberOfSource==1: #At most Two region case
            difference = abs(self.genAssemblyObj.source1.reg-self.genAssemblyobj.destination.reg)
            if  difference <=5: #close enough so only generate one numpy array
                GeneratedTable = np.zeros(difference+4,self.bits)
                StartIndex = min(self.genAssemblyObj.source1.reg-self.genAssemblyobj.destination.reg)-1
                self.table_array.append(GeneratedTable)
                self.table_index.append(StartIndex)

            else:
                Table1 = np.zeros(4,self.bits) # Maybe the last column put r11 ???
                Table2 = np.zeros(4,self.bits)
                self.table_array.append(Table1)
                self.table_array.append(Table2)
                self.table_index.append(min(self.genAssemblyObj.source1.reg-self.genAssemblyobj.destination.reg)-1)
                self.table_index.append(max(self.genAssemblyObj.source1.reg-self.genAssemblyobj.destination.reg)-1)
        else: # Three region case
            differenceS1S2 = abs(self.genAssemblyObj.source1.reg-self.genAssemblyobj.source2.reg)
            differenceS1D1 = abs(self.genAssemblyObj.source1.reg - self.genAssemblyobj.destination.reg)
            differenceS2D1 = abs(self.genAssemblyObj.source1.reg - self.genAssemblyobj.source2.reg)
            if differenceS2D1+differenceS1D1 <=10 or differenceS1S2+differenceS1D1<=10 or differenceS1S2+differenceS2D1<=10:
                # One region
                MaxDiff = max(self.genAssemblyObj.source1.reg,self.genAssemblyobj.source2.reg,self.genAssemblyobj.destination.reg) - min(self.genAssemblyObj.source1.reg,self.genAssemblyobj.source2.reg,self.genAssemblyobj.destination.reg)
                GeneratedTable = np.zeros(MaxDiff+4,self,self.bits)
                self.table_array.append(GeneratedTable)
                self.table_index.append()
            elif differenceS1S2<=5 or differenceS2D1<=5 or differenceS1D1<=5:
                # Two regions
                MinDiff = min(self.genAssemblyObj.source1.reg,self.genAssemblyobj.source2.reg,self.genAssemblyobj.destination.reg)
                Table1 = np.zeros(MinDiff+4,self.bits)
                Table2 = np.zeros(4,self.bits)
                self.table_array.append(Table1)
                self.table_array.append(Table2)
            else:
                # Three regions
                Table1 = np.zeros(4, self.bits)  # Maybe the last column put r11 ???
                Table2 = np.zeros(4, self.bits)
                Table3 = np.zeros(4, self.bits)
                self.table_array.append(Table1)
                self.table_array.append(Table2)
                self.table_array.append(Table3)



