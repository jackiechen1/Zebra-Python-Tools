from tkinter import messagebox
from main import numberOfBytes

datatype_bytes_conversion = {
    "b": 1,
    "ub": 1,
    "w": 2,
    "uw": 2,
    "d": 4,
    "ud": 4,
    "q": 8,
    "uq": 8,
    "hf": 2,
    "f": 4,
    "df": 8,
    "uv": 0,  # These three types are special type which needs to define separately
    "v": 0,
    "vf": 0
}

# Mnemonic needs one source
MnemonicList1 = ["mov"]

# Mnemonic needs two sources
MnemonicList2 = ["add", "math.div"]
conditionValueList = ["ze", "eq", "nz", "ne", "gt", "ge", "lt", "le"]
largeProjectList = ["PVC", "RLT", "MAR", "DEFAULT"]


def ThrowGrammarError(line, error):
    message = "Unknown grammar syntax at " + line + "\n" + error
    ThrowErrorMessage(message)


def ThrowErrorMessage(message):
    messagebox.showerror('Error message', message)


class Source:
    # e.g. -r5.0<0;1,0>:f
    modifiers = ''  # Source modifiers could be -,~,abs and so on
    reg = 5  # reg number
    offset = 0  # aka S
    V = 1  # Vertical stride
    W = 1  # Width
    H = 0  # Horizontal stride
    datatype = -1  # units in bits
    constant = False  # if source is a constant

    def __init__(self):
        self.modifiers = ''  # Source modifiers could be -,~,abs and so on
        self.reg = 100  # reg number
        self.offset = -1  # aka S
        self.V = -1  # Vertical stride
        self.W = -1  # Width
        self.H = -1  # Horizontal stride
        self.datatype = -1  # units in bytes


class Destination:
    # e.g. -r1.0<1>:f
    modifiers = ''  # Source modifiers could be -,~,abs,sat and so on
    reg = 1  # reg number
    offset = 0  # aka S
    H = 1  # Horizontal stride
    datatype = 32  # units in bytes

    def __init__(self):
        self.modifiers = ''  # Source modifiers could be -,~,abs,sat and so on
        self.reg = -1  # reg number
        self.offset = -1  # aka S
        self.H = -1  # Horizontal stride
        self.datatype = -1  # units in bits


class ExecInfo:
    # e.g. (8|M0)
    ExecSize = 8  # Element size
    mask = 0  # Idle for now

    def __init__(self):
        self.ExecSize = 0
        self.mask = 0


class FlagModify:  # Or Condition modifiers
    # e.g. (lt)f0.0
    condition = ''  # Options: ze,eq,nz,ne,gt,ge,lt,le
    offset = 0


def parsePrediction(line, obj):  # Not require
    if not line:
        return ""
    if line[0] != '[' and line[0] != '(':
        return line
    rightBracket = line.find(']')
    if rightBracket == -1:
        rightBracket = line.find(')')
        if rightBracket == -1:
            ThrowGrammarError(line, "Can't recognize prediction pattern")
    obj.predAndMask = line[1:rightBracket]
    return line[rightBracket + 1:]


def parseMnemonic(line, obj):
    if not line:
        return ""
    bracket = line.find('(')
    if bracket == -1:
        ThrowGrammarError(line, "Can't find ExecutionMask")
    if line[0:bracket] in MnemonicList1 or line[0:bracket] in MnemonicList2:
        obj.mnemonic = line[0:bracket]
        return line[bracket:]
    else:
        ThrowGrammarError(line, "Fail parsing Mnemonic operator")
        return ""


def parseExecutionMask(line, obj):
    if not line:
        return ""
    leftBracket = line.find('(')
    rightBracket = line.find(')')
    bar = line.find('|')
    try:
        obj.execinfo.ExecSize = int(line[leftBracket + 1:bar])
        obj.execinfo.mask = int(line[bar + 2:rightBracket])
        return line[rightBracket + 1:]
    except(Exception,):
        ThrowGrammarError(line, "Fail parsing ExecutionMask")
        return ""


