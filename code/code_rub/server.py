import socket
import threading

#server config
SERVER_IP = 'localhost'
HOST = 12000
BACKLOG = 5
my_server = None
serverAddress = (SERVER_IP, HOST)
SERVER_RUNNING = True
clients =[]

def handle_client(client_socket):
    request = client_socket.recv(1024)  # Đọc yêu cầu từ máy khách
    print(f"Received request: {request.decode('utf-8')}")
    
    # Xử lý yêu cầu ở đây
    # Ví dụ: client_socket.send(b"Hello from the server!")

    client_socket.close()

def init_server_listener(address, backLog = 5):
    global SERVER_RUNNING
    global clients
    
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # tao socket
    server.bind(address) # gan IP va Port
    server.listen(backLog)  # Lắng nghe tối đa 5 kết nối đồng thời

    print(f"Server is listening on port: {HOST}")

    while SERVER_RUNNING:
        client_socket, addr = server.accept()  # Chấp nhận kết nối từ máy khách
        clients.append(client_socket)
        print(f"Accepted connection from: {addr[0]}:{addr[1]}")
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()
    
def start_server_listener():
    my_server = threading.Thread(target=init_server_listener, args=(serverAddress, BACKLOG))
    my_server.start()
    
def stop_server_listener():
    global SERVER_RUNNING

def handle_command():
    # command
    global my_server
    while True : 
        print ("Chọn chức năng")
        print ("Chọn chức năng 1 : binh phuong")
        print ("Chọn chức năng 2 : lap phuong")
        print ("Chọn chức năng 3 : *10")
        print ("Chọn chức năng 4 : ngung server")
        print ("Chọn chức năng 5 : chay server")
        print ("Chọn chức năng 6 : break")
        a = int(input("Chon: "))
        if a == 5 : 
            start_server_listener()
            continue
        elif a == 4 :
            
            continue
        elif a == 6 :
            
            break
        b = int(input("Nhap so: "))
        if a == 1 :
            print(b*b)
        elif a == 2 :
            print(b*b*b)
        elif a == 3 :
            print(b*10)        
        else :
            print("Chon sai")
            
def start_handle_command_process():
    command_thread = threading.Thread(target=handle_command)
    command_thread.start()
    
if __name__ == "__main__":
    start_server_listener()
    start_handle_command_process()