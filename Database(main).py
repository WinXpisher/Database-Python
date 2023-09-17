from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import keyboard
import sqlite3
import os.path
from instruction_prog import Instruction_main

class Main():
    def __init__(self):
        self.window = Tk()
        w = int((self.window.winfo_screenwidth()) / 2)
        h = int((self.window.winfo_screenheight()) / 2)
        self.window.geometry(f'1200x240+400+200')
        self.window.title('Simple Data Base')
        self.window.resizable(False, False)
        self.tr(self.window)
        self.widgets(self.window)

    #Column
    def tr(self, root):
        self.columns = ('id', 'first_name', 'last_name', 'date_of_birth', 'email')
        self.tree = ttk.Treeview(root, columns = self.columns, show = 'headings')
        self.tree.heading('id', text = 'ID')
        self.tree.heading('first_name', text = 'First name')
        self.tree.heading('last_name', text = 'Last name')
        self.tree.heading('date_of_birth', text = 'Date of Birth')
        self.tree.heading('email', text = 'Email')
        self.tree.grid(row = 0, column = 0, padx = 170, sticky = 'nsew' )

        self.scr = ttk.Scrollbar(root, orient = 'vertical', command = self.tree.yview)
        self.tree.configure(yscrollcommand = self.scr.set)
        self.scr.place(x = 1176, y = 5, relheight = 0.94)
    #Interface
    def widgets(self, root):
        self.lab_id = Label(root, text = 'Number')
        self.ent_id = Entry(root)
        self.lab_f_n = Label(root, text = 'First_name')
        self.ent_f_n = Entry(root)
        self.lab_l_n = Label(root, text = 'Last_name')
        self.ent_l_n = Entry(root)
        self.lab_dob = Label(root, text = 'Date_of_birth(ex:23.02.91)')
        self.ent_dob = Entry(root)
        self.lab_em = Label(root, text = 'Email')
        self.ent_em = Entry(root)
        self.btn = Button(root, text = "Add", command = self.add)
        keyboard.add_hotkey('del', lambda: self.remove())
        keyboard.add_hotkey('Enter', lambda: self.showinfo())

        self.lab_id.place(x = 60)
        self.ent_id.place(x = 20, y = 20)
        self.lab_f_n.place(x = 60, y =40)
        self.ent_f_n.place(x = 20, y = 60)
        self.lab_l_n.place(x = 60, y = 80)
        self.ent_l_n.place(x = 20, y = 100)
        self.lab_dob.place(x = 10, y = 120)
        self.ent_dob.place(x = 20, y = 140)
        self.lab_em.place(x = 65, y = 160)
        self.ent_em.place(x = 20, y = 180)
        self.btn.place(x = 65, y = 201)
    #Logic Add
    def add(self, *args):
        try:
            self.id = int(self.ent_id.get())
            self.f_n = str(self.ent_f_n.get())
            self.l_n = str(self.ent_l_n.get())
            self.dob = str(self.ent_dob.get())
            self.em = str(self.ent_em.get())
            self.contacts = []
            self.contacts.append((f'{self.id}',f'{self.f_n}', f'{self.l_n}', f'{self.dob}', f'{self.em}'))

            for contact in self.contacts:
                self.tree.insert('', END, values = contact)

            BASE_DIR = os.path.dirname(os.path.abspath(__file__))
            db_path = os.path.join(BASE_DIR, "Database.sqlite")
            with sqlite3.connect(db_path) as db:
                cursor = db.cursor()
                datas = [(f'{self.id}', f'{self.f_n}', f'{self.l_n}', f'{self.dob}', f'{self.em}')]
                cursor.executemany("INSERT INTO albums VALUES(?,?,?,?,?)", datas)
                db.commit()
        except AttributeError and ValueError:
            return messagebox.showerror(title = 'Error', message = 'Дані некоректні, спробуйте ще раз!')
    #Logic Delete
    def remove(self):
        selected_items = self.tree.selection()        
        for selected_item in selected_items: 
            item = self.tree.item(selected_item)
            self.record = item['values']
            BASE_DIR = os.path.dirname(os.path.abspath(__file__))
            db_path = os.path.join(BASE_DIR, "Database.sqlite")
            with sqlite3.connect(db_path) as db:
                a = """DELETE FROM albums WHERE id = {record}""".format(record = self.record[0])
                cur = db.cursor()
                cur.execute(a)  
            self.tree.delete(selected_item)
            self.update() 
        return messagebox.showinfo(title = 'Info', message = 'Data was deleted!')
    #Logic Update info
    def update(self):
        d = []
        i = 1

        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(BASE_DIR, "Database.sqlite")
        with sqlite3.connect(db_path) as db:
            cur = db.cursor()
            for row in cur.execute('SELECT * FROM albums'):
                d.append(row)
            a = len(d)
            a += 1
            while i < a:
                i -= 1
                idq = d[i][0]
                i += 1
                up = """UPDATE albums SET id = {a} WHERE id = {id}""".format(a = i, id = idq)
                cur.execute(up)
                db.commit()
                i += 1 
    #Logic outout data
    def showinfo(self, *args):
        for selected_item in self.tree.selection():
            item = self.tree.item(selected_item)
            record = item['values']
            return messagebox.showinfo(title = 'Info', message=','.join(map(str, record)))
        self.add()
    #logic download data into sqllite3
    def upload(self):
        data = []

        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(BASE_DIR, "Database.sqlite")
        with sqlite3.connect(db_path) as db:
            cur = db.cursor()
            for row in cur.execute("SELECT * FROM albums"):
                self.tree.insert('', END, values = row)

    def run(self):
        
        self.upload()
        self.window.mainloop()

if __name__ == '__main__':
    Instruction_main().run()
    Main().run()
