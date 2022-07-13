from tkinter import *
import numpy as np
def test():
    list = [[0,0,0,0], [0, 0, 0, 0], [0, 0, 0, 0]]
    a = len(list)
    length = 300//a
    ws = Tk()
    ws.geometry("1000x800")

    list_table_rendering = []
    default_font = ("Helvetica", 8)
    class table_rendering:
        element_size = 4
        source1_color = "#D97E4A"
        source2_color = "#D97E4A"
        destination_color = "#D97E4A"
        default_color = "#D97E4A"
        bits = 32
        square_width = 30 # if 64 width =15
        square_height =30

    canvas = Canvas(ws, width=1000, height=800, bg="#7698A6")
    canvas.pack(side=RIGHT)
    table = table_rendering()
    for i in range(a):
        y = i * table.square_height
        for j in range(table.bits):
            x = j * table.square_width
            canvas.create_rectangle(x, y, x+table.square_width, y+table.square_height, fill="#D97E4A",outline = 'black')
           # canvas.create_text(x+10,y+10,text = str(32-j),fill = 'black',font = default_font)

    def displayIndex():
        for j in range(table.bits):
            if not j%table.element_size:
                x = j*table.square_width
                canvas.create_text(x+10,10,text = str(table.bits-j-1),fill = 'black',font = default_font)
    displayIndex()
    ws.mainloop()

def AssignArray(ExecSize,s,v,w,h,t,table,bits,row):
    # Assign Array value based on Gen assemblly rules
    for i in range(ExecSize):
        position = (s+(i/w)*v+i%w*h)*t/8
        if position>bits:
            position-=bits #second row
            table[row + 1:position + t / 8, i] = 1
        else:
            table[row:position + t / 8, i] = 1
    return table
table = np.zeros((4,32))
table = AssignArray(8,1,4,1,0,8,table,32,1)
print(table)