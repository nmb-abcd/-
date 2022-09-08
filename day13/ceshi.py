from socket import *
from select import select

class WebServer:
    def __init__(self, host='', port=0, html=None):
        self.host=host
        self.port=port
        self.address=(host,port)
        self.html=html
        self.rlist=[]
        self.sock=self._create_socket()

    def _create_socket(self) ->socket:
        sock=socket()
        sock.bind(self.address)
        sock.setblocking(False)
        return sock

    def _connect(self):
        connfd,addr=self.sock.accept()
        connfd.setblocking(False)
        self.rlist.append(connfd)

    def start(self):
        self.sock.listen(5)
        print("Listen The Port %d"%self.port)
        self.rlist.append(self.sock)
        while True:
            rs,ws,xs=select(self.rlist,[],[])
            for r in rs:
                if r is self.sock:
                    self._connect()
                else:
                    try: