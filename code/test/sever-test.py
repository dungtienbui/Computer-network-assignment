from pickle import TRUE
from secrets import token_bytes
from ftplib import FTP
import socket
import threading
import sqlite3

#----------thread variable------------
my_server_thread = None
normal_command_thread = None

#-------server config-----------
SERVER_IP = 'localhost'
HOST = 12000
BACKLOG = 5
serverAddress = (SERVER_IP, HOST)
server = None

SERVER_RUNNING = None
connected_clients = []

#----------------extract status code of response message---------------     
def get_status_code(response_data):
    status_code = int.from_bytes(response_data[:2], byteorder='big')
    if (status_code > 600 or status_code < 100):
        return None
    else:
        return status_code

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
    
# ----------------Ping-----------------------------------------
def ping(hostName):
    
    #----------------query data base-----------------
    host_addr = hostName
    #-----------------------------------------
    
    mess = None
    if check_ftp_peer_status(host_addr) == True:
        mess = f"Host: {hostName} available"
    else:
        mess = f"Host: {hostName} not available"
    return mess

#-----------------xu ly ket noi tu client toi---------------
def handle_client_request(client_socket):
    request_data = client_socket.recv(1024)  # Đọc yêu cầu từ máy khách
    print(f"Received request: {request_data.decode('utf-8')}")
    
    request_type = request_data[0:1]
    
    #xu ly theo tung loai request
    respond_message = None
    status_code = None
    respond_name = None
    # ------------Xử lý request----------------------
    
    #----------------Dang nhap----------------------------
    if request_type == b'\x01':
        
        username_length = int.from_bytes(request_data[1:2], byteorder='big')
        username = request_data[2:2 + username_length].decode('ascii', 'strict')
        userpass = request_data[2 + username_length:].decode('ascii', 'strict')
        
        #----------------query database---------------------------
        # to do
        isNameExit = True
        verifyPass = "12344"
        #
        #
        #------------------------------------------------------------
        
        if username == "":
            status_code = int(401).to_bytes(2, byteorder='big')
            respond_name = "NAME_ERROR"
            respond_message = status_code + respond_name.encode('ascii', 'strict')
        
        if isNameExit == False:
            status_code = int(401).to_bytes(2, byteorder='big')
            respond_name = "NAME_ERROR"
            respond_message = status_code + respond_name.encode('ascii', 'strict')
        
        elif userpass == verifyPass:
            status_code = int(200).to_bytes(2, byteorder='big')
            respond_name = "OK"
            respond_message = status_code + respond_name.encode('ascii', 'strict')
            
        else:
            status_code = int(402).to_bytes(2, byteorder='big')
            respond_name = "PASS_ERROR"
            respond_message = status_code + respond_name.encode('ascii', 'strict')
            
    #----------------Dang ky----------------------------
    elif request_type == b'\x02':
        username_length = int.from_bytes(request_data[1:2], byteorder='big')
        userpass_length = request_data[2:3]
        username = request_data[3:3+username_length].decode('ascii', 'strict')
        userpass = request_data[3+username_length:3+username_length+userpass_length].decode('ascii', 'strict')
        confirmpass = request_data[3+username_length+userpass_length:].decode('ascii', 'strict')
        
        #----------------query database---------------------------
        # to do
        isNameExit = True
        #
        #
        #------------------------------------------------------------
        if username == "":
            status_code = int(401).to_bytes(2, byteorder='big')
            respond_name = "NAME_ERROR"
            respond_message = status_code + respond_name.encode('ascii', 'strict')
        
        if isNameExit == True:
            status_code = int(401).to_bytes(2, byteorder='big')
            respond_name = "NAME_ERROR"
            respond_message = status_code + respond_name.encode('ascii', 'strict')
            
        elif userpass != confirmpass:
            status_code = int(402).to_bytes(2, byteorder='big')
            respond_name = "PASS_ERROR"
            respond_message = status_code + respond_name.encode('ascii', 'strict')

        else:
            #----------------update database: add new user---------------------------
            #
            # to do
            # 
            #------------------------------------------------------------
            status_code = int(200).to_bytes(2, byteorder='big')
            respond_name = "OK"
            respond_message = status_code + respond_name.encode('ascii', 'strict')
            
    #----------------Dang xuat----------------------------   
    elif request_type == b'\x03':
        username_length = int.from_bytes(request_data[1:2], byteorder='big')
        username = request_data[2:].decode('ascii', 'strict')
        
        status_code = int(200).to_bytes(2, byteorder='big')
        respond_name = "OK"
        respond_message = status_code + respond_name.encode('ascii', 'strict')
            
    #----------------Fetch fname----------------------------
    elif request_type == b'\x04':
        fname_length = request_data[1:2]
        fname = request_data[2:].decode('ascii', 'strict')
        
        if fname == "":
            status_code = int(401).to_bytes(2, byteorder='big')
            respond_name = "NAME_ERROR"
            respond_message = status_code + respond_name.encode('ascii', 'strict')
            
        #----------------query database---------------------------
        # to do
        #
        isFileExit = False
        isHostSharing_Available = False
        hostname_available = "Dung"
        hostname_available_address = "123.123.123.123"
        #
        #
        #---------------------------------------------------------
        
        if isFileExit == False:
            status_code = int(401).to_bytes(2, byteorder='big')
            respond_name = "NAME_ERROR"
            respond_message = status_code + respond_name.encode('ascii', 'strict')
            
        elif isHostSharing_Available == False:
            status_code = int(403).to_bytes(2, byteorder='big')
            respond_name = "NOT_FOUND_HOST_AVAILABLE"
            respond_message = status_code + respond_name.encode('ascii', 'strict')
        
        else:
            status_code = int(201).to_bytes(2, byteorder='big')
            respond_name = "FOUND_HOST_AVAILABLE"
            hostname_available_length = len(hostname_available).to_bytes(1, byteorder='big')
            
            respond_message = status_code + respond_name.encode('ascii', 'strict') + hostname_available_length + hostname_available.encode('ascii', 'strict') + hostname_available_address.encode('ascii', 'strict')
        
        
    #Yeu cau xoa ten file duoc B chia se do khong tai duoc file do tu B - yeu cau nay la tu dong gui tu app cua client
    elif request_type == b'\x05':
        hostname_length = request_data[1:2]
        fname_length = request_data[2:3]
        hostname = request_data[3:3+hostname_length].decode('ascii', 'strict')
        fname = request_data[3+hostname_length:].decode('ascii', 'strict')
        
        #--------------Update data base--------------------------
        # to do
        #
        #------------------------------------------------------------
        
        status_code = int(200).to_bytes(2, byteorder='big')
        respond_name = "OK"
        respond_message = status_code + respond_name.encode('ascii', 'strict')
        
    #----------------Publish fname lname----------------------------
    elif request_type == b'\x06':
        lname_length = request_data[1:2]
        lname = request_data[2:2+lname_length].decode('ascii', 'strict')
        fname = request_data[2+lname_length:]()
        
        #--------------Update data base--------------------------
        # to do
        # 
        # 
        #------------------------------------------------------------
        
        status_code = int(200).to_bytes(2, byteorder='big')
        respond_name = "OK"
        respond_message = status_code + respond_name.encode('ascii', 'strict')
        
    #----------------Khong co lenh xu ly phu hop----------------------------
    else:
        status_code = int(410).to_bytes(2, byteorder='big')
        respond_name = "UNKNOW_REQUEST"
        respond_message = status_code + respond_name.encode('ascii', 'strict')
    
    client_socket.send(respond_message)
    client_socket.close()
    
