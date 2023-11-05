import sqlite3
import tkinter as tk
from tkinter import messagebox

# Kết nối hoặc tạo cơ sở dữ liệu SQLite
conn = sqlite3.connect("p2p_server.db")
cursor = conn.cursor()

# Tạo hoặc kết nối các bảng dữ liệu
cursor.execute('''CREATE TABLE IF NOT EXISTS server_info
                  (id INTEGER PRIMARY KEY,
                   server_ip TEXT,
                   server_ports TEXT)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS clients
                  (id INTEGER PRIMARY KEY,
                   client_name TEXT,
                   client_ip TEXT,
                   client_port INTEGER)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS shared_files
                  (id INTEGER PRIMARY KEY,
                   client_id INTEGER,
                   file_name TEXT)''')

# Hàm thêm thông tin tệp vào cơ sở dữ liệu
def add_file(hostname, lname, fname):
    cursor.execute("SELECT id FROM clients WHERE client_name = ?", (hostname,))
    client_id = cursor.fetchone()
    
    if client_id is not None:
        cursor.execute("INSERT INTO shared_files (client_id, file_name) VALUES (?, ?)", (client_id[0], fname))
        conn.commit()
        messagebox.showinfo("File Published", f"{hostname} published the file '{fname}'.")
    else:
        messagebox.showerror("Error", f"Client '{hostname}' does not exist.")

# Tạo ứng dụng GUI
app = tk.Tk()
app.title("P2P File Sharing Application")

# Tạo giao diện người dùng
publish_file_label = tk.Label(app, text="Publish a File")
publish_file_label.pack()

publish_hostname_label = tk.Label(app, text="Client Name:")
publish_hostname_label.pack()
publish_hostname_entry = tk.Entry(app)
publish_hostname_entry.pack()

publish_fname_label = tk.Label(app, text="File Name:")
publish_fname_label.pack()
publish_fname_entry = tk.Entry(app)
publish_fname_entry.pack()

def publish_file():
    hostname = publish_hostname_entry.get()
    fname = publish_fname_entry.get()
    lname = "path/to/your/file"  # Đường dẫn đến tệp
    
    add_file(hostname, lname, fname)

publish_file_button = tk.Button(app, text="Publish File", command=publish_file)
publish_file_button.pack()

# Khám phá tệp và các phần giao diện khác có thể được thêm ở đây

app.mainloop()

# Đóng kết nối cơ sở dữ liệu
conn.close()
