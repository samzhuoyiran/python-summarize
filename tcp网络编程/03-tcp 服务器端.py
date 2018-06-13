from socket import *

# 创建一个套接字
tcp_server_socket = socket(AF_INET, SOCK_STREAM)
tcp_server_socket.bind(('', 7998))
tcp_server_socket.listen(128)
client_socket, client_address = tcp_server_socket.accept()

# 接收数据
recv_data = client_socket.recv(1024)
print(recv_data.decode())

# 发送一些数据到客户端
client_socket.send('HI'.encode())

# 关闭套接字
client_socket.close()