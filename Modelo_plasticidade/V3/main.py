from tkinter import *
from tkinter.ttk import Combobox
import hardening as hd

class Application:
    def __init__(self):
        self.window = Tk()
        self.window.title('FEA Helper')
        self.window.geometry('300x600+10+20')
        
        Application.Models(self)
        Application.Variables(self)
        self.window.mainloop()
        
    def Models(self):
        self.lab1    = Label(self.window, text = 'Modelo de plasticidade:',fg = 'Black')
        self.lab1.place(x=40, y = 20)
        self.m0=IntVar()
        self.m1=IntVar()
        self.r0 = Checkbutton(self.window,text='Bilinear',variable = self.m0)
        self.r1 = Checkbutton(self.window,text='Multilinear',variable = self.m1)
        self.r0.place(x = 30, y = 45)
        self.r1.place(x = 110, y = 45)

    def Variables(self):
        self.lab2    = Label(self.window, text = 'E [MPa]:',fg = 'Black')
        self.lab2.place(x=40, y = 70)
        self.E_entry = Entry(width=10)
        self.E_entry.place(x=120, y = 70)

        self.lab3    = Label(self.window, text = 'Sut [MPa]:',fg = 'Black')
        self.lab3.place(x=40, y = 95)
        self.E_entry = Entry(width = 10)
        self.E_entry.place(x=120, y = 95)

        self.lab4    = Label(self.window, text = 'Sy [MPa]:',fg = 'Black')
        self.lab4.place(x=40, y = 120)
        self.Sy_entry = Entry(width = 10)
        self.Sy_entry.place(x=120, y = 120)

        self.lab5    = Label(self.window, text = 'v [-]:',fg = 'Black')
        self.lab5.place(x=40, y = 145)
        self.v_entry = Entry(width = 10)
        self.v_entry.place(x=120, y = 145)
        

root = Application()