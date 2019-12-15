from tkinter import *
from tkinter import messagebox, filedialog
import os
import tkinter as tk
from template_matching import match_template

dir_path = os.path.dirname(os.path.realpath(__file__))

ftypes = [
    ('All files', '*'), 
]

input_path = None
input_entry = None
inputVar = None

template_path = None
template_entry = None
templateVar = None

visVar = None

def init_gui():
   top = Tk()
   top.geometry("600x300")
   top.resizable(0,0)
   global input_path, input_entry, inputVar, template_path, template_entry, templateVar, visVar
   # heading
   heading = Label(top, text="Template Matching")
   heading.place(x=140,y=0)
   heading.config(font=('Roboto',27,'bold'))

   # input related
   inputButton = Button(top, text = "Select input", command=selectInput)
   inputButton.place(x = 50,y = 50)
   input_label = Label(top, text="Input path")
   input_label.place(x=10,y=100)
   inputVar = StringVar()
   input_entry = Label(top, textvariable=inputVar)
   input_entry.place(x=135,y=100)
   input_entry.config(borderwidth=5)

   # template related
   templateButton = Button(top, text="Select template", command=selectTemplate)
   templateButton.place(x = 150,y = 50)
   template_label = Label(top, text="Template Directory")
   template_label.place(x=10,y=150)
   templateVar = StringVar()
   template_entry = Label(top, textvariable=templateVar)
   template_entry.place(x=135,y=150)
   template_entry.config(highlightbackground='black')

   # visualize checkbutton
   visVar = IntVar()
   visualizeBtn = Checkbutton(top, text = "Visualize", variable = visVar, onvalue = 1, offvalue = 0)
   visualizeBtn.place(x=300,y=50)

   # run button
   run = Button(top, text="Run", command=run_match_template)
   run.place(x=200,y=200)


   return top

def selectInput():
   global input_path
   input_path = filedialog.askopenfilename(initialdir = dir_path,title = "Select file", filetypes = ftypes)
   inputVar.set(input_path)

def selectTemplate():
   global template_path
   template_path = filedialog.askdirectory(initialdir = dir_path,title = "Select templates folder")
   templateVar.set(template_path)

def run_match_template():
   args = {
      "templates":template_path,
      "inputpath":input_path,
      "visualize":visVar.get()
   }
   err = match_template(args)
   if err:
      messagebox.showerror("Error", err)
   elif visVar.get():
      messagebox.showinfo("Information", "Check for results in resutls.csv and the results folder")
   elif not visVar.get():
      messagebox.showinfo("Information", "Check for results in results.csv")

if __name__=="__main__":
   app = init_gui()
   app.mainloop()