def parseFlagModifier(line, obj):  # Not require
    if not line:
        return ""
    if line[0] != '[':
        return line
    leftBracket = line.find('(')
    rightBracket = line.find(']')
    try:
        conditionValue = line[leftBracket + 1:leftBracket + 3]

        if conditionValue not in conditionValueList:
            ThrowGrammarError(line, "Unknown condition value")

        obj.flag.condition = conditionValue
        obj.flag.offset = line[leftBracket + 4:rightBracket]
        return line[rightBracket + 1:]
    except(Exception,):
        ThrowGrammarError(line, "Can't parse Flag Modifier")


def parseDestination(line, obj):
    if not line:
        return ""
    regexStart = line.find('r')
    leftBracket = line.find('<')
    rightBracket = line.find('>')
    dotPos = line.find('.')
    colon = line.find(':')
    endIndex = -1
    if regexStart == -1 or leftBracket == -1 or rightBracket == -1 or dotPos == -1 or colon == -1:
        ThrowGrammarError(line, "Fail to recognize region pattern")
    if line[0] == '-' or line[0] == '(' or line[0] == '~':
        obj.destination.modifiers = line[0, regexStart]
    if line[regexStart + 1] == '[':
        # TODO: Indirect Source Operands
        ThrowGrammarError(line, "Indirect Source Operands unsupported yet")
    else:
        try:
            obj.destination.reg = int(line[regexStart + 1:dotPos])
            obj.destination.offset = int(line[dotPos + 1:leftBracket])
            obj.destination.H = int(line[leftBracket + 1:rightBracket])
            if line[colon + 1:colon + 2] in datatype_bytes_conversion.keys():  # one char data type
                obj.destination.datatype = datatype_bytes_conversion[line[colon + 1:colon + 2]]
                endIndex = colon + 1
            elif line[colon + 1:colon + 3] in datatype_bytes_conversion.keys():  # two char data type
                obj.destination.datatype = datatype_bytes_conversion[line[colon + 1:colon + 3]]
                endIndex = colon + 2
            else:
                ThrowGrammarError(line, "Can't recognize datatype")
        except(Exception,):
            ThrowGrammarError(line, "Can't recognize register number")
    return line[endIndex + 1:]


