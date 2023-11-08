from ftplib import FTP
import os
import socket
import threading
import sqlite3
from my_server_db import Database

#---------------------------------------------------------------------------------#
#------------------------------CODE FOR INIT--------------------------------------#
#---------------------------------------------------------------------------------#

#--------------------------set current directory--------------------------
current_directory = os.path.dirname(__file__)
os.chdir(current_directory)

#-----------------------------thread variable-----------------------------
my_server_thread = None
normal_command_thread = None
db_lock = threading.Lock()

#-------------------------server listener config--------------------------
SERVER_IP = 'localhost'
SERVER_PORT = 12000
BACKLOG = 5
serverAddress = (SERVER_IP, SERVER_PORT)
server = None
SERVER_RUNNING = None
connected_clients = []

#----------------server database config-----------------------------------
DATA_PATH = "my_server_db.db"

#---------------------------------------------------------------------------------#
#-------------------------CODE FOR MANY FUNTION-----------------------------------#
#---------------------------------------------------------------------------------#

#------------------------------get and set server address-----------------------------
def get_self_ip_address():
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    return ip_address

def get_server_ip_address():
    global SERVER_IP
    return SERVER_IP

def get_server_port():
    global SERVER_PORT
    return SERVER_PORT

def set_server_port(port = 60000):
    global SERVER_PORT
    SERVER_PORT = port
    
#-------------kiem tra ftp peer co kha dung----------------
def check_ftp_peer_status(host_addr, port=21):
    try:
        ftp = FTP()
        ftp.connect(host_addr, port)
        ftp.login()
        ftp.close()
        return True
    except Exception as e:
        return False

#---------------------------------------------------------------------------------#
#-------------------------CODE FOR HANDLE REPONSE MESSAGE-------------------------#
#---------------------------------------------------------------------------------#

#----------------extract status code of response message--------------------------#
def get_status_code(response_data):
    status_code = int.from_bytes(response_data[:2], byteorder='big')
    if (status_code > 600 or status_code < 100):
        return None
    else:
        return status_code

