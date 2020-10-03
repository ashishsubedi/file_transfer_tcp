import socket
from threading import Thread
from socketserver import ThreadingMixIn

TCP_IP = '192.168.1.15'
TCP_PORT = 6000
BUFFER_SIZE = 1024

class ClientThread(Thread):
    def __init__(self,ip: str,port: int,sock: socket.socket):
        Thread.__init__(self)
        self.ip = ip
        self.port =  port
        self.sock = sock
        print(f"New thread started for {ip}:{port} ")

    def run(self):
        filename = 'file.txt'
        with open(filename,'rb') as f:
            while True:
                l = f.read(BUFFER_SIZE)
                # while the file contains data after read
                while(l):
                    self.sock.send(l)
                    l=f.read(BUFFER_SIZE)
                if not l:
                    self.sock.close()
                    break

def startServer():
    tcpsock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    tcpsock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    tcpsock.bind((TCP_IP,TCP_PORT))

    threads = []

    while True:
        tcpsock.listen(5)
        print("Waiting for incoming connections")
        (conn,(ip,port)) = tcpsock.accept()
        print(f"[CONNECTED] Welcome, {ip}:{port} !")
        newThread = ClientThread(ip,port,conn)
        newThread.start()
        threads.append(newThread)

    for t in threads:
        t.join()
    tcpsock.close()

if __name__ == "__main__":
    startServer()
