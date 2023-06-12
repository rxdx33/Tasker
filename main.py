import tkinter
import customtkinter
from tkinter import *
from tkinter import messagebox
import os

# TODO
# add word wrapping or worst case, sideways scroll bar?
# fix save and load functionality causing order to be reversed after closing and reopening app

def addTask(event=None):
    task = taskEntry.get()
    if task:
        tasksList.insert(0, task)
        taskEntry.delete(0, END)
        saveTasks()
    else:
        messagebox.showerror("Error", "Please enter a task.")

def removeTask(event=None):
    selected = tasksList.curselection()
    if selected:
        with open("taskerCompleted.txt", "a") as f:
            f.write(tasksList.get(selected[0]) + "\n")
        tasksList.delete(selected[0])
        saveTasks()
    else:
        messagebox.showerror("Error", "Please choose a task to delete.")

def removeAllTasks():
    if tasksList.get(0):
        res = messagebox.askquestion("Remove All Tasks", "Are you sure you want to delete all tasks?")
        if res == "yes":
            tasksList.delete(0, END)
            saveTasks()
        else:
            pass
    else:
        messagebox.showerror("Error", "No tasks to delete.")

def removeCompTasks():
    if os.path.exists("taskerCompleted.txt"):
        res = messagebox.askquestion("Remove Completed All Tasks", "Are you sure you want to delete all completed tasks?")
        if res == "yes":
            os.remove("taskerCompleted.txt")
            saveTasks()
        else:
            pass
    else:
        messagebox.showerror("Error", "No completed tasks to delete.")

def saveTasks():
    with open("taskerActive.txt", "w") as f:
        tasks = tasksList.get(0,END)
        for task in tasks:
            f.write(task + "\n")

def loadTasks():
    try:
        with open("taskerActive.txt", "r") as f:
            tasks = f.readlines()
            for task in tasks:
                tasksList.insert(0, task.strip())
    except FileNotFoundError:
        # If no file exists, make one
        with open("taskerActive.txt", "w"): 
            pass

def loadCompTasks():
    try:
        with open("taskerCompleted.txt", "r") as f:
            completed = f.read()
            if completed:
                messagebox.showinfo("Completed Items", completed)
    except FileNotFoundError:
        messagebox.showerror("Error", "No completed items found.")

def on_footer_click(event):
    global clickState

    if clickState == 0:
        footer.configure(text="MADE BY RADOS NIKACEVIC")
        clickState = 1
    elif clickState == 1:
        footer.configure(text="Made by Rados Nikacevic")
        clickState = 0

# setup
app = customtkinter.CTk()
app.geometry("365x610")
app.title("Rados' To Do List")
#app.config(bg="#252526")
customtkinter.set_appearance_mode("dark")
app.resizable(False, False)

font1 = ('System', 50, 'bold')
font2 = ('System', 18, 'bold')
font3 = ('System', 16, 'bold')

def change_appearance_mode_event(new_appearance_mode: str):
    customtkinter.set_appearance_mode(new_appearance_mode)

def sidebar_button_event():
    print("sidebar_button click")

# frame 1
titleLabel = customtkinter.CTkLabel(app, font=font1, text='TO DO', text_color='#fff')
titleLabel.place(x=100, y=20)

addButton = customtkinter.CTkButton(app, command=addTask, font=font2,text='Add Task', text_color='#fff', fg_color='#06911f', hover_color='#005E00', cursor='hand2', corner_radius=5, width=120)
addButton.place(x=40, y=110)

removeButton = customtkinter.CTkButton(app, command=removeTask, font=font2, text='Delete Task', text_color='#fff', fg_color='#96061c', hover_color='#630000', cursor='hand2', corner_radius=5, width=120)
removeButton.place(x=200, y=110)

taskEntry = customtkinter.CTkEntry(app, font=font2, text_color='#000', fg_color='#fff', width=280, placeholder_text="Enter task...")
taskEntry.pack()
taskEntry.place(x=40, y=150)
taskEntry.bind("<Return>", addTask)

tasksList = Listbox(app, width=40, height=15, font=font3)
tasksList.place(x=20, y=210)
tasksList.bind("<Delete>", removeTask)
tasksList.bind("<BackSpace>", removeTask)

removeAllButton = customtkinter.CTkButton(app, command=removeAllTasks, font=font2,text='Delete All Tasks', text_color='#fff', fg_color='#96061c', hover_color='#630000', cursor='hand2', corner_radius=5, width=120)
removeAllButton.place(x=200, y=490)

showCompButton = customtkinter.CTkButton(app, command=loadCompTasks, font=font2,text='Show Completed', text_color='#fff', fg_color='#358af3', hover_color='#0257C0', cursor='hand2', corner_radius=5, width=120)
showCompButton.place(x=40, y=490)

clearCompButton = customtkinter.CTkButton(app, command=removeCompTasks, font=font2,text='Delete Completed', text_color='#fff', fg_color='#96061c', hover_color='#630000', cursor='hand2', corner_radius=5, width=120)
clearCompButton.place(x=40, y=530)

clickState = 0
footer = customtkinter.CTkLabel(app, font=font3, text='Made by Rados Nikacevic', text_color='#6CE553')
footer.pack()
footer.bind("<Button-1>", on_footer_click)
footer.place(x=100, y=580)

loadTasks()


# run
app.mainloop()