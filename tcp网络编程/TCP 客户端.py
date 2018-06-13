# 完成TCP客户端的编写。
# 服务器的ip和端口号需手动输入
# 要发送的信息需要手动输入
# 接收服务器返回的数据，并打印。
import socket


def main():
    """主程序"""

    # 创建套接字  请求
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 获取数据
    ip = input('请输入想要发送的服务器 ip:')
    port = int(input(' 请输入 port:'))
    tcp_socket.connect((ip, port))

    # 进行交流
    while True:
        send_data = input(' 请输入你想要发送的信息:')
        tcp_socket.send(send_data.encode())
        recv_data = tcp_socket.recv(1024)
        if not recv_data:
            print('断开连接')
            break
        else:

            print(recv_data.decode())

    # 关闭套接字
    tcp_socket.close()


if __name__ == '__main__':
    main()