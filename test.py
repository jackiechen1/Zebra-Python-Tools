from tkinter import *
root = Tk()  # Make sure to execute this first before using BooleanVar().
boolvar = BooleanVar()
boolvar.set(True)
boolvar.get()

boolvar.set(False)
class test:
    boolvar = BooleanVar(None,False)
    def some(self):
        self.boolvar.set(True)
        Checkbutton(root, text='Example label switch', variable=self.boolvar,
                    onvalue=True,
                    offvalue=False)
