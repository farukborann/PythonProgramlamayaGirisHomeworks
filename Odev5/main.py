import sqlite3
import tkinter as tk
from tkinter import messagebox, filedialog
import algo1
import algo2

conn = sqlite3.connect('user_database.db')
cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                    username TEXT PRIMARY KEY,
                    password TEXT)''')

class Application(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("User Login")
        self.geometry("300x200")

        self.username_label = tk.Label(self, text="Username:")
        self.username_label.pack()
        self.username_entry = tk.Entry(self)
        self.username_entry.pack()

        self.password_label = tk.Label(self, text="Password:")
        self.password_label.pack()
        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.pack()

        self.login_button = tk.Button(self, text="Login", command=self.login)
        self.login_button.pack()

        self.register_button = tk.Button(self, text="Register", command=self.register)
        self.register_button.pack()

    def login(self):
        global username
        username = self.username_entry.get()
        password = self.password_entry.get()

        cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        user = cursor.fetchone()

        if user:
            self.open_menu()
        else:
            messagebox.showerror("Error", "Incorrect username or password!")

    def register(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        try:
            cursor.execute("INSERT INTO users VALUES (?, ?)", (username, password))
            conn.commit()
            messagebox.showinfo("Successful", "User successfully registered!")
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "This user already exists!")

    def open_menu(self):
        self.destroy()

        menu = Menu(self)
        menu.mainloop()

class Menu(tk.Tk):
    def __init__(self, parent):
        super().__init__()

        self.title("Menu")
        self.geometry("300x200")

        self.compare_button = tk.Button(self, text="Compare", command=self.compare_menu)
        self.compare_button.pack()

        self.operations_button = tk.Button(self, text="Operations", command=self.operations_menu)
        self.operations_button.pack()

        self.exit_button = tk.Button(self, text="Exit", command=self.exit)
        self.exit_button.pack()

    def compare_menu(self):
        compare_menu = CompareMenu(self)
        compare_menu.mainloop()

    def operations_menu(self):
        operations_menu = OperationsMenu(self)
        operations_menu.mainloop()

    def exit(self):
        conn.close()
        self.destroy()

class ChangePassword(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)

        self.title("Change Password")
        self.geometry("300x200")

        label_current_password = tk.Label(self, text="Current Password:")
        label_current_password.grid(row=0, column=0, padx=10, pady=5, sticky="e")
        self.entry_current_password = tk.Entry(self, show="*")
        self.entry_current_password.grid(row=0, column=1, padx=10, pady=5)

        label_new_password = tk.Label(self, text="New Password:")
        label_new_password.grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.entry_new_password = tk.Entry(self, show="*")
        self.entry_new_password.grid(row=1, column=1, padx=10, pady=5)

        button_change_password = tk.Button(self, text="Change Password", command=self.change_password)
        button_change_password.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

    def change_password(self):
        global username
        current_password = self.entry_current_password.get()
        new_password = self.entry_new_password.get()

        conn = sqlite3.connect('user_database.db')
        c = conn.cursor()
        
        c.execute("SELECT password FROM users WHERE username = ?", (username,))
        row = c.fetchone()
        if row is None:
            messagebox.showerror("Error", "User not found")
        elif row[0] != current_password:
            messagebox.showerror("Error", "Incorrect current password")
        else:
            c.execute("UPDATE users SET password = ? WHERE username = ?", (new_password, username))
            conn.commit()
            messagebox.showinfo("Success", "Password successfully changed")
        
        conn.close()

class CompareMenu(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        
        self.title("Text Comparison")
        self.geometry("400x300")

        self.file1_label = tk.Label(self, text="File 1:")
        self.file1_label.grid(row=0, column=0, padx=5, pady=5)

        self.file1_entry = tk.Entry(self)
        self.file1_entry.grid(row=0, column=1, padx=5, pady=5)

        self.file1_select_button = tk.Button(self, text="Select File", command=self.select_file1)
        self.file1_select_button.grid(row=0, column=2, padx=5, pady=5)

        self.file2_label = tk.Label(self, text="File 2:")
        self.file2_label.grid(row=1, column=0, padx=5, pady=5)

        self.file2_entry = tk.Entry(self)
        self.file2_entry.grid(row=1, column=1, padx=5, pady=5)

        self.file2_select_button = tk.Button(self, text="Select File", command=self.select_file2)
        self.file2_select_button.grid(row=1, column=2, padx=5, pady=5)

        self.result_label = tk.Label(self, text="")
        self.result_label.grid(row=2, column=1, padx=5, pady=5)

        self.compare_button_A = tk.Button(self, text="Compare Using Algorithm A", command=self.compareA)
        self.compare_button_A.grid(row=3, column=1, padx=5, pady=5)
        self.compare_button_B = tk.Button(self, text="Compare Using Algorithm B", command=self.compareB)
        self.compare_button_B.grid(row=3, column=2, padx=5, pady=5)

    def select_file1(self):
        global file1
        file1 = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        self.file1_entry.delete(0, tk.END)
        self.file1_entry.insert(0, file1.split("/")[-1])

    def select_file2(self):
        global file2
        file2 = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        self.file2_entry.delete(0, tk.END)
        self.file2_entry.insert(0, file2.split("/")[-1])

    def compareA(self):
        global file1, file2
        with open(file1, 'r') as file:
            text1 = file.read()

        with open(file2, 'r') as file:
            text2 = file.read()    

        result = algo1.text_similarity(text1, text2)
        self.result_label.config(text=result)

    def compareB(self):
        global file1, file2
        with open(file1, 'r') as file:
            text1 = file.read()

        with open(file2, 'r') as file:
            text2 = file.read()    
        
        similarity_score = algo2.text_similarity(text1, text2)
        self.result_label.config(text=similarity_score)

class OperationsMenu(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)

        self.title("Operations")
        self.geometry("300x200")

        self.password_button = tk.Button(self, text="Change Password", command=self.change_password_screen)
        self.password_button.pack()

    def change_password_screen(self):
        change_password_screen = ChangePassword(self)
        change_password_screen.mainloop()
        
app = Application()
app.mainloop()
