from socket import *
from select import select

HOST="0.0.0.0"
PORT=8889

ADDR=(HOST,PORT)

sock=socket()
sock.bind(ADDR)
sock.listen(7)


while True:
    file = open("yaya.jpeg", mode="rb")
    connfd,addr=sock.accept()
    print("Connect From",addr)
    data=connfd.recv(1024*10)
    print(data.decode())
    respose="""HTTP/1.1 200 OK
Content=Type:image/jpeg

""".encode()+file.read()
    connfd.send(respose)
