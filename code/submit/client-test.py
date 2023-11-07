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


#------------------config ftp peer-------------------
PEER_IP = '0.0.0.0'
PEER_PORT = 21
REPOSITORY_PATH = current_directory
DOWNLOAD_PATH = current_directory
peer_adrr = (PEER_IP, PEER_PORT)
PEER_NAME = None

# -----------set repository path--------------------------
#--------------causion error------------------------------
def set_repository_path(path):
    global REPOSITORY_PATH
    
    if os.path.exists(path):
        REPOSITORY_PATH = path
        return True
    else:
        return False
    
def set_download_path(path):
    global DOWNLOAD_PATH

    if os.path.exists(path):
        DOWNLOAD_PATH = path
        return True
    else:
        return False

#------------------------------get my ip address-------------
def get_self_ip_address():
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    return ip_address

#------------------------------get set server address-------------
def get_server_ip_address():
    global SERVER_IP
    return SERVER_IP

def set_server_ip_address(ip_addr):
    global SERVER_IP
    SERVER_IP = ip_addr

def get_server_port():
    global SERVER_PORT
    return SERVER_PORT

def set_server_port(port = 60000):
    global SERVER_PORT
    SERVER_PORT = port
    
#----------------------ftp_peer object--------------
ftp_peer = None


#---------------------start ftp peer-----------------
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
    username = name.encode()
    userpass = password.encode()
    username_length = bytes([len(username)])
    
    request_data = request_type + username_length + username + userpass
    
    try:
        client_socket = create_connect(server_addr)
    except ConnectionRefusedError:
        return "CONNECTION_REFUSED"
    except Exception:
        return "OTHER_CONNECT_ERROR!"
    
    client_socket.send(request_data)
    response_data = client_socket.recv(1024)
    client_socket.close()
    
    #------handle response message from server of login------------
    status_code = get_status_code(response_data)
    # name_response = response_data[2:].decode()
    if status_code == 200:
        global PEER_NAME
        PEER_NAME = name
        return "OK"
    elif status_code == 401:
        return "Ten dang nhap khong ton tai."
    elif status_code == 402:
        return "Mat khau khong chinh xac."
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
    
    try:
        client_socket = create_connect(server_addr)
    except ConnectionRefusedError:
        return "CONNECTION_REFUSED"
    except Exception:
        return "OTHER_CONNECT_ERROR!"
    
    client_socket.send(request_data)
    response_data = client_socket.recv(1024)
    client_socket.close()
    
    status_code = get_status_code(response_data)        
    if status_code == 200:
        return "Dang ky thanh cong"
    elif status_code == 401:
        return "Ten da ton tai"
    elif status_code == 402:
        return "Mat khau xac nhan khong dung."
    else:
        return "Loi phat sinh > <"
    
    
def logout_function(username):
    global PEER_NAME
    if PEER_NAME != username:
        return "Nguoi dung nhap sai ten."
    request_type = bytes([3])
    username = username.encode()
    username_length = bytes([len(username)])    
    request_data = request_type + username_length + username
    
    try:
        client_socket = create_connect(server_addr)
    except ConnectionRefusedError:
        return "CONNECTION_REFUSED"
    except Exception:
        return "OTHER_CONNECT_ERROR!"
    
    client_socket.send(request_data)
    response_data = client_socket.recv(1024)
    client_socket.close()
    
    status_code = get_status_code(response_data)        
    if status_code == 200:
        PEER_NAME = None
        return "Dang xuat thanh cong."
    else:
        return "Loi phat sinh > <"
    
    

def fetch_function(fname):
    global DOWNLOAD_PATH
    
    request_type = bytes([4])
    fname_length = bytes([len(fname)])
    fname = fname.encode() 
    request_data = request_type + fname_length + fname
    
    try:
        client_socket = create_connect(server_addr)
    except ConnectionRefusedError:
        return "CONNECTION_REFUSED"
    except Exception:
        return "OTHER_CONNECT_ERROR!"
    
    client_socket.send(request_data)
    response_data = client_socket.recv(1024)
    client_socket.close()
    
    status_code = get_status_code(response_data)
      
    if status_code == 201:
        
        #-------------------------handle------------------
        hostname_available_length = int.from_bytes(response_data[2:3], byteorder='big')
        hostname_available_address_length = int.from_bytes(response_data[3:4], byteorder='big')
        hostname = response_data[4:4+hostname_available_length].decode()
        host_addr = response_data[4+hostname_available_length: 4+hostname_available_length + hostname_available_address_length].decode()
        lname = response_data[4+hostname_available_length + hostname_available_address_length:].decode()
        
        ftp = FTP()
        ftp.connect(host_addr, PEER_PORT)
        ftp.login()
        
        #------file copied will has prefix "copy-"
        copy_file = "copy-" + os.path.basename(lname)
        
        try:
            ftp.voidcmd('TYPE I')
            f_size = ftp.size(lname)
        except Exception:
            unpublish(hostname, fname.decode())
            return "Lname_error."
        
        copy_file_path =  DOWNLOAD_PATH + "/" + copy_file
        with open(copy_file_path, "wb") as local_file:
            ftp.retrbinary(f"RETR {lname}", local_file.write)
        
        ftp.close()
        
        cf_size = os.path.getsize(copy_file)
        
        if f_size != cf_size:
            return f"Loi trong qua trinh tai file. File size: {f_size} >< Copy file size: {cf_size}"
        else:
            if DOWNLOAD_PATH == REPOSITORY_PATH:
                publish_function(copy_file, copy_file_path)
                return "File is downloaded completely and published."
            else:
                return "File is downloaded completely."
    elif status_code == 401:
        return "Khong tim thay file."
    elif status_code == 402:
        return  "Khong tim thay host kha dung."
    else:
        return "Loi phat sinh > <"
    
    
    
