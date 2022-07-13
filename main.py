from tkinter import *
from tkinter.scrolledtext import ScrolledText
import numpy as np
import re
from  parse import *
def visualize():

    return


def clean():
    return


def example():
    clean()
    text_input.insert("1.0", ExampleText)  # clean before insert
    return

Bits = ["32 bits","64 bits"]

Types = ["BugFix","Feature","Refactor","Performance","Workaround",
		 "Revert","Documentation","Tools"]
# maybe S,V, H, W
ExampleText = """// This example shows a operation moving 8 elements from r7 to r11
mov (8|M0)               r11.0<1>:ud   r7.0<1;1,0>:ud
// Next example shows moving 16 elements from r7 to r11
mov (16|M0)               r11.0<1>:ud   r7.0<1;1,0>:ud
// Next example shows the destination (r11) located every other element
mov (8|M0)               r11.0<2>:ud   r7.0<1;1,0>:ud
// Next example shows the destination (r11) adding an offset of one elements
mov (8|M0)               r11.1<2>:ud   r7.0<1;1,0>:ud
// Next example shows the source (r7) modifying v,w,h
mov (8|M0)               r11.0<1>:ud   r7.0<4;4,2>:ud
// Next example changing the data type from double word (32 bits) to word (16 bits).
mov (8|M0)               r11.0<1>:uw   r7.0<8;8,1>:uw"""
SourceTable = np.zeros((32,5))
widths = 1100
heights = 700

main_window = Tk()
main_window.title("Gen Assembly Visualize Tool")
default_font = ("Helvetica", 8)
default_font_big = ("Helvetica", 20, "bold")
default_font_bold_ital = ("Helvetica", 8, "bold", "italic")



# Label and Text
text_input = Text(width=int(widths/12.0),height = int(heights/40.0)) # .get() using try and except ,delete() .insert()
#text_input.insert("1.0",ExampleText) # clean before insert
main_label = Label(text = "Gen Assembly Visualize tool 1.0",font = default_font_big)
main_label.pack()
text_input.place(x=50,y=50)


# Button
visualizeButton = Button(text = "Visualize",width=8,height=2,command=visualize,relief=RAISED,borderwidth=5)
cleanButton = Button(text = "Clean",width=8,height=2,command=clean,relief=RAISED,borderwidth=5)
exampleButton = Button(text = "Example",width=8,height=2,command=example,relief=RAISED,borderwidth=5)

# Place Button
visualizeButton.place(x = int(widths/12.0*10),y=int(heights/15.0))
cleanButton.place(x = int(widths/12.0*10),y=int(heights/15.0)+100)
exampleButton.place(x = int(widths/12.0*10),y=int(heights/15.0)+200)

# For placing Labels and ScrolledText
main_window.minsize(width=widths,height=heights)
main_window.geometry("+300+100")
main_window.mainloop()

#if __name__ == '__main__':

    #parse_one_line("[f1.0] add (8|M8) [(nz)f0.0]         r11.0<1>:ud   r7.0<1;1,0>:ud r14.0<8;8,1>:f")
