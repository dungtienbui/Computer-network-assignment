from http import client
import socket
import threading
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import ThreadedFTPServer

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
REPOSITORY_PATH = "/Users/buitiendung/Documents/Learn_in_BachKhoa/Năm 3/HK231/Computer networks/team assignment/assignment1/code/code_rub"
peer_adrr = (PEER_IP, PEER_PORT)

#------------ftp_peer object--------------
ftp_peer = None


#---------------------start ftp peer--------------------------------
def start_ftp_peer_thread():
    global PEER_IP
    global PEER_PORT
    global ftp_peer
    authorizer = DummyAuthorizer()
    authorizer.add_anonymous(REPOSITORY_PATH, perm="elr")

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
 
          
def Signup(name, password, confirm):
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
    
    
def Logout(username):
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
    
    

def fetch(fname):
    request_type = bytes([4])
    fname = fname.encode()
    fname_length = bytes([len(fname)])  
    request_data = request_type + fname_length + fname
    
    client_socket = create_connect(server_addr)
    client_socket.send(request_data)
    response_data = client_socket.recv(1024)
    client_socket.close()
    
    status_code = get_status_code(response_data)    
    if status_code == 200:
        status_download = None
        #-------------------------handle-------------------
        #
        #
        #---------------------tai file------------------------
        #--------------a function to download file-------------
        #
        #------------------------------------------------------
        return f"File {fname} : {status_download}"
    elif status_code == 401:
        return "Khong tim thay file"
    elif status_code == 402:
        return  "Khong tim thay host kha dung"
    else:
        return "Loi phat sinh > <"
    
    
    
def unpublish(hostName, fname):
    request_type = bytes([5])
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
    
    
def publish(lname, fname):
    request_type = bytes([6])
    lname = lname.encode()
    fname = fname.encode()
    lname_length = bytes([len(lname)])  
    request_data = request_type + lname_length + lname + fname
    
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
        icmd = int(input("Chon chuc nang: "))
        if icmd == 7:
            stop_ftp_peer(ftp_peer)
            break;
        
#-----------chay thread handle_command----------------
def start_handle_command_process():
    global normal_command_thread
    normal_command_thread = threading.Thread(target=handle_command)
    normal_command_thread.start()

#-----------------main----------------------
if __name__ == "__main__":
    # start_client_listener()
    start_ftp_peer_thread()
    start_handle_command_process()
    