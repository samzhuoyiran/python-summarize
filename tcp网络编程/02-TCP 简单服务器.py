from socket import *

# 创建socket
tcp_server_socket = socket(AF_INET, SOCK_STREAM)

address = ('', 7788)
tcp_server_socket.bind(address)
tcp_server_socket.listen(128)

# client_socket用来为这个客户端服务
client_socket, clientAddr = tcp_server_socket.accept()

# 接收对方发送过来的数据
recv_data = client_socket.recv(1024)  # 接收1024个字节
print('接收到的数据为:', recv_data.decode())

# 发送一些数据到客户端
client_socket.send("Hello World !".encode())

# 关闭套接字
# client_socket.close()