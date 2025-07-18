import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3

def setup_database():
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def save_data_to_db():
    status_label.config(text="")
    
    name = name_entry.get()
    email = email_entry.get()

    if not name or not email:
        messagebox.showwarning("Input error", "Neither the name nor the email address can be empty！")
        return

    try:
        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()
        sql_command = "INSERT INTO users (name, email) VALUES (?, ?)"
        cursor.execute(sql_command, (name, email))
        conn.commit()
        conn.close()

        name_entry.delete(0, tk.END)
        email_entry.delete(0, tk.END)
        name_entry.focus_set() 
        
        status_label.config(text="The data has been successfully saved to the database data.db", foreground="green")

    except sqlite3.Error as e:
        messagebox.showerror("Database saving failed", f"A database error occurred\n{e}")

def on_enter_key(event):
    save_data_to_db()

window = tk.Tk()
window.title("Data entry")
window.geometry("450x280") 
window.resizable(False, False)
window.configure(bg='#f0f0f0')

window.bind('<Return>', on_enter_key)

style = ttk.Style(window)
if 'vista' in style.theme_names():
    style.theme_use('vista') 
else:
    style.theme_use('clam')

style.configure('TLabel', background='#f0f0f0', foreground='#333', font=('Segoe UI', 11))
style.configure('TEntry', font=('Segoe UI', 11))
style.configure('TButton', font=('Segoe UI', 12, 'bold'), borderwidth=0)
style.configure('Status.TLabel', background='#f0f0f0', font=('Segoe UI', 10))

style.map('TButton',
    foreground=[('pressed', 'white'), ('active', 'white')],
    background=[('pressed', '!disabled', '#0056b3'), ('active', '#0069d9')]
)

main_frame = ttk.Frame(window, padding="20 20 20 20", style='TFrame')
main_frame.pack(expand=True, fill="both")
style.configure('TFrame', background='#f0f0f0')

name_label = ttk.Label(main_frame, text="name:")
name_label.grid(row=0, column=0, sticky="w", padx=5, pady=10)

name_entry = ttk.Entry(main_frame, width=35)
name_entry.grid(row=0, column=1, sticky="ew", padx=5, pady=10)

email_label = ttk.Label(main_frame, text="Email:")
email_label.grid(row=1, column=0, sticky="w", padx=5, pady=10)

email_entry = ttk.Entry(main_frame, width=35)
email_entry.grid(row=1, column=1, sticky="ew", padx=5, pady=10)

button_frame = ttk.Frame(main_frame, style='TFrame')
button_frame.grid(row=2, column=0, columnspan=2, pady=(20, 0), sticky="ew")

save_button = ttk.Button(
    button_frame,
    text="Save data",
    command=save_data_to_db,
    style='TButton',
    cursor="hand2"
)
save_button.pack(expand=True, fill='x', ipady=5)

status_label = ttk.Label(main_frame, text="", style='Status.TLabel', anchor='center')
status_label.grid(row=3, column=0, columnspan=2, pady=(10, 0), sticky="ew")

main_frame.columnconfigure(1, weight=1)

setup_database()
window.mainloop()
