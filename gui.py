from tkinter import *

import table
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
                     "This example changing the data type from double word (32 bytes) to word (16 bytes)."]

default_font = ("Helvetica", 10)
default_small_font = ("Helvetica", 8)
default_font_big = ("Helvetica", 20, "bold")
default_font_bold_ital = ("Helvetica", 10, "bold", "italic")
default_font_bold = ("Helvetica", 10, "bold")
table_size_corresponding = {32: default_font, 64: default_small_font, }
project_list = ["DEFAULT", "ACM", "ACMPLUS", "ADL", "ADLS", "ARL", "ATS", "DG1", "MAR", "MTL", "PVC", "RKLC", "RKLGM",
                "RLT", "RYF", "SVL", "TGLLP"]


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

    def cleanExampleLabels(self):
        self.example_mode.set(self.example_mode.get())
        if self.example_mode.get():
            self.example_label.config(text=ExampleModeLabels[self.currentCommand])
        else:
            self.example_label.config(text="")

    def clean(self):
        self.softClean()
        self.text_input.delete("1.0", "end")
        self.example_mode.set(False)
        self.example_label.config(text="")

    def example(self):
        self.clean()
        self.text_input.insert("1.0", ExampleText)  # clean before insert
        self.example_mode.set(True)
        self.visualize()

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

        self.table.AssignNewObj(self.genobjs[self.currentCommand], self.Bytes.get())

        self.drawRegion()
        self.drawElementBoundary()
        self.drawBackgroundCanvas()
        self.displayBitIndex()
        self.UpdateCommandLabel()
        if self.example_mode.get():
            self.example_label.config(text=ExampleModeLabels[self.currentCommand])
        return

    widths = 1100  # widths and heights of Main windows
    heights = 900

    currentCommand = 0  # Index of current command
    MaxCommand = 1
    genobjs = []  # A list of gen Assembly object
    command_labels = []  # A list of list of command labels
    table = TableChart()
    main_window = Tk()
    example_mode = BooleanVar(None, False)
    project = StringVar(None, "DEFAULT")

    # Main window and frames
    topHalf = Frame(master=main_window, bd=5)
    topHalfButtons = Frame(master=topHalf, bd=10)
    topHalfLabels = Frame(master=topHalf)

    middlePart = Frame(master=main_window)
    bottomHalf = Frame(master=main_window)
    bottomHalfButtons = Frame(master = bottomHalf)

    # Label and Text
    text_input = Text(master=topHalf, width=int(widths / 12.0),
                      height=int(heights / 60.0))
    main_label = Label(text="Gen Assembly Visualize tool 1.0", font=default_font_big)
    command_label = Frame(master=middlePart)  # for demonstrating the command in different color panel
    example_label = Label(master=middlePart, text="", fg="black",
                          font=default_font_bold_ital)  # display the example comments
    Bytes_selection_label = Label(master=topHalfLabels, text="bytes select", fg="black", font=default_font)
    Project_selection_label = Label(master=topHalfLabels, text="Project select", fg="black", font=default_font)

    # Button
    visualizeButton = Button()
    cleanButton = Button()
    exampleButton = Button()
    previousButton = Button()
    nextButton = Button()

    # Canvas
    canvas = Canvas(bottomHalf, width=widths / 1.5, height=heights / 3, bg="#C5c5c5")

    # Bytes selection
    Bytes = IntVar(None, 32)
    Bytes1 = Radiobutton()
    Bytes2 = Radiobutton()

    # Check Box
    exampleLabelTurnOff = Checkbutton()
    projectOption = OptionMenu(topHalfLabels, project, *project_list)
    regNum = canvas.create_text(0, 0, )

    def __init__(self):
        # Initialize windows
        self.createWidgets()
        return

    def createWidgets(self):
        self.visualizeButton = Button(master=self.topHalfButtons, text="Visualize", width=8, height=2,
                                      command=self.visualize, relief=RAISED,
                                      borderwidth=5)
        self.cleanButton = Button(master=self.topHalfButtons, text="Clean", width=8, height=2, command=self.clean,
                                  relief=RAISED, borderwidth=5)
        self.exampleButton = Button(master=self.topHalfButtons, text="Example", width=8, height=2, command=self.example,
                                    relief=RAISED,
                                    borderwidth=5)
        self.previousButton = Button(master=self.bottomHalfButtons, text="Previous", width=8, height=2, command=self.previous,
                                     relief=RAISED,
                                     borderwidth=5, state=DISABLED)
        self.nextButton = Button(master=self.bottomHalfButtons, text="Next", width=8, height=2, command=self.next,
                                 relief=RAISED, borderwidth=5,
                                 state=DISABLED)
        self.Bytes1 = Radiobutton(master=self.topHalfLabels, text="32 Bytes", variable=self.Bytes, value=32)
        self.Bytes2 = Radiobutton(master=self.topHalfLabels, text="64 Bytes", variable=self.Bytes, value=64)

        self.exampleLabelTurnOff = Checkbutton(master=self.topHalfLabels, text='Example label',
                                               variable=self.example_mode,
                                               onvalue=True,
                                               offvalue=False, command=self.cleanExampleLabels)

    def packElements(self):
        self.main_window.title("Gen Assembly Visualize Tool")

        # pack Buttons
        self.visualizeButton.pack(side=TOP, pady=10)
        self.cleanButton.pack(side=TOP, pady=10)
        self.exampleButton.pack(side=TOP, pady=10)

        # pack top labels
        self.Bytes_selection_label.pack(side=TOP)
        self.Bytes1.pack(side=TOP)
        self.Bytes2.pack(side=TOP)
        self.Project_selection_label.pack(side=TOP, pady=10)
        self.projectOption.pack(side=TOP)
        self.exampleLabelTurnOff.pack(side=TOP, pady=20)

        # pack top half
        self.text_input.pack(side=LEFT)
        self.topHalfButtons.pack(side=LEFT)
        self.topHalfLabels.pack(side=LEFT)

        # pack middle section
        self.command_label.pack()
        self.example_label.pack()

        # pack buttom section
        self.canvas.pack(side=TOP)
        self.previousButton.pack(side = LEFT,padx = 200)
        self.nextButton.pack(side = RIGHT,padx = 200)
        self.bottomHalfButtons.pack()

        # pack all frames
        self.main_label.pack()
        self.topHalf.pack()
        self.middlePart.pack()
        self.bottomHalf.pack()

        # Main window
        self.main_window.minsize(width=self.widths, height=self.heights)
        self.main_window.geometry("+200+100")

    # Draw background grey canvas and solid line between elements
    def drawBackgroundCanvas(self):
        j = 0
        while j < self.Bytes.get():
            left = j * self.table.square_width
            right = (j + self.table.element_size) * self.table.square_width
            self.canvas.create_rectangle(left, 0, right, 15 * self.table.square_height,
                                         outline='black')
            j += self.table.element_size

    def drawHalfRegion(self, x1, y1, x2, y2, fill_color):
        color1 = colorMap[int(fill_color[0])]
        color2 = colorMap[int(fill_color[1])]
        self.canvas.create_rectangle(x1, y1, x2, (y1 + y2) / 2.0, fill=color1, outline='black', width=1, dash=1)
        self.canvas.create_rectangle(x1, (y1 + y2) / 2.0, x2, y2, fill=color2, outline='black', width=1, dash=1)

    # Draw three regions (source1, source2, destination)
    def drawRegion(self):
        tableNumber = self.table.tableRegNumber[0][2]
        previousRow = 0
        for t in range(0, tableNumber + 1):
            M, N = self.table.tableNpArray[t].shape
            for i in range(M):  # row
                for j in range(N):  # column
                    fill_color = self.table.tableNpArray[t][i][j]
                    if fill_color != colorMap[4] and fill_color != colorMap[5] and fill_color != colorMap[6]:
                        self.canvas.create_rectangle(self.table.square_width * j,
                                                     self.table.square_height * (i + 1 + previousRow),
                                                     self.table.square_width * (j + 1),
                                                     self.table.square_height * (i + 2 + previousRow),
                                                     fill=fill_color, outline='black', width=1, dash=1)
                    else:
                        self.drawHalfRegion(self.table.square_width * j,
                                            self.table.square_height * (i + 1 + previousRow),
                                            self.table.square_width * (j + 1),
                                            self.table.square_height * (i + 2 + previousRow),
                                            fill_color)

                y = (i + 1.5 + previousRow) * self.table.square_height
                self.regNum = self.canvas.create_text(self.widths/1.68, y, text="r" + str(
                    self.table.tableRegNumber[t][0] + i),
                                                      fill='black',
                                                      font=default_font_bold_ital)
            previousRow += (M + 1)

    def drawElementBoundary(self):
        tableNumber = self.table.tableRegNumber[0][2]
        previousRow = 0
        for t in range(0, tableNumber + 1):
            M, N = self.table.tableNpArray[t].shape
            i = 0
            j = 0
            while i < M:  # row
                while j < N:  # column
                    left = j
                    if self.table.tableNpArray[t][i][left] == colorMap[1]:  # Source1
                        OneElementChunk = self.table.genAssemblyObj.source1.datatype
                    elif self.table.tableNpArray[t][i][left] == colorMap[2]:  # Source2
                        OneElementChunk = self.table.genAssemblyObj.source2.datatype
                    elif self.table.tableNpArray[t][i][left] == colorMap[3]:  # Destination
                        OneElementChunk = self.table.genAssemblyObj.destination.datatype
                    else:  # background color
                        OneElementChunk = self.table.element_size
                    right = j + OneElementChunk
                    if self.table.tableNpArray[t][i][left] != colorMap[0]:
                        # top left corner and bottom right corner
                        self.canvas.create_rectangle(self.table.square_width * left,
                                                     self.table.square_height * (i + 1 + previousRow),
                                                     self.table.square_width * right,
                                                     self.table.square_height * (i + 2 + previousRow),
                                                     outline='black', width=3)
                    j = right
                i += 1
                j = 0
            previousRow += (M + 1)

    # Display the bit index, range from 0 to 32/64, stride by element size
    def displayBitIndex(self):
        # Display the bit index
        for j in range(self.table.bytes):
            if not j % self.table.element_size:
                x = j * self.table.square_width
                self.canvas.create_text(x + 10 - (self.table.bytes - 32) / 16, 10, text=str(self.table.bytes - j - 1),
                                        fill='black',
                                        font=table_size_corresponding[self.table.bytes])

    # Update command label after switching to a new command
    def UpdateCommandLabel(self):
        # data[0] text before destination
        # data[1] destination
        # data[2] source1
        # data[3] source2 --option
        # data[4] other modification flag --option

        # Clean command label frame
        for widget in self.command_label.winfo_children():
            widget.destroy()
        data = self.command_labels[self.currentCommand]
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


    # Update command labels
    def updateText(self):
        inputText = self.text_input.get("1.0", "end")
        self.genobjs, self.command_labels = parse_lines(inputText)
        if not len(self.genobjs):
            return
        for obj in self.genobjs:
            CheckConstraint(obj, self.project)
        self.MaxCommand = len(self.genobjs)
        if self.MaxCommand != 1:
            self.nextButton.configure(state=NORMAL)

    def run(self):
        self.packElements()
        self.main_window.mainloop()
