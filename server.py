import socket
import sys,os
from connection import send_data,read_data,establishSendRecvConn_server


TCP_IP = '0.0.0.0'
TCP_PORT = 7200
BUFFER_SIZE = 2048


FLAG_SEND = 1
FLAG_RECV = 0

END_PATTERN = bytes('ENDCOMM','utf-8')

FILE_SIZE_HEADER = 10
FILENAME_SIZE_HEADER = 30
HEADER_SIZE = FILE_SIZE_HEADER + FILENAME_SIZE_HEADER


filename = ''


def startServer(ip=TCP_IP,port=TCP_PORT):
    try:
        tcpsock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        tcpsock.bind((ip,port))
       
        tcpsock.listen(1)
        print("Waiting for incoming connections")
        (sock,(ip,port)) = tcpsock.accept()
        print(f"[CONNECTED] Welcome, {ip}:{port} !")
        return sock,ip,port

    except Exception as e :
        print("Error",e)
        return None,e,False
    
    

def init_conn(sock):
    try:
        retry = '1'
        while retry == '1':
            state,flag = establishSendRecvConn_server(sock)
            if not state: return False
            if(flag == FLAG_RECV):
                filename = input("Enter full path of file to receive: ")
            elif flag == FLAG_SEND:
                filename = input("Enter full path of file to send: ")
            else:
                print("Exiting program")
                return False

            if flag == FLAG_RECV:
                read_data(sock,filename)

            elif flag == FLAG_SEND:
                send_data(sock,filename)
            
            retry = input("Another file? Type 1 to send. press other key to exit ")
            flag = -1

            
    except Exception as e:
        print(e)
    finally:
        sock.close()

if __name__ == "__main__":
    sock,ip,port = startServer()
    init_conn(sock)
