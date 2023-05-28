import socket

# Fungsi untuk mengambil konten file yang diminta oleh client
def get_file_content(file_path):
    try:
        with open(file_path, 'rb') as file:
            content = file.read()
        return content
    except IOError:
        return None

# Fungsi untuk membuat HTTP response message
def create_response(status_code, content_type, content):
    response = "HTTP/1.1 {}\r\n".format(status_code)
    response += "Content-Type: {}\r\n".format(content_type)
    response += "Content-Length: {}\r\n".format(len(content))
    response += "\r\n"
    response += content.decode('utf-8')
    return response.encode('utf-8')

# Fungsi untuk memparsing HTTP request yang diterima
def parse_request(request):
    lines = request.split('\r\n')
    if len(lines) < 2:
        return None

    # Mendapatkan method dan file path dari request
    method, file_path, _ = lines[0].split(' ')

    # Hanya mendukung GET request
    if method != 'GET':
        return None

    return file_path

# Fungsi utama
def main():
    # Konfigurasi alamat dan port server
    server_address = 'localhost'
    server_port = 8000

    # Membuat socket TCP
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Binding socket ke alamat dan port server
    server_socket.bind((server_address, server_port))

    # Listening for incoming connections
    server_socket.listen(1)
    print("Web server berjalan di http://{}:{}".format(server_address, server_port))

    while True:
        # Menerima koneksi dari client
        client_socket, client_address = server_socket.accept()

        # Menerima data dari client
        request_data = client_socket.recv(1024).decode('utf-8')

        # Mem-parsing HTTP request
        file_path = parse_request(request_data)

        if file_path:
            # Mengambil konten file
            if file_path == '/':
                file_content = get_file_content('index.html')
            else:
                file_content = get_file_content(file_path[1:])

            if file_content:
                # Mengirim HTTP response dengan status 200 OK dan konten file
                response = create_response("200 OK", "text/html", file_content)
            else:
                # Mengirim HTTP response dengan status 404 Not Found dan konten dari 404notfound.html
                not_found_content = get_file_content('error404.html')
                response = create_response("404 Not Found", "text/html", not_found_content)
        else:
            # Mengirim HTTP response dengan status 400 Bad Request
            response_content = "<h1>400 Bad Request</h1>"
            response = create_response("400 Bad Request", "text/html", response_content.encode('utf-8'))

        # Mengirim response ke client
        client_socket.sendall(response)

        # Menutup koneksi
        client_socket.close()

if __name__ == '__main__':
    main()