def parseSource(line, obj, order):  # Second source not require
    if not line:
        return ""
    regexStart = line.find('r')
    leftBracket = line.find('<')
    rightBracket = line.find('>')
    semicolon = line.find(';')
    dotPos = line.find('.')
    colon = line.find(':')
    comma = line.find(',')
    endIndex = -1
    if regexStart == -1 or leftBracket == -1 or rightBracket == -1 or dotPos == -1 or colon == -1 or semicolon == -1 or comma == -1:
        # Error case
        if (order == 1 and colon == -1) or (order == 2 and colon == -1 and obj.mnemonic in MnemonicList1):
            ThrowGrammarError(line, "Fail to recognize region pattern")
        # No offset input
        elif dotPos == -1 and leftBracket != -1 and regexStart != -1 and leftBracket - regexStart <= 4:
            pass
        # First source is a constant
        elif order == 1 and colon != -1:
            obj.source1.constant = True
            if line[colon + 1:colon + 2] in datatype_bytes_conversion.keys():
                endIndex = colon + 1
            elif line[colon + 1:colon + 3] in datatype_bytes_conversion.keys():
                endIndex = colon + 2
            else:
                ThrowGrammarError(line, "Can't recognize datatype")
            return line[endIndex + 1:]
        elif order == 2:
            # Second source is a constant
            if colon != -1 and obj.mnemonic in MnemonicList2:
                obj.source2.constant = True
                if line[colon + 1:colon + 2] in datatype_bytes_conversion.keys():
                    endIndex = colon + 1
                elif line[colon + 1:colon + 3] in datatype_bytes_conversion.keys():
                    endIndex = colon + 2
                else:
                    ThrowGrammarError(line, "Can't recognize datatype")
                return line[endIndex + 1:]
            # Don't need a second source
            elif obj.mnemonic in MnemonicList1:
                obj.source2.constant = True
                return line
            # Other cases happened
            else:
                ThrowErrorMessage("Bug in source code! Unexpected cases happened!")
                return line[endIndex + 1:]
        else:
            ThrowErrorMessage("Bug in source code! Unexpected cases happened!")
            return line[endIndex + 1:]
    if line[0] == '-' or line[0] == '(' or line[0] == '~':
        if order == 1:
            obj.source1.modifiers = line[0:regexStart]
        else:
            obj.source2.modifiers = line[0: regexStart]
    if line[regexStart + 1] == '[':
        # TODO: Indirect Source Operands
        ThrowGrammarError(line, "Indirect Source Operands unsupported yet")
    else:
        try:
            if order == 1:
                # No offset case
                if dotPos == -1:
                    obj.source1.offset = 0
                    obj.source1.reg = int(line[regexStart + 1: leftBracket])
                else:
                    obj.source1.offset = int(line[dotPos + 1: leftBracket])
                    obj.source1.reg = int(line[regexStart + 1: dotPos])
                obj.source1.V = int(line[leftBracket + 1: semicolon])
                obj.source1.W = int(line[semicolon + 1: comma])
                obj.source1.H = int(line[comma + 1: rightBracket])
                if line[colon + 1: colon + 2] in datatype_bytes_conversion.keys():  # one char data type
                    obj.source1.datatype = datatype_bytes_conversion[line[colon + 1: colon + 2]]
                    endIndex = colon + 1
                elif line[colon + 1: colon + 3] in datatype_bytes_conversion.keys():  # two char data type
                    obj.source1.datatype = datatype_bytes_conversion[line[colon + 1: colon + 3]]
                    endIndex = colon + 2
                else:
                    ThrowGrammarError(line, "Can't recognize datatype")
            else:
                # No offset case
                if dotPos == -1:
                    obj.source2.offset = 0
                    obj.source2.reg = int(line[regexStart + 1: leftBracket])
                else:
                    obj.source2.offset = int(line[dotPos + 1: leftBracket])
                    obj.source2.reg = int(line[regexStart + 1: dotPos])
                obj.source2.V = int(line[leftBracket + 1: semicolon])
                obj.source2.W = int(line[semicolon + 1: comma])
                obj.source2.H = int(line[comma + 1: rightBracket])
                if line[colon + 1: colon + 3] in datatype_bytes_conversion.keys():  # two char data type
                    obj.source2.datatype = datatype_bytes_conversion[line[colon + 1: colon + 3]]
                    endIndex = colon + 2
                elif line[colon + 1: colon + 2] in datatype_bytes_conversion.keys():  # one char data type
                    obj.source2.datatype = datatype_bytes_conversion[line[colon + 1: colon + 2]]
                    endIndex = colon + 1
                else:
                    ThrowGrammarError(line, "Can't recognize datatype")

        except(Exception,):
            ThrowGrammarError(line, "Can't recognize register number")
    return line[endIndex + 1:]


def parseImmediateSourceOperands(line, obj):
    if not line:
        return ""
    colon = line.find(':')

    # Ignore the source reg if we find an immdiate source operands
    if colon != -1:
        obj.source1.constant = True
        obj.source2.constant = True
    return ""


def parse_one_line(line, comments):
    # remove space
    oneline = line.replace(" ", "")

    # skip comments
    if oneline[0] == '/' and oneline[1] == '/':
        return None, None, comments
    elif oneline[0] == '/' and oneline[1] == '*':
        return None, None, True
    elif oneline.find("*/") != -1:
        return None, None, False
    elif comments:
        return None, None, True
    genAssemblyObj = GenAssembly()
    lineLabel = []
    # parse line in order and save critical segmentation for label
    line = parsePrediction(oneline, genAssemblyObj)
    line = parseMnemonic(line, genAssemblyObj)
    line = parseExecutionMask(line, genAssemblyObj)
    line = parseFlagModifier(line, genAssemblyObj)
    BeforeDestination = oneline.find(line)

    line = parseDestination(line, genAssemblyObj)
    BeforeSource1 = oneline.find(line)
    line = parseSource(line, genAssemblyObj, 1)

    lineLabel.append(oneline[0:BeforeDestination])
    lineLabel.append(oneline[BeforeDestination:BeforeSource1])
    if not line:
        BeforeSource2 = len(oneline)
        lineLabel.append(oneline[BeforeSource1:BeforeSource2])
    else:
        BeforeSource2 = oneline.find(line)
        lineLabel.append(oneline[BeforeSource1:BeforeSource2])

    line = parseSource(line, genAssemblyObj, 2)

    if not line:
        BeforeFlag = len(oneline)
        lineLabel.append(oneline[BeforeSource2:BeforeFlag])
    else:
        BeforeFlag = oneline.find(line)
        lineLabel.append(oneline[BeforeSource2:BeforeFlag])
    if line:
        lineLabel.append(line)
        parseImmediateSourceOperands(line, genAssemblyObj)
    return genAssemblyObj, lineLabel, comments


