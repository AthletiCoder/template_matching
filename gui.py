import template_matching as TM
from tkinter import *
from tkinter import messagebox, filedialog

top = Tk()
top.geometry("500x500")
text = Text(top)

ftypes = [
    ('All files', '*'), 
]

def selectInput():
   inputPath = filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = ftypes)
   print(inputPath)
   text.insert(INSERT, inputPath)

def selectTemplate():
   templatePath = filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = ftypes)
   text.insert(END, templatePath)

inputButton = Button(top, text = "Select input", command=selectInput)
templateButton = Button(top, text="Select template", command=selectTemplate)

inputButton.place(x = 50,y = 50)
templateButton.place(x = 150,y = 50)
top.mainloop()


