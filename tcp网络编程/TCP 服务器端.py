import socket

# 创建套接字
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# 绑定端口
server_socket.bind(('', 8999))

# 转换属性
server_socket.listen(128)

while True:
    # 从完成连接列表中取出一个客户端进行处理
    client_socket, client_address = server_socket.accept()
    print('收到连接来自:', client_address)

    while True:
        # 进行交流
        recv_data = client_socket.recv(1024)

        if not recv_data:
            print(' 断开连接')
            break
        else:
            print(recv_data.decode())
            client_socket.send(recv_data)

# 关闭套接字
        client_socket.close()
server_socket.close()