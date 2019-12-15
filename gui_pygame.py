import template_matching as TM
from tkinter import *
from tkinter import messagebox, filedialog
import os


dir_path = os.path.dirname(os.path.realpath(__file__))
top = Tk()
top.geometry("500x500")
text = Text(top)
ftypes = [
    ('All files', '*'), 
]

def selectInput():
   inputPath = filedialog.askopenfilename(initialdir = dir_path,title = "Select file",filetypes = ftypes)
   text.insert(INSERT, inputPath)
   return inputPath

def selectTemplate():
   templatePath = filedialog.askopenfilename(initialdir = dir_path,title = "Select file",filetypes = ftypes)
   text.insert(END, templatePath)
   return templatePath

inputButton = Button(top, text = "Select input", command=selectInput)
templateButton = Button(top, text="Select template", command=selectTemplate)

inputButton.place(x = 50,y = 50)
templateButton.place(x = 150,y = 50)
top.mainloop()


