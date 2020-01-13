import bluetooth
from common import *

def parse_input(data, socket):
    if data == b'send_screenshot':
        send_screenshot_serv(socket)
    if data == b'get_screenshot':
        get_screenshot_serv(socket)
    if data == b'send_file':
        send_file_serv(socket)
    if data == b'get_file':
        get_file_serv(socket)

def send_screenshot_serv(socket):
    print("send_screenshot_serv")
    get_screenshot(socket)
    send_ready(socket)

    
def get_screenshot_serv(socket):
    print("get_screenshot_serv")
    send_screenshot(socket)
    recv_ready(socket)

def send_file_serv(socket):
    print("send_file_serv")
    recv_file(socket)
    send_ready(socket)


def get_file_serv(socket):
    print("get_file_serv")
    path = socket.recv(1024)
    send_file(path,socket)
    recv_ready(socket)


server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
server_sock.bind(("", bluetooth.PORT_ANY))
server_sock.listen(1)

port = server_sock.getsockname()[1]

uuid = "58369c20-ecf6-11e3-ba36-82687f4fc15c"

bluetooth.advertise_service(server_sock, "SampleServer",
                    service_id=uuid,
                    service_classes=[uuid, bluetooth.SERIAL_PORT_CLASS],
                    profiles=[bluetooth.SERIAL_PORT_PROFILE]
                    )

print("Waiting for connection on RFCOMM channel %d" % port)

client_sock, client_info = server_sock.accept()
print("Accepted connection from ", client_info)

while True:
    client_sock.setblocking(True)
    data = client_sock.recv(1024)
    print("Received", data)
    parse_input(data, client_sock)
    print("ready for command")

print("Disconnected.")

client_sock.close()
server_sock.close()
print("All done.")
