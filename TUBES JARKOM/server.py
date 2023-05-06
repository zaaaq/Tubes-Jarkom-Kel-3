from socket import *

def tcp_server():
    SERVER_HOST = "localhost"
    SERVER_PORT = 6789

    sock_server = socket(AF_INET, SOCK_STREAM)
    sock_server.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

    sock_server.bind((SERVER_HOST, SERVER_PORT))

    sock_server.listen()

    print("Server ready.....")

    while True:
        sock_client, client_addres = sock_server.accept()

        request = sock_client.recv(1024).decode()
        print("Dari client :"+request)

        response = handle_request()
        sock_client.send(response.encode())

        sock_client.close()
    #endwhile
    sock_server.close()
    #endwhile
#enddef

def handle_request():
    response_line = "HTTP/1.1 200 OK\r\n"
    content_type = "Content-Type: text/html\r\n\r\n"
    file = open("D:\Telkom Univ\SEM 4\TUBES JARKOM\index.html", 'r')
    message_body = file.read()
    file.close()
    response = response_line+content_type+message_body
    return response
#enddef

if __name__ == "__main__":
    tcp_server()
#endmain