#-----------------xu ly ket noi tu client toi---------------
def handle_client_request(client_socket):
    request_data = client_socket.recv(1024)
    
    print(f"\nReceived request: {request_data.decode('utf-8')}\n")
    
    request_type = request_data[0:1]
    
    #xu ly theo tung loai request
    respond_message = None
    status_code = None
    respond_name = None
    
    # ------------Xử lý request----------------------
    #----------------Dang nhap----------------------------
    if request_type == b'\x01':
        
        username_length = int.from_bytes(request_data[1:2], byteorder='big')
        username = request_data[2:2 + username_length].decode()
        userpass = request_data[2 + username_length:].decode()
        
        if username == "":
            status_code = int(401).to_bytes(2, byteorder='big')
            respond_name = "NAME_ERROR"
            respond_message = status_code + respond_name.encode()
        
        isNameExit = None
        verify_password = None
        verify_ip = None
        
        #----------------query database---------------------------
        db_lock.acquire()
        try:
            my_db = Database(DATA_PATH)
            data = my_db.get_info_hostname(username)
            my_db.close()
        finally:
            db_lock.release()
            
        if data == []:
            isNameExit = False
        else:
            verify_password = data[0][1]
            verify_ip = data[0][2] #-------kiem tra tai khoan dang nhap co dung vi tri--------------
        #------------------------------------------------------------
            
        if isNameExit == False:
            status_code = int(401).to_bytes(2, byteorder='big')
            respond_name = "NAME_ERROR"
            respond_message = status_code + respond_name.encode()
        
        elif userpass == verify_password:
            #------------kiem tra ip va user-------------------------------
            client_IP_addr = client_socket.getpeername()[0]
            if verify_ip == client_IP_addr:
                status_code = int(200).to_bytes(2, byteorder='big')
                respond_name = "OK"
                respond_message = status_code + respond_name.encode()
            else:
                status_code = int(401).to_bytes(2, byteorder='big')
                respond_name = "NAME_ERROR"
                respond_message = status_code + respond_name.encode()
             #------------------------------------------------------------
             
        else:
            status_code = int(402).to_bytes(2, byteorder='big')
            respond_name = "PASS_ERROR"
            respond_message = status_code + respond_name.encode()
            
    #----------------Dang ky----------------------------
    elif request_type == b'\x02':
        username_length = int.from_bytes(request_data[1:2], byteorder='big')
        userpass_length = int.from_bytes(request_data[2:3] , byteorder='big')
        username = request_data[3:3+username_length].decode()
        userpass = request_data[3+username_length:3+username_length+userpass_length].decode()
        confirmpass = request_data[3+username_length+userpass_length:].decode()
        
        if username == "":
            status_code = int(401).to_bytes(2, byteorder='big')
            respond_name = "NAME_ERROR"
            respond_message = status_code + respond_name.encode()
            
        isNameExit = None    
        
        #----------------query database---------------------------
        db_lock.acquire()
        try:
            my_db = Database(DATA_PATH)
            data = my_db.get_info_hostname(username)
            my_db.close()
        finally:
            db_lock.release()
            
        if data == []:
            isNameExit = False
        else:
            isNameExit = True
        #------------------------------------------------------------
        
        if isNameExit == True:
            status_code = int(401).to_bytes(2, byteorder='big')
            respond_name = "NAME_ERROR"
            respond_message = status_code + respond_name.encode()
            
        elif userpass != confirmpass:
            status_code = int(402).to_bytes(2, byteorder='big')
            respond_name = "PASS_ERROR"
            respond_message = status_code + respond_name.encode()

        else:
            #----------------update database: add new user---------------------------
            db_lock.acquire()
            try:
                my_db = Database(DATA_PATH)
                client_IP_addr = client_socket.getpeername()[0]
                my_db.insert_host(username, userpass, client_IP_addr)
                my_db.close()
            finally:
                db_lock.release()
            #------------------------------------------------------------
            status_code = int(200).to_bytes(2, byteorder='big')
            respond_name = "OK"
            respond_message = status_code + respond_name.encode()
            
    #----------------Dang xuat----------------------------   
    #-----------this request is useless temporarily----------------------------------
    elif request_type == b'\x03':
        username_length = int.from_bytes(request_data[1:2], byteorder='big')
        username = request_data[2:].decode()
        
        status_code = int(200).to_bytes(2, byteorder='big')
        respond_name = "OK"
        respond_message = status_code + respond_name.encode()
        
    #----------------------------Fetch fname-----------------------------------------#
    elif request_type == b'\x04':
        fname_length = int.from_bytes(request_data[1:2], byteorder='big')
        fname = request_data[2:].decode()
        
        if fname == "":
            status_code = int(401).to_bytes(2, byteorder='big')
            respond_name = "NAME_ERROR"
            respond_message = status_code + respond_name.encode()
            
        isFileExit = None
        isHostSharing_Available = None
        hostname_available = None
        hostname_available_address = None
        lname = None
        
        #----------------Query database------------------------
        db_lock.acquire()
        try:
            my_db = Database(DATA_PATH)
            host_list = my_db.search_file(fname)
            my_db.close()
        finally:
            db_lock.release()
        #-----------------------------------------------------
        
        if host_list == []:
            isFileExit = False
        else:
            isFileExit = True
            
            #----------Find first host is available-------------
            for a_host in host_list:
                hostname = a_host[0]
                host_addr = a_host[1]
                if check_ftp_peer_status(host_addr) == False:
                    isHostSharing_Available = False
                else:
                    isHostSharing_Available = True
                    hostname_available = hostname
                    hostname_available_address = host_addr
                    db_lock.acquire()
                    try:
                        my_db = Database(DATA_PATH)
                        lname = my_db.get_lname_of_host(fname, hostname_available)[0][0]
                        my_db.close()
                    finally:
                        db_lock.release()
                    break
            #---------------------------------------------------
        
        if isFileExit == False:
            status_code = int(401).to_bytes(2, byteorder='big')
            respond_name = "NAME_ERROR"
            respond_message = status_code + respond_name.encode()
            
        else:
            if isHostSharing_Available == False:
                status_code = int(403).to_bytes(2, byteorder='big')
                respond_name = "NOT_FOUND_HOST_AVAILABLE"
                respond_message = status_code + respond_name.encode()
            
            else:
                status_code = int(201).to_bytes(2, byteorder='big')
                hostname_available_length = len(hostname_available).to_bytes(1, byteorder='big')
                hostname_available_address_length = len(hostname_available_address).to_bytes(1, byteorder='big')
                respond_message = status_code + hostname_available_length + hostname_available_address_length + hostname_available.encode() + hostname_available_address.encode() + lname.encode()
        
    #--------------------------------Publish fname lname-----------------------------------------------#
    elif request_type == b'\x05':
        fname_length = int.from_bytes(request_data[1:2], byteorder='big')
        fname = request_data[2:2+fname_length].decode()
        lname = request_data[2+fname_length:].decode()
        
        if fname == "":
            status_code = int(401).to_bytes(2, byteorder='big')
            respond_name = "NAME_ERROR"
            respond_message = status_code + respond_name.encode()
        if lname == "":
            status_code = int(401).to_bytes(2, byteorder='big')
            respond_name = "NAME_ERROR"
            respond_message = status_code + respond_name.encode()
        
        check_success = None
        
        #--------------Update data base-----------------------------
        try:
            client_IP_addr = client_socket.getpeername()[0]
            
            db_lock.acquire()
            try:
                my_db = Database(DATA_PATH)
                hostname = my_db.get_hostname_byIP(client_IP_addr)[0][0]
                my_db.insert_file(fname, lname, hostname)
                my_db.close()
            finally:
                db_lock.release()
            
            check_success = True
        except:
            check_success = False
            
        #------------------------------------------------------------
        
        if check_success == True:
            status_code = int(200).to_bytes(2, byteorder='big')
            respond_name = "OK"
            respond_message = status_code + respond_name.encode()
        else:
            status_code = int(401).to_bytes(2, byteorder='big')
            respond_name = "NAME_ERROR"
            respond_message = status_code + respond_name.encode()
        
    #-------------------------Unpublish--------------------------------        
    elif request_type == b'\x06':
        hostname_length = int.from_bytes(request_data[1:2], byteorder='big')
        fname_length = int.from_bytes(request_data[2:3], byteorder='big')
        hostname = request_data[3:3+hostname_length].decode()
        fname = request_data[3+hostname_length:].decode()
        
        #--------------Update data base--------------------------
        db_lock.acquire()
        try:
            my_db = Database(DATA_PATH)
            check_isExit_file = my_db.check_file_of_host(hostname, fname)
            my_db.close()
        finally:
            db_lock.release()
            
        if check_isExit_file != []:
            db_lock.acquire()
            try:
                my_db = Database(DATA_PATH)
                my_db.delete_file_of_host(fname, hostname)
                my_db.close()
            finally:
                db_lock.release()
            
            status_code = int(200).to_bytes(2, byteorder='big')
            respond_name = "OK"
            respond_message = status_code + respond_name.encode()
        else:
            status_code = int(401).to_bytes(2, byteorder='big')
            respond_name = "NAME_ERROR"
            respond_message = status_code + respond_name.encode()
        
        #------------------------------------------------------------
        
        
    #----------------Khong co lenh xu ly phu hop----------------------------
    else:
        status_code = int(410).to_bytes(2, byteorder='big')
        respond_name = "UNKNOW_REQUEST"
        respond_message = status_code + respond_name.encode()
    
    client_socket.send(respond_message)
    client_socket.close()
    
