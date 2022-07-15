

import numpy as np
from parse import *
from table import *
from gui import *
from test import *


if __name__ == '__main__':
    genobj = parse_one_line("mov (16|M8)        r45.0<1>:uw   r95.0<8;8,1>:ud r97.0<1;1,0>:ud")
    generateTable = TableChart()
    generateTable.AssignNewObj(genobj)
    for i in range(len(generateTable.tableNpArray)):
        PrinTable(generateTable.tableNpArray[i], generateTable.tableRegNumber[i],64)
        print("===================================================================================================================================================================================================")
