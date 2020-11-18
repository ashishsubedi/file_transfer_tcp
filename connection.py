
import socket
from time import time
import sys
import os


FLAG_SEND = 1
FLAG_RECV = 0

END_PATTERN = bytes('ENDCOMM','utf-8')
HEADER_SIZE = 10



TCP_IP = 'localhost'
TCP_PORT = 7200

BUFFER_SIZE = 8192


def establishSendRecvConn_server(sock,flag=-1,recvFlag=-1):
   

    while(flag+recvFlag != 1):
        if flag == -1:
            flag = int(input("Enter 0- Receive \t 1- Send \t Press any other key to exit: "))
        '''
            Response must be opposite of flag
            For eg, if client is sending file (flag=1), then server must send recieving flag(flag=0) which sums to 1
        '''
        print("Waiting for client's Response")
       
        recvFlag = int(sock.recv(4).decode('utf-8'))

        #Establish flag handshake
        sock.send(bytes(str(flag),'utf-8'))

    if(flag+recvFlag == 1):return True, flag
    else: return False, -1

def establishSendRecvConn_client(s,flag=-1,recvFlag=-1):

    while(flag+recvFlag != 1):
        if flag == -1:
            flag = int(input("Enter 0- Receive \t 1- Send \t Press any other key to exit: "))
       

        #Establish flag handshake
        s.send(bytes(str(flag),'utf-8'))
        '''
            Response must be opposite of flag
            For eg, if client is sending file (flag=1), then server must send recieving flag(flag=0) which sums to 1
        '''
        print("Waiting for Server's response")
        recvFlag = int(s.recv(4).decode('utf-8'))

    if(flag+recvFlag == 1):return True,flag
    else: return False,-1

def send_data(s,filename):
    try:
        print("Sending to receiver")
        with open(filename,'rb') as f:
            msgLen = os.path.getsize(filename)
            s.send(bytes(f'{msgLen:<{HEADER_SIZE}}','utf-8'))
            print(f"Total Upload Size: {msgLen} bytes")
            actSize = msgLen
            totalBytes = 0

            while True:
                #Send header
                l = f.read(BUFFER_SIZE)
                # while the file contains data after read
                while(l):
                    totalBytes += len(l)
                    print(f'Uploading... {str(totalBytes):>{HEADER_SIZE}} bytes {str(totalBytes/actSize*100)}% uploaded',end='\r',flush=True)

                    s.sendall(l)
                    l=f.read(BUFFER_SIZE)
                if not l:
                    s.send(END_PATTERN)
                    complete = s.recv(BUFFER_SIZE)
                    if complete ==END_PATTERN:
                        print("Upload complete")
                        break
                    else:
                        raise Exception("Error ACK")
    except Exception as e:
        print("Some error occured",e)
    

def read_data(s,filename):
    try:
        with open(filename,'wb') as f:
            print("Waiting for sender")
            msgLen = int(s.recv(HEADER_SIZE).decode('utf-8'))
            print(f"Total Download Size: {msgLen} bytes")
            actSize = msgLen
            totalBytes = 0

            while msgLen>0:
                if(msgLen>BUFFER_SIZE):
                    size = BUFFER_SIZE
                else:
                    size = msgLen
                msgLen-=BUFFER_SIZE
                
                data = s.recv(size)

                totalBytes += len(data)
                print(f'Downloading... {str(totalBytes):>{HEADER_SIZE}} bytes {str(totalBytes/actSize*100)}%\n',end='\r',flush=True)
                f.write(data)

        complete = s.recv(BUFFER_SIZE)
        if(complete == END_PATTERN):
            s.send(END_PATTERN)
            print(f"\nDownload Complete... {str(totalBytes):>{HEADER_SIZE}} bytes downloaded\t\t")
        else:
            raise Exception("Error ACK")
 
    except Exception as e:
        print("Some error occured",e)
