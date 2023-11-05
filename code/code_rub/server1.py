import socket

# Tạo socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Xác định địa chỉ và cổng của máy chủ
server_ip = "172.16.13.104"  # Địa chỉ IP của máy chủ
server_port = 12345  # Cổng của máy chủ

# Liên kết máy chủ với địa chỉ và cổng
server_socket.bind((server_ip, server_port))

# Lắng nghe kết nối từ máy khách
server_socket.listen()

print(f"Listening on {host}:{port}")

# Chấp nhận kết nối từ máy khách
client_socket, client_address = server_socket.accept()

# Nhận dữ liệu từ máy khách
request_data = client_socket.recv(1024)

#Hàm respond
def respond(client_socket, status_code, name):
    response_data = status_code.to_bytes(2, byteorder='big') + name.encode()
    client_socket.send(response_data)
    client_socket.close()


# ------------- Phân tích request---------------------
request_type = request_data[0:1]  # 1 byte kiểu request

# ------------Xử lý request----------------------
if request_type == b'\x01':
    username_length = request_data[1:2]
    username = request_data[2:2 + username_length].decode()
    userpass = request_data[2 + username_length:].decode()
    if username == "your_username" and user_pass == "your_password":
        respond(client_socket, 200, "OK")
    elif username == None:
        respond(client_socket, 401, "NAME_ERROR")
    elif user_pass == None:
        respond(client_socket, 402, "PASS_ERROR")
        
elif request_type == b'\x02':
    username_length = request_data[1:2]
    userpass_length = request_data[2:3]
    username = request_data[3:3+username_length].decode()
    userpass = request_data[3+username_length:3+username_length+userpass_length].decode()
    confirmpass = request_data[3+username_length+userpass_length:].decode()
    if username == "another name":
        respond(client_socket, 401, "NAME_ERROR")
    elif userpass != confirmpass:
        respond(client_socket, 402, "PASS_ERROR")
    else:
        respond(client_socket, 200, "OK")
        
elif request_type == b'\x03':
    username_length = request_data[1:2]
    username = request_data[2:].decode()
    
elif request_type == b'\x04':
    fname_length = request_data[1:2]
    fname = request_data[2:].decode()
    #### Hàm respond
    if fname == "Không tìm thấy file":
        respond(client_socket, 401, "NAME_ERROR")
    elif fname == "Không tìm thấy host":
        respond(client_socket, 403, "NOT_FOUND_HOST_AVAILABLE")

elif request_type == b'\x05':
    hostname_length = request_data[1:2]
    fname_length = request_data[2:3]
    hostname = request_data[3:3+hostname_length].decode()
    fname = request_data[3+hostname_length:].decode()
    
    respond(client_socket, 200, "OK")
    
elif request_type == b'\x06':
    lname_length = request_data[1:2]
    lname = request_data[2:2+lname_length].decode()
    fname = request_data[2+lname_length:]()
    
    respond(client_socket, 200, "OK")
    
elif request_type == b'\x07':
    request_message = request_data[1:].decode()
    if request_message == "Hi":
        respond(client_socket, 200, "OK")

else:
    respond(client_socket, 410, "Unknown request")


# Đóng kết nối
client_socket.close()
