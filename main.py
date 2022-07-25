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