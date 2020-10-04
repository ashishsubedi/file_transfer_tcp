import socket
from threading import Thread
from socketserver import ThreadingMixIn

TCP_IP = '0.0.0.0'
TCP_PORT = 7200
BUFFER_SIZE = 4096


FLAG_SEND = 1
FLAG_RECV = 0

flag = -1
recvFlag = -1
filename = ''

def establishSendRecvConn(sock):
    global flag,recvFlag,filename
    while(flag+recvFlag != 1):
        flag = int(input("Enter 0- Receive \t 1- Send \t Press any other key to exit"))
        '''
            Response must be opposite of flag
            For eg, if client is sending file (flag=1), then server must send recieving flag(flag=0) which sums to 1
        '''
        print("Waiting for client's Response")
        recvFlag = int(sock.recv(4).decode('utf-8'))

        #Establish flag handshake
        sock.send(bytes(str(flag),'utf-8'))

    if(flag+recvFlag == 1):return True
    else: return False



def startServer():
    
    tcpsock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    tcpsock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    tcpsock.bind((TCP_IP,TCP_PORT))

    # while True:
    tcpsock.listen(1)
    print("Waiting for incoming connections")
    (sock,(ip,port)) = tcpsock.accept()
    print(f"[CONNECTED] Welcome, {ip}:{port} !")
    try:
        retry = 1
        while(retry == 1 or retry == '1'):
            if not establishSendRecvConn(sock): return False

            if(flag == FLAG_RECV):
                filename = input("Enter full path of file to receive")
            elif flag == FLAG_SEND:
                filename = input("Enter full path of file to send")
            else:
                print("Exiting program")
                return False

            if flag == FLAG_RECV:
                try:
                    with open(filename,'wb') as f:
                        print("Downloading file")
                        while True:
                            data = sock.recv(BUFFER_SIZE)
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
                                sock.send(l)
                                l=f.read(BUFFER_SIZE)
                            if not l:
                                break
                except:
                    print("Some error occured")
                    retry = input("Press 1 to send file again, press any other key to exit")
    except:
        pass
    finally:
        tcpsock.close()

if __name__ == "__main__":
    startServer()
