from tkinter import *
from tkinter import ttk
from tkinter import messagebox

class Instruction_main():
    def __init__(self):
        self.instructWindow = Tk()
        self.instructWindow.geometry(f'300x400+400+200')
        self.instructWindow.title('Instruction of program')
        self.instructWindow.resizable(False, False)
        self.text(self.instructWindow)

    def text(self, root):
        self.lab_t1 = Label(root, text = 'Instruction of program:', font = ('', 14))
        self.lab_t2 = Label(root, text = '1.Add info press Enter\n or button Add', font = ('', 14))
        self.lab_t3 = Label(root, text = '2.Delete press Del', font = ('', 14))

        self.lab_t1.place(x = 10)
        self.lab_t2.place(x = 10, y = 40)
        self.lab_t3.place(x = 10, y = 85)
    
    def run(self):
        self.instructWindow.mainloop()

if __name__ == '__main__':
    Instruction_main().run()
