import os
import socket
import threading
from tkinter import N
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import ThreadedFTPServer

#server config
CLIENT_IP = 'localhost'
CLIENT_PORT = 12000
BACKLOG = 5
my_client_thread = None
client_addr = (CLIENT_IP, CLIENT_PORT)
PEER_RUNNING = True
connected_peer = []

#--------config ftp peer----------
PEER_IP = CLIENT_IP
PEER_PORT = 21
REPOSITORY_PATH = None #----------set path of repository--------------------
peer_adrr = (PEER_IP, PEER_PORT)

#------------ftp_peer_thread--------------
ftp_peer_thread = None
ftp_peer = None

def init_ftp_peer(my_peer_address, path_repository):
    authorizer = DummyAuthorizer()
    authorizer.add_anonymous(path_repository, perm="lr")
    
    handler = FTPHandler
    handler.authorizer = authorizer
    
    peer = ThreadedFTPServer(my_peer_address, handler)
    
    return peer

def start_peer_thread():
    global ftp_peer_thread
    ftp_peer = init_ftp_peer(peer_adrr, REPOSITORY_PATH)
    ftp_peer_thread = threading.Thread(target=ftp_peer.serve_forever)

def stop_ftp_server():
    global ftp_server
    if ftp_peer:
        try:
            ftp_peer.close()
        except Exception as e:
            print(f"An error occurred while stopping the FTP server: {e}")
        finally:
            ftp_server = None
