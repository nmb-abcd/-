"""
练习: 根据所学http协议完成
通过浏览器访问服务端,请求根 则会
显示一张图片在浏览器上 ,图片自选

Content-Type:image/jpeg
"""
from socket import *


def get_response(filename):
    response = "HTTP/1.1 200 OK\r\n"
    response += "Content-Type:image/jpeg\r\n"
    response += "\r\n"
    with open(filename, 'rb') as file:
        response = response.encode() + file.read()
    return response  # 字节串


def main():
    sock = socket()
    sock.bind(("0.0.0.0", 8000))
    sock.listen(5)

    while True:
        connfd, addr = sock.accept()
        print("Connect from", addr)
        # 接收请求
        request = connfd.recv(1024)
        response = get_response("yaya.jpeg")
        connfd.send(response)  # 字节串


if __name__ == '__main__':
    main()