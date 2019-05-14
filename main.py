import webbrowser
import integer_entry
import files_creator
from tkinter import Button
from tkinter import Entry
from tkinter import filedialog
from tkinter import Frame
from tkinter import Label
from tkinter import Menu
from tkinter import messagebox
from tkinter import StringVar
from tkinter import Tk
from tkinter import Toplevel
from tkinter import INSERT
from tkinter import END
from tkinter.ttk import Radiobutton

#------------------- Actions when buttons are clicked -------------------------#

def about_clicked():
    t = Toplevel()
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
    if path_entry.get() == "" or \
       files_entry.get() == "" or \
       size_entry.get() == "":
        messagebox.showerror("Error", "You must fill all options!")
    else:
        files_creator.filesCreator(path_entry.get(), files_entry.get(),
                                size_entry.get(), size_unit.get())

def cancel_clicked():
    window.destroy()

def browse_clicked():
    folder_path = filedialog.askdirectory()
    path_entry.delete(0, END)
    path_entry.insert(0, str(folder_path))

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

browse_btn = Button(window, text="Browse", command=browse_clicked, padx=10)
browse_btn.grid(column=2, row=0)

#-------------------------- Number of files -----------------------------------#

files_label = Label(window, text="Number of Files", font=("Arial", 12),
                    padx=20, pady=10)
files_label.grid(column=0, row=1)

files_entry = integer_entry.integerEntry(window, width=30)
files_entry.grid(column=1, row=1)

#---------------------------- Size of files -----------------------------------#

size_label = Label(window, text="Size of Files", font=("Arial", 12),
                   padx=20, pady=10)
size_label.grid(column=0, row=2)

size_entry = integer_entry.integerEntry(window, width=30)
size_entry.grid(column=1, row=2, padx=20)

size_frame = Frame(window)
size_frame.grid(column=2, row=2)

size_unit = StringVar()
size_unit.set('MB')

size_kb_radio = Radiobutton(size_frame,variable=size_unit,text='KB',value='KB')
size_mb_radio = Radiobutton(size_frame,variable=size_unit,text='MB',value='MB')
size_gb_radio = Radiobutton(size_frame,variable=size_unit,text='GB',value='GB')
size_kb_radio.grid(column=0, row=0)
size_mb_radio.grid(column=1, row=0)
size_gb_radio.grid(column=2, row=0)

#------------------------- Create and Cancel ----------------------------------#

bottom_frame = Frame(window)
bottom_frame.grid(column=1, row=3)

create_btn = Button(bottom_frame, text="Create", command=create_clicked, padx=5)
create_btn.grid(column=0, row=0)

button_space = Label(bottom_frame, text="", font=("Arial", 2), padx=30)
button_space.grid(column=1, row=0)

cancel_btn = Button(bottom_frame, text="Cancel", command=cancel_clicked, padx=5)
cancel_btn.grid(column=2, row=0)

#-------------------- Right and bottom window spacing -------------------------#

space_bottom = Label(window, text="", font=("Arial", 2), padx=20)
space_bottom.grid(column=0, row=4)
space_right = Label(window, text="", font=("Arial", 2), padx=20)
space_right.grid(column=3, row=0)

#-----------------------------------------------------------------------------#

window.mainloop()