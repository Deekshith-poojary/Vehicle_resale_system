import socket
import threading
import ssl
def handle_client_request(client_socket):
    print("Received request:\n")
    # read the data sent by the client in the request
    request = b''
    client_socket.setblocking(False)
    while True:
        try:
            # receive data from web server
            data = client_socket.recv(4096)
            request = request + data
            # Receive data from the original destination server
            print(f"{request.decode('utf-8')} kk")
        except:
            break
    # extract the webserver's host and port from the request
    host, port,method = extract_host_port_from_request(request)
    if method=='CONNECT':
        client_socket.send(b'HTTP/1.1 200 Connection Established\r\n\r\n')
        print('connected')
    # create a socket to connect to the original destination server
    destination_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # connect to the destination server
    destination_socket.connect((host, port))
    # send the original request
    destination_ssl_socket = ssl.wrap_socket(destination_socket, ssl_version=ssl.PROTOCOL_TLS)
    if method=='CONNECT':
        client_socket.send(b'HTTP/1.1 200 Connection Established\r\n\r\n')
        print('connected')
    else:
        destination_ssl_socket.sendall(request)
        # read the data received from the server
        # once chunk at a time and send it to the client
        print("Received response:\n")
        rec=b''
        while True:
            # receive data from web server
            data = destination_ssl_socket.recv(4096)
            rec=rec+data
            # Receive data from the original destination server
            print(f"{data.decode('utf-8')}")
            # no more data to send
            if len(data) > 0:
                # send back to the client
                continue
            else:
                break
        client_socket.sendall(rec)
    # close the sockets
    destination_ssl_socket.close()
    client_socket.close()

def extract_host_port_from_request(request):
    # get the value after the "Host:" string
#    with open('a.txt','wb') as f:
#        f.flush()
#        f.write(request)
#    a=0
#    for i in open('a.txt'):
#        a=a+1
#    if a>1:
#        host_string_start = request.find(b'Host: ') + len(b'Host: ')
#        host_string_end = request.find(b'\r\n', host_string_start)
#        host_string = request[host_string_start:host_string_end].decode('utf-8')
#        webserver_pos = host_string.find("/")
#        if webserver_pos == -1:
#            webserver_pos = len(host_string)
#        # if there is a specific port
#        port_pos = host_string.find(":")
#        # no port specified
#        if port_pos == -1 or webserver_pos < port_pos:
#            # default port
#            port = 80
#            host = host_string[:webserver_pos]
#        else:
#            # extract the specific port from the host string
#            port = int((host_string[(port_pos + 1):])[:webserver_pos - port_pos - 1])
#            host = host_string[:port_pos]
 #   else:

    colon_index = request.find(b':')
    method = request.split(b' ')[0].decode('utf-8')
  #  method = first_line.split()[0].decode('utf-8')
    a=len(method+' ')
    if colon_index != -1:
        # Extract host
        host = request[a:colon_index].decode('utf-8')

        # Extract port
        port_end_index = request.find(b' ', colon_index)
        port = request[colon_index + 1:port_end_index].decode('utf-8')

    print("hhhhhhhh",host,port,method)
    return host, int(port),method

def start_proxy_server():
    port = 8888
    # bind the proxy server to a specific address and port
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('127.0.0.1', port))
    # accept up to 10 simultaneous connections
    server.listen(10)
    print(f"Proxy server listening on port {port}...")
    # listen for incoming requests
    while True:
        client_socket, addr = server.accept()
        print(f"Accepted connection from {addr[0]}:{addr[1]}")
        # create a thread to handle the client request
        client_handler = threading.Thread(target=handle_client_request, args=(client_socket,))
        client_handler.start()

if __name__ == "__main__":
    start_proxy_server()

