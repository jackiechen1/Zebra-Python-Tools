from tkinter import *

widths = 1100  # widths and heights of Main windows
heights = 900
main_window = Tk()

default_font = ("Helvetica", 10)
default_small_font = ("Helvetica", 8)
default_font_big = ("Helvetica", 20, "bold")
default_font_bold_ital = ("Helvetica", 10, "bold", "italic")

# Label and Text
text_input = Text(width=int(widths / 12.0),
                  height=int(heights / 40.0))
main_label = Label(text="Gen Assembly Visualize tool 1.0", font=default_font_big)
command_label = Label(text = "ABHDGASKJHDKA", font=default_font_bold_ital)  # for demonstrating the command in different color panel
example_label = Label(text="DASFASFASFA", fg="black", font=default_font_bold_ital)  # display the example comments


# Canvas
canvas = Canvas(main_window, width=widths/1.3, height=heights/900*350, bg="#C5c5c5")

main_window.title("Gen Assembly Visualize Tool")

# Labels and text
main_label.pack()
text_input.place(x=20, y=heights/9)
example_label.place(x=20+int(widths / 3.0), y=heights / 9*4.0)



# Main window
main_window.minsize(width=widths, height=heights)
main_window.geometry("+200+100")

# Canvas
canvas.place(x=20, y=int(heights / 2.0))

main_window.mainloop()