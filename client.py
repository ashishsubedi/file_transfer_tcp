import socket
from time import time

TCP_IP = 'https://ftserverhost.herokuapp.com/'
TCP_PORT = 6000
BUFFER_SIZE = 1024

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect((TCP_IP,TCP_PORT))

start = time()

with open('received_file','wb') as f:
    print("Downloading file")
    while True:
        data = s.recv(BUFFER_SIZE)
        print(data)
        if not data:
            break
        f.write(data)

end = time()
print(f'File downloaded in {end-start} ms')
s.close()
        