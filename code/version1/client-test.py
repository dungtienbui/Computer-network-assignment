from ftplib import FTP
import socket
import threading
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import ThreadedFTPServer
import os

#--------------------------set current directory--------------------------
current_directory = os.path.dirname(__file__)
os.chdir(current_directory)


#----------thread variable------------
my_client_thread = None
normal_command_thread = None


#-------server indentification-----------
SERVER_IP = 'localhost'
SERVER_PORT = 12000
server_addr = (SERVER_IP, SERVER_PORT)


#--------config ftp peer----------
PEER_IP = '0.0.0.0'
PEER_PORT = 21
REPOSITORY_PATH = os.path.dirname(current_directory)
peer_adrr = (PEER_IP, PEER_PORT)


#------------------------------get my ip address-------------
def get_ip_address():
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    return ip_address

#------------ftp_peer object--------------
ftp_peer = None


#---------------------start ftp peer--------------------------------
def start_ftp_peer_thread():
    global PEER_IP
    global PEER_PORT
    global ftp_peer
    authorizer = DummyAuthorizer()
    authorizer.add_anonymous(REPOSITORY_PATH, perm="lr")

    handler = FTPHandler
    handler.authorizer = authorizer

    server = ThreadedFTPServer((PEER_IP, PEER_PORT), handler)

    ftp_peer = server
    ftp_thread = threading.Thread(target=ftp_peer.serve_forever)
    ftp_thread.start()

#---------------------stop ftp peer--------------------------------
def stop_ftp_peer(ftp_peer):
    if ftp_peer:
        try:
            ftp_peer.close()
        except Exception as e:
            print(f"An error occurred while stopping the FTP server: {e}")
        finally:
            ftp_peer = None


#----------------tao mot ket noi toi server--------------------
def create_connect(server_address):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(server_address)
    return client_socket

#----------------extract status code of response message---------------     
def get_status_code(response_data):
    status_code = int.from_bytes(response_data[:2], byteorder='big')
    if (status_code > 600 or status_code < 100):
        return None
    else:
        return status_code

#---------------------function-----------------------------------------
####################################################################
#----------------login name password-------------------------------------
def login_funtion(name, password):
    request_type = bytes([1])
    username = name.encode('ascii', 'strict')
    userpass = password.encode('ascii', 'strict')
    username_length = bytes([len(username)])
    
    request_data = request_type + username_length + username + userpass
    
    client_socket = create_connect(server_addr)
    client_socket.send(request_data)
    response_data = client_socket.recv(1024)
    client_socket.close()
    
    #------handle response message from server of login------------
    status_code = get_status_code(response_data)
    if status_code == 200:
        return "Dang nhap thanh cong"
    elif status_code == 401:
        return "Ten dang nhap khong ton tai"
    elif status_code == 402:
        return "Mat khau khong chinh xac"
    else:
        return "Loi phat sinh > <"
 
          
def signup_function(name, password, confirm):
    request_type = bytes([2])
    username = name.encode()
    userpass = password.encode()
    confirmpass = confirm.encode()
    username_length = bytes([len(username)])
    userpass_length = bytes([len(userpass)])
    request_data = request_type + username_length + userpass_length + username + userpass + confirmpass
    
    client_socket = create_connect(server_addr)
    client_socket.send(request_data)
    response_data = client_socket.recv(1024)
    client_socket.close()
    
    status_code = get_status_code(response_data)        
    if status_code == 200:
        return "Dang ky thanh cong"
    elif status_code == 401:
        return "Ten da ton tai"
    elif status_code == 402:
        return "Mat khau xac nhan khong dung"
    else:
        return "Loi phat sinh > <"
    
    
def logout_function(username):
    request_type = bytes([3])
    username = username.encode()
    username_length = bytes([len(username)])    
    request_data = request_type + username_length + username
    
    client_socket = create_connect(server_addr)
    client_socket.send(request_data)
    response_data = client_socket.recv(1024)
    client_socket.close()
    
    status_code = get_status_code(response_data)        
    if status_code == 200:
        return "Dang ky thanh cong"
    else:
        return "Loi phat sinh > <"
    
    