def unpublish(hostName, fname):
    
    request_type = bytes([6])
    hostname = hostName.encode()
    fname = fname.encode()
    hostname_length = bytes([len(hostname)])
    fname_length = bytes([len(fname)])
        
    request_data = request_type + hostname_length + fname_length + hostname + fname
        
    try:
        client_socket = create_connect(server_addr)
    except ConnectionRefusedError:
        return "CONNECTION_REFUSED"
    except Exception:
        return "OTHER_CONNECT_ERROR!"
    
    client_socket.send(request_data)
    response_data = client_socket.recv(1024)
    client_socket.close()
    
    status_code = get_status_code(response_data)        
    if status_code == 200:
        return "OK"
    else:
        return "ERROR!"
    
    
def publish_function(fname, lname):
    
    request_type = bytes([5])
    lname = lname.encode()
    fname = fname.encode()
    fname_length = bytes([len(fname)])  
    request_data = request_type + fname_length + fname + lname
    
    try:
        client_socket = create_connect(server_addr)
    except ConnectionRefusedError:
        return "CONNECTION_REFUSED"
    except Exception:
        return "OTHER_CONNECT_ERROR!"
    
    client_socket.send(request_data)
    response_data = client_socket.recv(1024)
    client_socket.close()
    
    status_code = get_status_code(response_data)        
    if status_code == 200:
        return f"Publish thanh cong file {fname}."
    else:
        return "ERROR!"
#---------------------------------------------------------
#--------------------end----------------------------------
#---------------------------------------------------------

        
        print("10. Shutdown:")
        
#---------ham xu ly cac tac vu thong thuong----------------
def handle_command():
    global PEER_NAME
    running = True
    running_log = True
    while running:
        print("#------------------------------------#")
        print("1. Dang nhap: ")
        print("2. Dang ky:")
        print("3. Cai dat dia chi cua server: ")
        print("4. Shutdown:")
        unlog_icmd = input("Chon chuc nang: ")
        if unlog_icmd == '1':
            my_name = input('Nhap ten: ')
            my_pass = input('Nhap pass: ')
            log = login_funtion(my_name, my_pass)
            print(log)
            
            if log == "OK":
                while running_log:
                    print("#------------------------------------#")
                    print("1. Dang xuat:")
                    print("2. Fetch:")
                    print("3. Publish:")
                    print("4. Unpulish:")
                    print("5. Cai dat thu muc download: ")
                    print("6. Cai dat thu muc repository path: ")
                    icmd = input("Chon chuc nang: ")
                    if icmd == '1':
                        my_name = input('Nhap ten: ')
                        if PEER_NAME != my_name:
                            print("Nhap sai ten.")
                        else:
                            print(logout_function(my_name))
                            break
                    elif icmd == '2':
                        fname = input('Nhap ten file: ')
                        print(fetch_function(fname))
                    elif icmd == '3':
                        fname = input('Nhap fname: ')
                        lname = input('Nhap lname: ')
                        print(publish_function(fname, lname))
                    elif icmd == '4':
                        hostname = input('Nhap ten host: ')
                        fname = input('Nhap fname: ')
                        print(unpublish(hostname, fname))
                    elif icmd == '5':
                        path = input("Nhap duong dan download (tuyet doi) : ")
                        if set_download_path(path) == True :
                            print("Thiet lap duong dan download thanh cong.")
                        else:
                            print("Thiet lap duong dan download khong thanh cong.")
                    elif icmd == '6':
                        path = input("Nhap duong dan repository (tuyet doi) : ")
                        if set_repository_path(path) == True :
                            print("Thiet lap duong dan repository thanh cong.")
                        else:
                            print("Thiet lap duong dan repository khong thanh cong.")          
                    print("#------------------------------------#")
        elif unlog_icmd == '2':
            my_name = input('Nhap ten: ')
            my_pass = input('Nhap pass: ')
            my_conf = input('Nhap confirm pass: ')
            print(signup_function(my_name, my_pass, my_conf))            
        elif unlog_icmd == '3':
            addr = input("Nhap dia chi ip cua server: ")
            prt = input("Nhap dia port cua server: ")
            set_server_ip_address(addr)
            set_server_port(prt)
        elif unlog_icmd == '4':
            stop_ftp_peer(ftp_peer)
            break;
        print("#------------------------------------#")
        
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
    