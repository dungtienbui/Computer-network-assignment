from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import ThreadedFTPServer
import threading

# Tạo một biến toàn cục để theo dõi trạng thái của máy chủ FTP
ftp_server = None

def start_ftp_server():
    global ftp_server
    # Tạo một tài khoản khách với quyền truy cập "elradfmw"
    authorizer = DummyAuthorizer()
    authorizer.add_anonymous("/Users/buitiendung/Documents/Code/Learning code/Visual_studio_code/Python", perm="elr")

    # Cài đặt các xử lý cho máy chủ FTP
    handler = FTPHandler
    handler.authorizer = authorizer

    # Khởi tạo máy chủ FTP với địa chỉ và cổng cụ thể
    server = ThreadedFTPServer(("0.0.0.0", 21), handler)

    # Lưu trạng thái máy chủ FTP vào biến toàn cục
    ftp_server = server

    # Bắt đầu máy chủ FTP trong một luồng riêng biệt
    server_thread = threading.Thread(target=ftp_server.serve_forever)
    server_thread.start()

def stop_ftp_server():
    global ftp_server
    if ftp_server:
        try:
            ftp_server.close()
        except Exception as e:
            print(f"An error occurred while stopping the FTP server: {e}")
        finally:
            ftp_server = None

def command_process():
    global ftp_server
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
            start_ftp_server()
            continue
        elif a == 4 :
            stop_ftp_server()
            continue
        elif a == 6 :
            if ftp_server != None : stop_ftp_server()
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


def start_command_process():
    command_thread = threading.Thread(target=command_process)
    command_thread.start()

if __name__ == "__main__":
    start_command_process()
    
    
    

    