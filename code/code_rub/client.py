import socket
import threading

def handle_client(client_socket):
    request = client_socket.recv(1024)  # Đọc yêu cầu từ máy khách
    print(f"Received request: {request.decode('utf-8')}")

    # Xử lý yêu cầu ở đây
    # Ví dụ: client_socket.send(b"Hello from the server!")

    client_socket.close()

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", 8888))  # Chọn cổng và địa chỉ IP
    server.listen(5)  # Lắng nghe tối đa 5 kết nối đồng thời

    print("Server is listening on port 8888")

    while True:
        client_socket, addr = server.accept()  # Chấp nhận kết nối từ máy khách
        print(f"Accepted connection from: {addr[0]}:{addr[1]}")

        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()

if __name__ == "__main__":
    main()
