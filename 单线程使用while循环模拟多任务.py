import socket
import re


def main():
    tcp_server = WebServer()
    tcp_server.run_server()


class WebServer(object):
    def run_server(self):
        """运行服务"""
        # 客户端列表
        clients = list()

        # 设置服务器端非堵塞
        self.tcp_server.setblocking(False)
        while True:
            try:
                client, addr = self.tcp_server.accept()
                # 客户端也是非堵塞
                client.setblocking(False)

                # 放到列表中
                clients.append(client)
            except Exception as e:
                pass

            for client_new in clients:

                try:
                    data = client_new.recv(1024).decode()
                    print(data)
                    if data:
                        # 有数据
                        self.client_exec(client_new, data)
                    else:
                        print("关闭了客户端")
                        # 关闭了客户端
                        client_new.close()
                        clients.remove(client_new)

                except Exception as e:
                    pass

        # 关闭服务器
        self.tcp_server.close()

    def client_exec(self, client, data):
        """这个就是单独客户端的处理"""
        # 接收数据

        head_lines = data.splitlines()
        try:
            print(head_lines[0])
            re_match = re.match(r'[^/]+(/[^ ]*)', head_lines[0])
            # 判断是否匹配了
            if re_match:  # 匹配 了
                file_name = re_match.group(1)
                # 如果是/那么去首页
                if file_name == "/":
                    file_name = "/index.html"
        except Exception as e:
            print(e)  # 工作中是记录到文件

        # 进行响应
        try:
            headers = "HTTP/1.1 200 OK\r\n"

            with open("./html%s" % file_name, 'rb') as f:  
                body = f.read()  # 读取文件

            # body = "show page is find!"

            # content = headers +"\r\n" +body
            content = headers + "\r\n"

            # client.send(content.encode("utf-8"))
            client.send(content.encode("utf-8"))
            client.send(body)
        except Exception as e:
            print(e)
            # 返回一个404的正常显示的页面
            head = "HTTP/1.1 404 NOT FIND\r\n"
            body = "not find page!"
            content = head + "\r\n" + body

            client.send(content.encode("utf-8"))

        # 关闭客户端
        client.close()


    def __init__(self):  
        """ 初始化tcp服务器"""
        # 服务器tcp服务器对象
        self.tcp_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 设置我们的端口地址重用
        self.tcp_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # 绑定端口号
        self.tcp_server.bind(("", 6789))
        # 改成被动模式
        self.tcp_server.listen(128)



if __name__ == '__main__':
    main()
