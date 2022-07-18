from tkinter import *
from table import *

ExampleText = """add (8|M0)               r11.0<1>:ud   r7.0<1;1,0>:ud r101.0<1;1,0>:ud
mov (16|M0)               r120.0<1>:ud   r127.0<1;1,0>:ud
mov (8|M0)               r105.0<2>:ud   r70.0<1;1,0>:ud
mov (8|M0)               r1.1<2>:ud   r5.0<1;1,0>:ud
mov (8|M0)               r13.0<1>:ud   r79.0<4;4,2>:ud
mov (8|M0)               r16.0<1>:uw   r13.0<8;8,1>:uw"""
ExampleModeLabels = ["This example shows an operation adding 8 elements of r7 and r101 to r11",
                     "This example shows moving 16 elements from r127 to r20",
                     "This example shows the destination (r105) located every other element",
                     "This example shows the destination (r1) adding an offset of one elements",
                     "This example shows the source (r79) changing v,w,h",
                     "This example changing the data type from double word (32 bits) to word (16 bits)."]

default_font = ("Helvetica", 10)
default_small_font = ("Helvetica", 8)
default_font_big = ("Helvetica", 20, "bold")
default_font_bold_ital = ("Helvetica", 10, "bold", "italic")

table_size_corresponding = {32:default_font,64:default_small_font,}

