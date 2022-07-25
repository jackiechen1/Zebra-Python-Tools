from gui import *

numberOfBytes = 32  # 32 or 64
def CheckModule():
    try:
        import numpy
    except ImportError:
        print("numpy is not installed. Using '$pip install numpy' to install the package")
    try:
        import tkinter
    except ImportError:
        print("tkinter is not installed")
    print("All modules are installed!")
if __name__ == '__main__':
    CheckModule()
    MainGui = GUI()
    MainGui.run()


# Zebra-Python-Tools
'''
Last modify by Zhongyi Jiang  07/25/2022
Web version: https://jackiechen1.github.io/zebratest.github.io/ 
Todo list:
1. prediction usage
2. flag modifier usage
3. saturation/ source modifier, including - ~ sat abs
4. if and else support
5. check constraint
6. more widgets options

'''