def parse_lines(lines):
    lines_list = lines.split('\n')
    objs = []
    lineLabelList = []
    comments = False  # Whether current line within a comment section
    for line in lines_list:
        if line:
            obj, lineLabel, comments = parse_one_line(line, comments)
            if obj:
                objs.append(obj)
                lineLabelList.append(lineLabel)
    return objs, lineLabelList


class GenAssembly:
    source1 = Source()  # First source (default one for one source mnemonic)
    source2 = Source()  # Second source
    destination = Destination()
    immediateSourceOperands = 0  # default none
    predAndMask = ""
    mnemonic = "mov"
    execinfo = ExecInfo()
    flag = FlagModify()

    def __init__(self):
        self.source1 = Source()
        self.source2 = Source()
        self.execinfo = ExecInfo()
        self.flag = FlagModify()
        self.destination = Destination()


# Check register region restrictions
# More info in this page: https://gfxspecs.intel.com/Predator/Home/Index/47273
def CheckConstraint(obj, project):
    n = max(obj.source1.datatype, obj.source2.datatype, obj.destination.datatype)
    if project in largeProjectList:
        if obj.execinfo.ExecSize * n > 128:
            ThrowErrorMessage(
                "Where n is the largest element size in bytes for any source or destination operand type, ExecSize * n must be <= 64. For PVC, RLT, MAR,ExecSize * n must be <= 128 ")
            return
    else:
        if obj.execinfo.ExecSize * n > 64:
            ThrowErrorMessage(
                "Where n is the largest element size in bytes for any source or destination operand type, ExecSize * n must be <= 64. For PVC, RLT, MAR,ExecSize * n must be <= 128 ")
            return

    # TODO: When the Execution Data Type is wider than the destination data type, the destination must be aligned as required by the wider execution data type and specify a HorzStride equal to the ratio in sizes of the two data types. For example, a mov with a D source and B destination must use a 4-byte aligned destination and a Dst.HorzStride of 4.
    def CheckSourceRegion(W, H, V, datatype):
        # Region restrictions:
        if obj.execinfo.ExecSize < W:
            ThrowErrorMessage("ExecSize must be greater than or equal to Width.")
        elif obj.execinfo.ExecSize == W and H and V != W * H:
            ThrowErrorMessage(
                "If ExecSize = Width and HorzStride != 0, VertStride must be set to Width * HorzStride.")
        elif W == 1 and H != 0:
            ThrowErrorMessage(
                "If Width = 1, HorzStride must be 0 regardless of the values of ExecSize and VertStride.")
        elif obj.execinfo.ExecSize == 1 and W == 1 and (V or H):
            ThrowErrorMessage("If ExecSize = Width = 1, both VertStride and HorzStride must be 0.")
        elif V == 0 and H == 0 and W != 1:
            ThrowErrorMessage(
                "If VertStride = HorzStride = 0, Width must be 1 regardless of the value of ExecSize.")
        elif obj.destination.H == 0:
            ThrowErrorMessage("Dst.HorzStride must not be 0.")
        elif ((obj.execinfo.ExecSize / W) * V + obj.execinfo.ExecSize % W * H) * datatype > numberOfBytes * 2:
            ThrowErrorMessage(" Crossing more than 2 registers")

    # TODO: VertStride must be used to cross GRF register boundaries. This rule implies that elements within a 'Width' cannot cross GRF boundaries.
    CheckSourceRegion(obj.source1.W, obj.source1.H, obj.source1.V, obj.source1.datatype)
    CheckSourceRegion(obj.source2.W, obj.source2.H, obj.source2.V, obj.source2.datatype)
    # TODO: Project specific constriction
