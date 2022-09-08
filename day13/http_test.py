"""
http请求和响应
"""
from socket import *
sock=socket()
sock.bind(("0.0.0.0",8880))
sock.listen(5)

connfd,addr=sock.accept()
print("Connect From",addr)
data=connfd.recv(1024)
respose="""HTTP/1.1 200 OK
Content=Type:texxt/html

Hello World
"""
connfd.send(respose.encode())
print(data.decode())

connfd.close()
sock.close()