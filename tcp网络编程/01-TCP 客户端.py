# 导入包
from socket import *

# 创建套接字
tcp_client_socket = socket(AF_INET, SOCK_STREAM)

server_ip = input('ip :')
server_port = int(input('port :'))

# 链接服务器
tcp_client_socket.connect((server_ip, server_port))

# 提示用户输入数据
send_data = input('请输入要发送的数据:')

tcp_client_socket.send(send_data.encode())

# 接受对方发送过来的数据
recv_data = tcp_client_socket.recv(1024)
print('接收到的数据是:', recv_data.decode)

# 关闭套接字
tcp_client_socket.close()
# from socket import *
#
# # 创建socket
# tcp_client_socket = socket(AF_INET, SOCK_STREAM)
#
# # 目的信息
# server_ip = input("请输入服务器ip:")
# server_port = int(input("请输入服务器port:"))
#
# # 链接服务器
# tcp_client_socket.connect((server_ip, server_port))
#
# # 提示用户输入数据
# send_data = input("请输入要发送的数据：")
#
# tcp_client_socket.send(send_data.encode())
#
# # 接收对方发送过来的数据，最大接收1024个字节
# recvData = tcp_client_socket.recv(1024)
# print('接收到的数据为:', recvData.decode())
#
# # 关闭套接字
# tcp_client_socket.close()