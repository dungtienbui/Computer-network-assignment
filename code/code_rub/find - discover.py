import sqlite3
import tkinter as tk
from tkinter import messagebox

# Tạo hoặc kết nối cơ sở dữ liệu
conn = sqlite3.connect("p2p_server.db")
cursor = conn.cursor()

# Tạo bảng lưu thông tin của server
cursor.execute('''CREATE TABLE IF NOT EXISTS server_info
                  (id INTEGER PRIMARY KEY,
                   server_ip TEXT,
                   server_ports TEXT)''')

# Tạo bảng lưu danh sách tên các client
cursor.execute('''CREATE TABLE IF NOT EXISTS clients
                  (id INTEGER PRIMARY KEY,
                   client_name TEXT,
                   client_ip TEXT,
                   client_port INTEGER)''')

# Tạo bảng lưu danh sách các tệp mà mỗi client chia sẻ
cursor.execute('''CREATE TABLE IF NOT EXISTS shared_files
                  (id INTEGER PRIMARY KEY,
                   client_id INTEGER,
                   file_name TEXT)''')

# Tạo giao diện người dùng
app = tk.Tk()
app.title("P2P File Sharing Application")

def add_server_info():
    server_ip = server_ip_entry.get()
    server_ports = server_ports_entry.get()
    cursor.execute("INSERT INTO server_info (server_ip, server_ports) VALUES (?, ?)", (server_ip, server_ports))
    conn.commit()
    messagebox.showinfo("Server Info", "Server Info added successfully!")

def add_client_info():
    client_name = client_name_entry.get()
    client_ip = client_ip_entry.get()
    client_port = client_port_entry.get()
    cursor.execute("INSERT INTO clients (client_name, client_ip, client_port) VALUES (?, ?, ?)", (client_name, client_ip, client_port))
    conn.commit()
    messagebox.showinfo("Client Info", "Client Info added successfully!")

def add_shared_file():
    client_id = shared_file_client_id_entry.get()
    file_name = shared_file_name_entry.get()
    cursor.execute("INSERT INTO shared_files (client_id, file_name) VALUES (?, ?)", (client_id, file_name))
    conn.commit()
    messagebox.showinfo("Shared File", "Shared File added successfully!")

server_info_label = tk.Label(app, text="Server Info")
server_info_label.pack()
server_ip_label = tk.Label(app, text="Server IP:")
server_ip_label.pack()
server_ip_entry = tk.Entry(app)
server_ip_entry.pack()
server_ports_label = tk.Label(app, text="Server Ports:")
server_ports_label.pack()
server_ports_entry = tk.Entry(app)
server_ports_entry.pack()
add_server_button = tk.Button(app, text="Add Server Info", command=add_server_info)
add_server_button.pack()

client_info_label = tk.Label(app, text="Client Info")
client_info_label.pack()
client_name_label = tk.Label(app, text="Client Name:")
client_name_label.pack()
client_name_entry = tk.Entry(app)
client_name_entry.pack()
client_ip_label = tk.Label(app, text="Client IP:")
client_ip_label.pack()
client_ip_entry = tk.Entry(app)
client_ip_entry.pack()
client_port_label = tk.Label(app, text="Client Port:")
client_port_label.pack()
client_port_entry = tk.Entry(app)
client_port_entry.pack()
add_client_button = tk.Button(app, text="Add Client Info", command=add_client_info)
add_client_button.pack()

shared_file_label = tk.Label(app, text="Shared Files")
shared_file_label.pack()
shared_file_client_id_label = tk.Label(app, text="Client ID:")
shared_file_client_id_label.pack()
shared_file_client_id_entry = tk.Entry(app)
shared_file_client_id_entry.pack()
shared_file_name_label = tk.Label(app, text="File Name:")
shared_file_name_label.pack()
shared_file_name_entry = tk.Entry(app)
shared_file_name_entry.pack()
add_shared_file_button = tk.Button(app, text="Add Shared File", command=add_shared_file)
add_shared_file_button.pack()



def find_hosts_sharing_file(file_name):
    cursor.execute("SELECT client_name FROM clients WHERE id IN (SELECT client_id FROM shared_files WHERE file_name = ?)", (file_name,))
    hosts = cursor.fetchall()
    host_list = [host[0] for host in hosts]
    return host_list

def discover_shared_files(host_name):
    cursor.execute("SELECT file_name FROM shared_files WHERE client_id = (SELECT id FROM clients WHERE client_name = ?)", (host_name,))
    files = cursor.fetchall()
    file_list = [file[0] for file in files]
    return file_list

def search_file():
    file_name = search_file_entry.get()
    hosts_sharing_file = find_hosts_sharing_file(file_name)
    if hosts_sharing_file:
        message = f"The file '{file_name}' is shared by the following hosts: {', '.join(hosts_sharing_file)}"
    else:
        message = f"The file '{file_name}' is not shared by any host."
    messagebox.showinfo("File Search Result", message)

def discover_files():
    host_name = discover_files_entry.get()
    shared_files = discover_shared_files(host_name)
    if shared_files:
        message = f"{host_name} shares the following files: {', '.join(shared_files)}"
    else:
        message = f"{host_name} is not sharing any files."
    messagebox.showinfo("Shared Files", message)

search_file_label = tk.Label(app, text="Search for a file")
search_file_label.pack()
search_file_entry = tk.Entry(app)
search_file_entry.pack()
search_file_button = tk.Button(app, text="Search", command=search_file)
search_file_button.pack()

discover_files_label = tk.Label(app, text="Discover Files of a Host")
discover_files_label.pack()
discover_files_entry = tk.Entry(app)
discover_files_entry.pack()
discover_files_button = tk.Button(app, text="Discover", command=discover_files)
discover_files_button.pack()

app.mainloop()

# Đóng kết nối cơ sở dữ liệu
conn.close()