def fetch_function(fname):
    request_type = bytes([4])
    fname_length = bytes([len(fname)])
    fname = fname.encode() 
    request_data = request_type + fname_length + fname
    
    client_socket = create_connect(server_addr)
    client_socket.send(request_data)
    response_data = client_socket.recv(1024)
    client_socket.close()
    
    status_code = get_status_code(response_data)
      
    if status_code == 201:
        status_download = None
        
        #-------------------------handle------------------
        hostname_available_length = int.from_bytes(response_data[2:3], byteorder='big')
        hostname_available_address_length = int.from_bytes(response_data[3:4], byteorder='big')
        hostname = response_data[4:4+hostname_available_length].decode()
        host_addr = response_data[4+hostname_available_length: 4+hostname_available_length + hostname_available_address_length].decode()
        lname = response_data[4+hostname_available_length + hostname_available_address_length:].decode()
        
        # try:
        #     ftp = FTP()
        #     ftp.connect(host_addr, 21)
        #     copy_file = REPOSITORY_PATH + "/" + os.path.basename(lname)
        #     with open(copy_file, "wb") as local_file:
        #         ftp.retrbinary(f"RETR {lname}", local_file.write)
        #     ftp.close()
        # except Exception:
        #     return "Loi phat sinh > <"
        #------------------------------------------------------
        
        ftp = FTP()
        ftp.connect(host_addr, 21)
        ftp.login()
        copy_file = REPOSITORY_PATH + "/copy-" + os.path.basename(lname)
        with open(copy_file, "wb") as local_file:
            ftp.retrbinary(f"RETR {lname}", local_file.write)
        ftp.close()

        
        print(f"File {fname} : {status_download}")
        return "Downloaded"
    elif status_code == 401:
        return "Khong tim thay file"
    elif status_code == 402:
        return  "Khong tim thay host kha dung"
    else:
        return "Loi phat sinh > <"
    
    
    
def unpublish(hostName, fname):
    request_type = bytes([6])
    hostname = hostName.encode()
    fname = fname.encode()
    hostname_length = bytes([len(hostname)])
    fname_length = bytes([len(fname)])
        
    request_data = request_type + hostname_length + fname_length + hostname + fname
        
    client_socket = create_connect(server_addr)
    client_socket.send(request_data)
    response_data = client_socket.recv(1024)
    client_socket.close()
    
    status_code = get_status_code(response_data)        
    if status_code == 200:
        return "Report OK"
    else:
        return "ERROR!"
    
    
def publish_function(fname, lname):
    request_type = bytes([5])
    lname = lname.encode()
    fname = fname.encode()
    fname_length = bytes([len(fname)])  
    request_data = request_type + fname_length + fname + lname
    
    client_socket = create_connect(server_addr)
    client_socket.send(request_data)
    response_data = client_socket.recv(1024)
    client_socket.close()
    
    status_code = get_status_code(response_data)        
    if status_code == 200:
        return f"Publish thanh cong file {fname}"
    else:
        return "ERROR!"
#---------------------------------------------------------
#--------------------end----------------------------------
#---------------------------------------------------------



#---------ham xu ly cac tac vu thong thuong----------------
def handle_command():
    global PEER_IP
    while True:
        print("1. Dang nhap:")
        print("2. Dang ky:")
        print("3. Dang xuat:")
        print("4. Fetch:")
        print("5. Publish:")
        print("6. Unpulish:")
        print("7. Shutdown:")
        icmd = input("Chon chuc nang: ")
        if icmd == '7':
            stop_ftp_peer(ftp_peer)
            break;
        elif icmd == '1':
            my_name = input('Nhap ten: ')
            my_pass = input('Nhap pass: ')
            print(login_funtion(my_name, my_pass))
        elif icmd == '2':
            my_name = input('Nhap ten: ')
            my_pass = input('Nhap pass: ')
            my_conf = input('Nhap confirm pass: ')
            print(signup_function(my_name, my_pass, my_conf))
        elif icmd == '3':
            my_name = input('Nhap ten: ')
            print(logout_function(my_name))
        elif icmd == '4':
            fname = input('Nhap ten file: ')
            print(fetch_function(fname))
        elif icmd == '5':
            fname = input('Nhap fname: ')
            lname = input('Nhap lname: ')
            print(publish_function(fname, lname))
        elif icmd == '6':
            hostname = input('Nhap ten host: ')
            fname = input('Nhap fname: ')
            print(unpublish(hostname, fname))
            
            
#-----------chay thread handle_command----------------
def start_handle_command_process():
    global normal_command_thread
    normal_command_thread = threading.Thread(target=handle_command)
    normal_command_thread.start()

#-----------------main----------------------
if __name__ == "__main__":
    # start_client_listener()
    print("/copy-" + os.path.basename("/dddd/dddd/d.x"))
    start_ftp_peer_thread()
    start_handle_command_process()
    