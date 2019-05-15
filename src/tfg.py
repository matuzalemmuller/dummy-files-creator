import webbrowser
import integer_entry
import files_creator
from tkinter import Button
from tkinter import Entry
from tkinter import filedialog
from tkinter import Frame
from tkinter import IntVar
from tkinter import Label
from tkinter import Menu
from tkinter import messagebox
from tkinter import StringVar
from tkinter import Tk
from tkinter import Toplevel
from tkinter import INSERT
from tkinter import END
from tkinter.ttk import Progressbar
from tkinter.ttk import Radiobutton

#-------------------------------- Progressbar ---------------------------------#

def progress_bar(Files):
    progress_frame = Frame(window)
    progress_frame.grid(row=1)

    progress_text = StringVar()
    progress_text.set("0/"+files_entry.get())

    progress_bar = Progressbar(progress_frame, orient="horizontal", length=500,
                              mode="determinate")
    progress_bar.config(value=0, maximum=int(files_entry.get()))
    progress_label = Label(progress_frame, textvariable=progress_text)

    progress_bar.grid(column=0)
    progress_label.grid(column=1)
    progress_bar.grid(column=1,row=3)

    while Files.created_files < int(files_entry.get()):
        if Files.errorFlag == 1:
            messagebox.showinfo("Error", "An error ocurred:" + \
                                str(Files.error) + \
                                "\nCheck if you have enough space and " + \
                                "permissions to write in the destination")
            break
        if not Files.is_running():
            progress_frame.destroy()
            return
        progress_text.set(str(Files.created_files)+"/"+files_entry.get())
        progress_bar.config(value=Files.created_files)
        progress_bar.update()

    if Files.errorFlag == 0:
        progress_text.set(str(Files.created_files)+"/"+files_entry.get())
        progress_bar.config(value=Files.created_files)
        progress_bar.update()
        messagebox.showinfo("Success!", "File(s) created!")

    progress_frame.destroy()

#------------------- Actions when buttons are clicked -------------------------#

def about_clicked():
    t = Toplevel()
    t.wm_title("About")
    t.resizable(False, False)
    tfg_label = Label(t, text="2019 Test File Generator", padx=20, pady=3)
    author_label = Label(t, text="by Mat Muller", padx=20, pady=3)
    version_label = Label(t, text="v1.0.0", padx=20, pady=3)
    link = Label(t, text="https://git.io/fjWdz", fg="blue", cursor="hand2")
    link.bind("<Button-1>", lambda event: webbrowser.open(link.cget("text")))
    tfg_label.pack()
    author_label.pack()
    version_label.pack()
    link.pack()

def widgets_status(status):
    path_entry.config(state=status)
    files_entry.config(state=status)
    size_entry.config(state=status)
    create_btn.config(state=status)
    browse_btn.config(state=status)
    size_kb_radio.config(state=status)
    size_mb_radio.config(state=status)
    size_gb_radio.config(state=status)

def close_clicked():
    window.destroy()

def cancel_clicked(Files):
    result = messagebox.askyesno(title="Confirmation",
                                 message="Are you sure?\nThe current file " + \
                                         "will still be created before " + \
                                         "the process is cancelled.")
    if result == True:
        Files.stop()

def create_clicked():
    if path_entry.get() == "" or \
       files_entry.get() == "" or \
       size_entry.get() == "":
        messagebox.showerror("Error", "You must fill all options!")
    else:
        Files = files_creator.filesCreator(path_entry.get(), files_entry.get(),
                                           size_entry.get(), size_unit.get())
        widgets_status('disabled')
        close_btn.config(text="Cancel", command=lambda: cancel_clicked(Files))
        progress_bar(Files)
        widgets_status('normal')
        close_btn.config(text="Close", command=close_clicked)

def browse_clicked():
    folder_path = filedialog.askdirectory()
    path_entry.delete(0, END)
    path_entry.insert(0, str(folder_path))

#------------------------ Window and Help menu --------------------------------#

window = Tk()
window.title("Test Files Generator")
window.resizable(False, False)

menu = Menu(window) 
new_item = Menu(menu, tearoff=False)
new_item.add_command(label='About', command=about_clicked)
menu.add_cascade(label='Help', menu=new_item)
window.config(menu=menu)

options_frame = Frame(window)
options_frame.grid(row=0)

#-------------------------------- Path ----------------------------------------#

path_label = Label(options_frame, text="Path", padx=20, pady=10)
path_entry = Entry(options_frame, width=30)
browse_btn = Button(options_frame, text="Browse", command=browse_clicked,
                    padx=10)

path_label.grid(column=0, row=0)
path_entry.grid(column=1, row=0)
browse_btn.grid(column=2, row=0)

#-------------------------- Number of files -----------------------------------#

files_label = Label(options_frame, text="Number of Files", padx=20, pady=10)
files_label.grid(column=0, row=1)

files_entry = integer_entry.integerEntry(options_frame, width=30)
files_entry.grid(column=1, row=1)

#---------------------------- Size of files -----------------------------------#

size_label = Label(options_frame, text="Size of File(s)", padx=20, pady=10)
size_entry = integer_entry.integerEntry(options_frame, width=30)
size_frame = Frame(options_frame)

size_label.grid(column=0, row=2)
size_entry.grid(column=1, row=2, padx=20)
size_frame.grid(column=2, row=2)

size_unit = IntVar()
size_unit.set(2)

size_kb_radio = Radiobutton(size_frame,variable=size_unit,text='KB',value=1)
size_mb_radio = Radiobutton(size_frame,variable=size_unit,text='MB',value=2)
size_gb_radio = Radiobutton(size_frame,variable=size_unit,text='GB',value=3)
size_kb_radio.grid(column=0, row=0)
size_mb_radio.grid(column=1, row=0)
size_gb_radio.grid(column=2, row=0)

#-------------------------- Create and Close ----------------------------------#

bottom_frame = Frame(options_frame)
bottom_frame.grid(column=1, row=4)

create_btn = Button(bottom_frame, text="Create", command=create_clicked, padx=5)
button_space = Label(bottom_frame, text="", font=("Arial", 2), padx=30)
close_btn = Button(bottom_frame, text="Close", command=close_clicked, padx=5)

create_btn.grid(column=0, row=0)
button_space.grid(column=1, row=0)
close_btn.grid(column=2, row=0)

#--------------------- Right and bottom frame spacing -------------------------#

space_bottom = Label(options_frame, text="", font=("Arial", 2), padx=20)
space_right = Label(options_frame, text="", font=("Arial", 2), padx=20)

space_bottom.grid(column=0, row=5)
space_right.grid(column=3, row=0)

#-----------------------------------------------------------------------------#

window.mainloop()