#-----------------khoi tao client listenner---------------
def init_server_listenner(address, backLog = 5):
    global server
    global SERVER_RUNNING
    global connected_clients
    
    SERVER_RUNNING = True
    
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # tao socket
    server.bind(address) # gan IP va Port
    server.listen(backLog)  # Lắng nghe tối đa 5 kết nối đồng thời

    print(f"Server is listening on port: {HOST}")

    while SERVER_RUNNING:
        client_socket, addr = server.accept()  # Chấp nhận kết nối từ máy khách
        connected_clients.append(client_socket)
        print(f"Accepted connection from: {addr[0]}:{addr[1]}")
        client_handler = threading.Thread(target=handle_client_request, args=(client_socket,))
        client_handler.start()
    
    server.close()
    
# def stop_server():
#     global SERVER_RUNNING
#     global connected_clients
#     if not connected_clients:
#         SERVER_RUNNING = False
#         return True
#     for client in connected_clients :
#         try:
#             # Kiểm tra trạng thái của kết nối, ví dụ: gửi một tin nhắn kiểm tra
#             client.send(b"Are you there?")
#         except Exception:
#             # Xử lý nếu kết nối đã đóng hoặc gặp lỗi
#             print(f"Client {client.getpeername()} disconnected.")
#             client.close()
#             connected_clients.remove(client)
     
#----------xu ly cac tac vu thong thuong----------------------  
def handle_command():
    while True:
        print("1. ping to client:")
        print("2. discover:")
        print("3. Shutdown:")
        icmd = int(input("Chon:"))
        if icmd == 1:
            ip = input("Nhap dia chi: ")
            print(ping(ip))
            
        elif icmd == 2:
            host = input("Nhap te host")
            print(f"Discove {host}")
            
        elif icmd == 3:
            global SERVER_RUNNING
            SERVER_RUNNING = False
            break
        
#--------------chay thread---------------------
def start_server_listener():
    global my_server_thread
    my_server_thread = threading.Thread(target=init_server_listenner, args=(serverAddress, BACKLOG))
    my_server_thread.start()
            
def start_handle_command_process():
    global normal_command_thread
    normal_command_thread = threading.Thread(target=handle_command)
    normal_command_thread.start()
    
#-----------------main----------------------
if __name__ == "__main__":
    start_server_listener()
    start_handle_command_process()