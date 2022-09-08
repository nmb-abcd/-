"""
web sever 服务
"""
from socket import *
from select import select
import os


# 具体处理http请求
class Handle:
    def __init__(self, html):
        self.html = html

    def _response(self, status, filename):
        response = "HTTP/1.1 %s\r\n" % status
        response += "Content-Type:text/html\r\n"
        response += "\r\n"
        with open(filename, 'rb') as file:
            response = response.encode() + file.read()
        return response

    def _send_response(self, connfd, info):
        # 请求的是 首页 还是 其他网页
        if info == '/':
            filename = self.html + "/index.html"
        else:
            filename = self.html + info

        # 判断是否存在 True / False
        if os.path.exists(filename):
            data = self._response("200 OK", filename)

        else:
            data = self._response("404 Not Found", self.html + "/404.html")

        connfd.send(data) # 发送响应

    def handle(self, connfd):
        # 接收HTTP请求
        request = connfd.recv(1024).decode()
        # print(request)
        if not request:
            return
        # 获取请求内容
        info = request.split(" ")[1]
        print('请求内容:', info)
        # 组织响应并发送
        self._send_response(connfd, info)


class WebServer:
    # 实例化对象过程中做好准备工作
    def __init__(self, host='', port=0, html=None):
        self.host = host
        self.port = port
        self.address = (host, port)
        self.html = html  # 用户提供的网页
        self.rlist = []
        self.handle = Handle(html)
        self.sock = self._create_socket()

    # 创建套接字
    def _create_socket(self):
        sock = socket()
        sock.bind(self.address)
        sock.setblocking(False)  # 非阻塞
        return sock

    # 连接浏览器
    def _connect(self):
        connfd, addr = self.sock.accept()
        connfd.setblocking(False)
        self.rlist.append(connfd)  # 增加关注

    # start启动函数过程中 搭建服务  IO并发模型
    def start(self):
        self.sock.listen(5)
        print("Listen the port %d" % self.port)
        self.rlist.append(self.sock)  # 初始关注监听套接字
        # 循环接收监控ＩＯ发生
        while True:
            rs, ws, xs = select(self.rlist, [], [])
            for r in rs:
                if r is self.sock:
                    self._connect()  # 处理连接
                else:
                    try:
                        self.handle.handle(r)  # 处理http请求
                    except:
                        pass
                    self.rlist.remove(r)  # 短连接场景,处理完即关闭
                    r.close()


if __name__ == '__main__':
    # 先想一下怎么用
    # 什么需要用户决定 服务器地址  内容
    httpd = WebServer(host="0.0.0.0", port=8880, html="/home/tarena/001yuanma_biji/14、综合案例/day17/day17_all/day17/static")
    httpd.start()  # 启动服务