class GUI:

    def visualize(self):
        self.softClean()
        self.updateText()
        self.renderTable()

    # Soft clean do not clean the text input
    def softClean(self):
        self.genobjs = []
        self.command_labels = []
        self.MaxCommand = 1
        self.currentCommand = 0
        self.nextButton.configure(state=DISABLED)
        self.previousButton.configure(state=DISABLED)
        self.cleanWidgets()

    def cleanWidgets(self):
        self.canvas.delete('all')
        for widget in self.command_label.winfo_children():
            widget.destroy()

    def clean(self):
        self.softClean()
        self.text_input.delete("1.0", "end")
        self.exampleMode = False
        self.example_label.config(text="")

    def example(self):
        self.clean()
        self.text_input.insert("1.0", ExampleText)  # clean before insert
        self.exampleMode = True
        return

    # Previous command
    def previous(self):
        self.currentCommand -= 1
        if not self.currentCommand:  # reach the first page
            self.previousButton.configure(state=DISABLED)
        self.nextButton.configure(state=NORMAL)
        self.cleanWidgets()
        self.renderTable()

    # Next command
    def next(self):
        self.currentCommand += 1
        if self.currentCommand == self.MaxCommand - 1:
            self.nextButton.configure(state=DISABLED)
        self.cleanWidgets()
        self.previousButton.configure(state=NORMAL)
        self.renderTable()

    def renderTable(self):
        for widget in self.command_label.winfo_children():
            widget.destroy()

        self.table.AssignNewObj(self.genobjs[self.currentCommand], self.bits.get())
        self.drawBackgroundCanvas()
        self.drawRegion()
        self.displayBitIndex()
        self.UpdateCommandLabel()
        if self.exampleMode:
            self.example_label.config(text=ExampleModeLabels[self.currentCommand])
        return


    widths = 1500  # widths and heights of Main windows
    heights = 900
    main_window = Tk()

    currentCommand = 0  # Index of current command
    MaxCommand = 1
    genobjs = []  # A list of gen Assembly object
    command_labels = []  # A list of list of command labels
    table = TableChart()
    exampleMode = False
    RadioFrame = Frame()

    # Label and Text
    text_input = Text(width=int(widths / 12.0),
                      height=int(heights / 40.0))
    main_label = Label(text="Gen Assembly Visualize tool 1.0", font=default_font_big)
    command_label = Label()  # for demonstrating the command in different color panel
    example_label = Label(text="", fg="black", font=default_font_bold_ital)  # display the example comments
    bits_selection_label = Label(master=RadioFrame, text="Bits select", fg="black", font=default_font)

    # Button
    visualizeButton = Button()
    cleanButton = Button()
    exampleButton = Button()
    previousButton = Button()
    nextButton = Button()

    # Canvas
    canvas = Canvas(main_window, width=870, height=350, bg="#C5c5c5")
    regNum = canvas.create_text(0, 0, )

    # Bits selection
    bits = IntVar(None, 32)
    bits1 = Radiobutton()
    bits2 = Radiobutton()

    def __init__(self):
        # Initialize windows
        self.createWidgets()
        return

    def createWidgets(self):
        self.visualizeButton = Button(text="Visualize", width=8, height=2, command=self.visualize, relief=RAISED,
                                      borderwidth=5)
        self.cleanButton = Button(text="Clean", width=8, height=2, command=self.clean, relief=RAISED, borderwidth=5)
        self.exampleButton = Button(text="Example", width=8, height=2, command=self.example, relief=RAISED,
                                    borderwidth=5)
        self.previousButton = Button(text="Previous", width=8, height=2, command=self.previous, relief=RAISED,
                                     borderwidth=5, state=DISABLED)
        self.nextButton = Button(text="Next", width=8, height=2, command=self.next, relief=RAISED, borderwidth=5,
                                 state=DISABLED)
        self.bits1 = Radiobutton(master=self.RadioFrame, text="32 bits", variable=self.bits, value=32)
        self.bits2 = Radiobutton(master=self.RadioFrame, text="64 bits", variable=self.bits, value=64)

    def packElements(self):
        self.main_window.title("Gen Assembly Visualize Tool")

        # Labels and text
        self.main_label.pack()
        self.text_input.place(x=200, y=100)
        self.example_label.place(x=int(self.widths / 12.0 * 5), y=self.heights / 2 - 50)

        # Place Button
        self.visualizeButton.place(x=int(self.widths / 12.0 * 10), y=int(self.heights / 15.0) + 50)
        self.cleanButton.place(x=int(self.widths / 12.0 * 10), y=int(self.heights / 15.0) + 150)
        self.exampleButton.place(x=int(self.widths / 12.0 * 10), y=int(self.heights / 15.0) + 250)
        self.previousButton.place(x=50, y=int(self.heights * 3 / 4.0))
        self.nextButton.place(x=int(self.widths / 12.0 * 10), y=int(self.heights * 3 / 4.0))

        # Main window
        self.main_window.minsize(width=self.widths, height=self.heights)
        self.main_window.geometry("+300+100")

        # Canvas
        self.canvas.place(x=200, y=int(self.heights / 2))

        # Radios
        self.bits_selection_label.pack()
        self.bits1.pack()
        self.bits2.pack()
        self.RadioFrame.place(x=int(self.widths / 12.0 * 10), y=int(self.heights / 15.0) + 350)

    # Draw background grey canvas
    def drawBackgroundCanvas(self):
        for i in range(15):
            y = i * self.table.square_height
            for j in range(self.table.bits):
                x = j * self.table.square_width
                self.canvas.create_rectangle(x, y, x + self.table.square_width, y + self.table.square_height,
                                             fill="#C5c5c5", outline='black')

    # Draw three regions (source1, source2, destination)
    def drawRegion(self):
        tableNumber = self.table.tableRegNumber[0][2]
        previousRow = 0
        for t in range(0, tableNumber + 1):
            M, N = self.table.tableNpArray[t].shape
            for i in range(M):  # row
                for j in range(N):  # column
                    fill_color = self.table.tableNpArray[t][i][j]
                    self.canvas.create_rectangle(self.table.square_width * j,
                                                 self.table.square_height * (i + 1 + previousRow),
                                                 self.table.square_width * (j + 1),
                                                 self.table.square_height * (i + 2 + previousRow),
                                                 fill=fill_color, outline='black')
                y = (i + 1.5 + previousRow) * self.table.square_height
                self.regNum = self.canvas.create_text(815, y, text="r" + str(
                    self.table.tableRegNumber[t][0] + i),
                                                      fill='black',
                                                      font=default_font_bold_ital)
            previousRow += (M + 1)

    # Display the bit index, range from 0 to 32/64, stride by element size
    def displayBitIndex(self):
        # Display the bit index
        for j in range(self.table.bits):
            if not j % self.table.element_size:
                x = j * self.table.square_width
                self.canvas.create_text(x + 10-(self.table.bits-32)/16, 10, text=str(self.table.bits - j - 1), fill='black',
                                        font=table_size_corresponding[self.table.bits])

    # Update command label after switching to a new command
    def UpdateCommandLabel(self):
        # data[0] text before destination
        # data[1] destination
        # data[2] source1
        # data[3] source2 --option
        # data[4] other modification flag --option
        data = self.command_labels[self.currentCommand]
        self.command_label = Frame(master=self.main_window)
        l1 = Label(master=self.command_label, text=data[0], fg="black", font=default_font_bold_ital)
        l2 = Label(master=self.command_label, text=data[1], fg=colorMap[3], font=default_font_bold_ital)
        l3 = Label(master=self.command_label, text=data[2], fg=colorMap[1], font=default_font_bold_ital)

        l1.pack(side=LEFT)
        l2.pack(side=LEFT)
        l3.pack(side=LEFT)

        if len(data) > 3 and not self.table.genAssemblyObj.immediateSourceOperands:  # additional source2
            l4 = Label(master=self.command_label, text=data[3], fg=colorMap[2], font=default_font_bold_ital)
            l4.pack(side=LEFT)
        elif len(
                data) == 4 and self.table.genAssemblyObj.immediateSourceOperands:  # no source2 but have immediate Source Operands
            l4 = Label(master=self.command_label, text=data[3], fg="black", font=default_font_bold_ital)
            l4.pack(side=LEFT)
        else:  # source2 and immediate flag
            l4 = Label(master=self.command_label, text=data[3], fg=colorMap[2], font=default_font_bold_ital)
            l5 = Label(master=self.command_label, text=data[4], fg="black", font=default_font_bold_ital)
            l4.pack(side=LEFT)
            l5.pack(side=LEFT)

        self.command_label.place(x=200, y=self.heights / 2 - 50)

    def updateText(self):
        inputText = self.text_input.get("1.0", "end")
        self.genobjs, self.command_labels = parse_lines(inputText)
        if not len(self.genobjs):
            return
        self.MaxCommand = len(self.genobjs)
        if self.MaxCommand != 1:
            self.nextButton.configure(state=NORMAL)

    def run(self):
        self.packElements()
        self.main_window.mainloop()