#-----------------khoi tao client listenner---------------
def init_server_listenner(address, backLog = 5):
    global server
    global SERVER_RUNNING
    global connected_clients
    
    SERVER_RUNNING = True
    
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(address)
    server.listen(backLog)

    print(f"\nServer is listening on port: {SERVER_PORT}\n")

    while SERVER_RUNNING:
        client_socket, addr = server.accept()
        connected_clients.append(client_socket)
        print(f"\nAccepted connection from: {addr[0]}:{addr[1]}\n")
        client_handler = threading.Thread(target=handle_client_request, args=(client_socket,))
        client_handler.start()
    
#-------------------START SERVER LISTENER---------------------------#
def start_server_listener():
    global my_server_thread
    my_server_thread = threading.Thread(target=init_server_listenner, args=(serverAddress, BACKLOG))
    my_server_thread.setDaemon(True)
    my_server_thread.start()

def stop_server():
    global server
    global SERVER_RUNNING
    global connected_clients
    for client in connected_clients:
        try:
            client.send()
        except Exception:
            client.close()
            connected_clients.remove(client)
    if not connected_clients:
        server.close()
        SERVER_RUNNING = False
        return True
    else:
        return False
     
     

     
#---------------------------------------------------------------------------------#
#-------------------------CODE FOR HANDLE NORMA TASK------------------------------#
#---------------------------------------------------------------------------------#

