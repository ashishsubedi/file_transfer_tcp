import socket
from time import time
import sys

FLAG_SEND = 1
FLAG_RECV = 0

flag = -1
recvFlag = -1
filename = ''

TCP_IP = '0.0.0.0'
TCP_PORT = 7200
BUFFER_SIZE = 4096

TCP_IP = input("Enter SERVER address: ")
TCP_PORT = int(input("Enter server port: "))

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect((TCP_IP,TCP_PORT))

print("Connection Establisehd with Server")
def establishSendRecvConn():
    global flag,recvFlag,filename
    while(flag+recvFlag != 1):
        flag = int(input("Enter 0- Receive \t 1- Send \t Press any other key to exit"))
       

        #Establish flag handshake
        s.send(bytes(str(flag),'utf-8'))
        '''
            Response must be opposite of flag
            For eg, if client is sending file (flag=1), then server must send recieving flag(flag=0) which sums to 1
        '''
        print("Waiting for Server's response")
        recvFlag = int(s.recv(4).decode('utf-8'))

    if(flag+recvFlag == 1):return True
    else: return False


if __name__ == "__main__":
    try: 
        retry = 1
        while (retry == 1 or retry == '1'):
            if not establishSendRecvConn(): sys.exit(1)

            if(flag == FLAG_RECV):
                filename = input("Enter full path of file to receive")
            elif flag == FLAG_SEND:
                filename = input("Enter full path of file to send")
            else:
                print("Exiting program")
                sys.exit(1)

            if flag == FLAG_RECV:
                try:
                    with open(filename,'wb') as f:
                        print("Downloading file")
                        while True:
                            data = s.recv(BUFFER_SIZE)
                            print(data)
                            if not data:
                                break
                            f.write(data)
                except:
                    print("Some error occured")
                    retry = input("Press 1 to send file again, press any other key to exit")
            
            elif flag == FLAG_SEND:
                try:
                    with open(filename,'rb') as f:
                        print("Uploading file")
                        while True:
                            l = f.read(BUFFER_SIZE)
                            # while the file contains data after read
                            while(l):
                                s.send(l)
                                l=f.read(BUFFER_SIZE)
                            if not l:
                                break
                except:
                    print("Some error occured")
                    retry = input("Press 1 to send file again, press any other key to exit")
            
            
            retry = input("Press 1 to send file again, press any other key to exit")
    except:
        pass
    finally:
        s.close()
            