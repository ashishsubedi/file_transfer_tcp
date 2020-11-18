import socket
from time import time
import sys
import os
from connection import send_data,read_data,establishSendRecvConn_client


FLAG_SEND = 1
FLAG_RECV = 0

END_PATTERN = bytes('ENDCOMM','utf-8')
HEADER_SIZE = 10

flag = -1
recvFlag = -1

filename = ''

TCP_IP = 'localhost'
TCP_PORT = 7200

BUFFER_SIZE = 8192


def init_client(ip=TCP_IP,port=TCP_PORT):
    
    try:
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.connect((TCP_IP,TCP_PORT))
        
        print("Connection Establisehd with Server")
        return s
    except:
        print("Failed to Connect to server")

def init_conn(sock):
    try:
        retry = '1'
        while retry == '1':
            state,flag = establishSendRecvConn_client(sock)
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
            
            retry = input("Another file? Type 1 to process. press other key to exit ")
            flag = -1
            
    except Exception as e:
        print(e)
    finally:
        sock.close()

if __name__ == "__main__":

    s = init_client()
    init_conn(s)
            