# ----------------Ping-----------------------------------------
def ping(hostname):
    
    #----------------query data base-----------------
    db_lock.acquire()
    try:
        my_db = Database(DATA_PATH)
        host_addr = my_db.get_ip_by_hostname(hostname)
        my_db.close()
    finally:
        db_lock.release()
    #------------------------------------------------
    if host_addr == []:
        return "NOT FIND HOSTNAME"
    else:
        mess = None
        if check_ftp_peer_status(host_addr[0][0]) == True:
            mess = f"Host: {hostname} : {host_addr[0][0]} available"
        else:
            mess = f"Host: {hostname} not available"
        return mess
    
#-------------------dicover---------------------------------
def discover(hostname):
    data = None
    db_lock.acquire()
    try:
        my_db = Database(DATA_PATH)
        info_data = my_db.get_info_hostname(hostname)
        if info_data == []:
            data = "Khong tim thay host"
        else:
            data = my_db.get_all_file_of_host(hostname)
        my_db.close()
    finally:
        db_lock.release()
    
    return data

#-------------------remove a registered host---------------------------------
def remove_host(hostname):
    
    flag_success = None
    
    db_lock.acquire()
    try:
        my_db = Database(DATA_PATH)
        info_data = my_db.get_info_hostname(hostname)
        if info_data == []:
            flag_success = 'NOT FIND HOSTNAME'
        else:
            host_ip = info_data[0][2]
            if check_ftp_peer_status(host_ip) == False:
                my_db.delete_host(hostname)
                flag_success = 'DELETED HOST'
            else:
                flag_success = "HOST IS ONLINE. CAN'T DELETE HOST."
        my_db.close()
    finally:
        db_lock.release()
        
    return flag_success

#-------------------remove a file of host---------------------------------
def remove_file_of_host(hostname, fname):
    idx = None
    db_lock.acquire()
    try:
        my_db = Database(DATA_PATH)
        info_data = my_db.get_info_hostname(hostname)
        if info_data == []:
            idx = 1 #---khong tim thay host-----------
        else:
            file_remove = my_db.check_file_of_host(hostname, fname)
            if file_remove == []:
                idx = 2 #-------khong tim thay file---------------
            else:
                my_db.delete_file_of_host(fname, hostname)
                idx = 0 #---------xoa thanh cong------------------------
        my_db.close()
    finally:
        db_lock.release()
        
    return idx

#-------------------get all host---------------------------------
def get_all_host():
    list_host = None
    db_lock.acquire()
    try:
        my_db = Database(DATA_PATH)
        list_host = my_db.get_allData_host_table()
        my_db.close()
    finally:
        db_lock.release()
    return list_host

#-------------------get all file---------------------------------
def get_all_file():
    list_file = None
    db_lock.acquire()
    try:
        my_db = Database(DATA_PATH)
        list_file = my_db.get_allData_file_table()
        my_db.close()
    finally:
        db_lock.release()
    return list_file

#----------xu ly cac tac vu thong thuong----------------------
def handle_command():
    while True:
        print("#------------------------------------#")
        print("1. Ping to client:")
        print("2. Discover:")
        print("3. Remove a host:")
        print("4. Remove a file (fname) of a host:")
        print("5. Get all host:")
        print("6. Get all file:")
        print("7. Shutdown:")
        print("#------------------------------------#")
        icmd = input("Chon chuc nang: ")
        if icmd == '1':
            ip = input("Nhap hostname: ")
            print(ping(ip))
        elif icmd == '2':
            host = input("Nhap ten host: ")
            print(f"Discove {host}")
            print(discover(host))
        elif icmd == '3':
            hostname = input("Nhap hostname: ")
            print(remove_host(hostname))
        elif icmd == '4':
            hostname = input("Nhap hostname: ")
            fname = input("Nhap fname: ")
            idx = remove_file_of_host(hostname, fname)
            if idx == 0:
                print(f"File {fname} is removed")
            elif idx == 1:
                print(f"NOT FIND HOSTNAME!")
            elif idx == 2:
                print(f"NOT FIND FNAME")
                
        elif icmd == '5':
            ls = get_all_host()
            for x in ls:
                print(x)
        elif icmd == '6':
            ls = get_all_file()
            for x in ls:
                print(x)
        elif icmd == '7':
            break

#-------------------START SERVER NORMAL TASK HANDLER---------------------------#
def start_handle_command_process():
    global normal_command_thread
    normal_command_thread = threading.Thread(target=handle_command)
    normal_command_thread.start()
    
#-------------------------------main----------------------
if __name__ == "__main__":
    start_server_listener()
    start_handle_command_process()