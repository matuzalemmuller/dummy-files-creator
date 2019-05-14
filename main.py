import webbrowser
import integer_entry
import files_creator
import tkinter as tkinter
from tkinter import Tk, Label, Entry, Button, Menu, messagebox

#------------------- Actions when buttons are clicked -------------------------#

def about_clicked():
    t = tkinter.Toplevel()
    t.wm_title("About")
    t.resizable(False, False)
    tfg_label = Label(t, text="2019 Test File Generator", font=("Arial", 12), 
                      padx=20, pady=3)
    tfg_label.pack()
    author_label = Label(t, text="by Mat Muller", font=("Arial", 12),
                         padx=20, pady=3)
    author_label.pack()
    version_label = Label(t, text="v1.0.0", font=("Arial", 12), padx=20, pady=3)
    version_label.pack()

    link = Label(t, text="https://git.io/fjWdz", fg="blue", cursor="hand2")
    link.pack()
    link.bind("<Button-1>", lambda event: webbrowser.open(link.cget("text")))

def create_clicked():
    files_creator.filesCreator()

def cancel_clicked():
    window.destroy()

#------------------------ Window and Help menu --------------------------------#

window = Tk()
window.title("Test Files Generator")
window.resizable(False, False)

menu = Menu(window) 
new_item = Menu(menu)
new_item.add_command(label='About', command=about_clicked)
menu.add_cascade(label='Help', menu=new_item)
window.config(menu=menu)

#-------------------------------- Path ----------------------------------------#

path_label = Label(window, text="Path", font=("Arial", 12), padx=20, pady=10)
path_label.grid(column=0, row=0)

path_entry = Entry(window, width=30)
path_entry.grid(column=1, row=0)

#-------------------------- Number of files -----------------------------------#

files_label = Label(window, text="Number of Files", font=("Arial", 12),
                    padx=20, pady=10)
files_label.grid(column=0, row=1)

files_entry = integer_entry.integerEntry(window, width=30)
files_entry.grid(column=1, row=1)

#---------------------------- Size of files -----------------------------------#

size_label = Label(window, text="Size of Files (MB)", font=("Arial", 12),
                   padx=20, pady=10)
size_label.grid(column=0, row=2)

size_entry = integer_entry.integerEntry(window, width=30)
size_entry.grid(column=1, row=2)

#------------------------- Create and Cancel ----------------------------------#

create_btn = Button(window, text="Create", command=create_clicked, padx=5)
create_btn.grid(column=0, row=3)

cancel_btn = Button(window, text="Cancel", command=cancel_clicked, padx=5)
cancel_btn.grid(column=1, row=3)

#-------------------- Right and bottom window spacing -------------------------#

space_bottom = Label(window, text="", font=("Arial", 2), padx=20)
space_bottom.grid(column=0, row=4)
space_right = Label(window, text="", font=("Arial", 2), padx=20)
space_right.grid(column=2, row=0)

#-----------------------------------------------------------------------------#

window.mainloop()