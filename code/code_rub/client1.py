import socket
import socket.timeout


# Tạo socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Xác định địa chỉ và cổng của máy chủ
server_ip = "172.16.13.104"  # Địa chỉ IP của máy chủ
server_port = 12345  # Cổng của máy chủ

# Kết nối đến máy chủ
client_socket.connect((server_ip, server_port))


def get_status_code(response_data):
    # if len(response_data) >= 2:
    #     # Chuyển 2 byte đầu tiên thành số nguyên
    #     status_code = int.from_bytes(response_data[:2], byteorder='big')
    #     return status_code
    # return None
    status_code = int.from_bytes(response_data[:2], byteorder='big')
    if (status_code > 600 or status_code < 100):
        return None
    else:
        return status_code


def Login(name, password):
    request_type = bytes([1])
    username = name.encode()
    userpass = password.encode()
    username_length = bytes([len(username)])
    request_data = request_type + username_length + username + userpass    
    client_socket.send(request_data)
        
    response_data = client_socket.recv(1024)
    status_code = get_status_code(response_data)        
    if status_code == 200:
        return "Đăng nhập thành công"
    elif status_code == 401:
        return "Tên đăng nhập không tồn tại"
    elif status_code == 402:
        return "Mật khẩu không chính xác"
    else:
        return "Lỗi phát sinh > <"
    
def Signup(name, password, confirm):
    request_type = bytes([2])
    username = name.encode()
    userpass = password.encode()
    confirmpass = confirm.encode()
    username_length = bytes([len(username)])
    userpass_length = bytes([len(userpass)])
    request_data = request_type + username_length + userpass_length + username + userpass + confirmpass
    
    client_socket.send(request_data)
    
    
    response_data = client_socket.recv(1024)
    status_code = get_status_code(response_data)        
    if status_code == 200:
        return "Dang ky thanh cong"
    elif status_code == 401:
        return "Ten da ton tai"
    elif status_code == 402:
        return "Mat khau xac nhan khong dung"
    else:
        return "Loi phat sinh > <"
    
def Logout(username):
    request_type = bytes([3])
    username = username.encode()
    username_length = bytes([len(username)])    
    request_data = request_type + username_length + username
    client_socket.send(request_data)
    
    
    
def fetch(fname_user):
    request_type = bytes([4])
    fname = fname_user.encode()
    fname_length = bytes([len(fname)])  
    request_data = request_type + fname_length + fname   
    client_socket.send(request_data)
    
    response_data = client_socket.recv(1024)
    status_code = get_status_code(response_data)    
    if status_code == 200:
        return "Tải thành công"
    elif status_code == 401:
        return "Không tìm thấy file"
    elif status_code == 402:
        return  "Không tìm thấy host"
    else:
        return "Lỗi phát sinh > <"

def Xoafile_fname(hostname_user, fname_user):
    request_type = bytes([5])
    hostname = hostname_user.encode()
    fname = fname_user.encode()
    hostname_length = bytes([len(hostname_bytes)])
    fname_length = bytes([len(fname_bytes)])
        
    request_data = request_type + hostname_length + fname_length + hostname + fname
        
    client_socket.send(request_data)
        
    response = client_socket.recv(1024)
    status_code = get_status_code(response_data)        
    if status_code == 200:
        return "Xóa thành công"
    else:
        return "ERROR!"  

def publish(lname_user, fname_user):
    request_type = bytes([6])
    lname = lname_user.encode()
    fname = fname_user.encode()
    lname_length = bytes([len(lname)])  
    request_data = request_type + lname_length + lname + fname
    client_socket.send(request_data)
        
    response_data = client_socket.recv(1024)
    status_code = get_status_code(response_data)        
    if status_code == 200:
        return "Publish thành công"
    else:
        return "ERROR!"
  
def ping(server_ip, server_port):
    client_socket.settimeout(5)  # Thiết lập timeout là 5 giây

    try:
        request_type = bytes([7])  # Chuyển request_type thành một byte với giá trị 7
        request_message = "Hi"
        request_data = request_type + request_message.encode()   
        client_socket.send(request_data)
    
        response_data = client_socket.recv(1024)
        status_code = get_status_code(response_data)
        if status_code == 200:
            print("Ping thành công")

    except socket.timeout.timeout:
        return "Lỗi: Time out"


# Đóng kết nối
client_socket.close()
