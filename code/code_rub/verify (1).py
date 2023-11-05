import sqlite3
import tkinter as tk
from tkinter import messagebox

# Tạo hoặc kết nối cơ sở dữ liệu SQLite cho server
conn = sqlite3.connect("p2p_server.db")
cursor = conn.cursor()

# Tạo bảng lưu thông tin tài khoản và mật khẩu của các client
cursor.execute('''CREATE TABLE IF NOT EXISTS client_accounts
                  (id INTEGER PRIMARY KEY,
                   client_name TEXT,
                   password TEXT)''')

# Thêm tài khoản và mật khẩu của client vào cơ sở dữ liệu (chạy một lần)
cursor.execute("INSERT INTO client_accounts (client_name, password) VALUES (?, ?)", ("Alice", "123456"))
cursor.execute("INSERT INTO client_accounts (client_name, password) VALUES (?, ?)", ("Bob", "password123"))
conn.commit()


# Hàm kiểm tra tên và mật khẩu
def verify(hostname, password):
    cursor.execute("SELECT password FROM client_accounts WHERE client_name = ?", (hostname,))
    stored_password = cursor.fetchone()

    if stored_password is not None and stored_password[0] == password:
        return True
    else:
        return False

# Tạo ứng dụng GUI
app = tk.Tk()
app.title("P2P File Sharing Application")

# Giao diện người dùng
login_label = tk.Label(app, text="Login")
login_label.pack()

login_hostname_label = tk.Label(app, text="Client Name:")
login_hostname_label.pack()
login_hostname_entry = tk.Entry(app)
login_hostname_entry.pack()

login_password_label = tk.Label(app, text="Password:")
login_password_label.pack()
login_password_entry = tk.Entry(app, show="*")  # Để ẩn mật khẩu
login_password_entry.pack()

# Hàm xử lý đăng nhập
def login():
    hostname = login_hostname_entry.get()
    password = login_password_entry.get()

    if verify(hostname, password):
        messagebox.showinfo("Login Successful", f"Welcome, {hostname}!")
    else:
        messagebox.showerror("Login Failed", "Invalid username or password.")

login_button = tk.Button(app, text="Login", command=login)
login_button.pack()

app.mainloop()

# Đóng kết nối cơ sở dữ liệu
conn.close()
