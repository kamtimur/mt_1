import bluetooth

def parse_input(data):
    if data == "send_screenshot":
        get_screenshot()
    if data == "get_screenshot":
        get_screenshot()
    if data == "send_file":
        send_file()
    if data == "get_file":
        get_file()

def send_screenshot(socket):
    socket.send("ready")
    data = socket.recv(1024)
    #сохранение скриншота
    
def get_screenshot(socket):
    screenshot = pyautogui.screenshot()
    socket.send(screenshot)

def send_file(socket):
    socket.send("send_file")
    data = socket.recv(1024)
    if data == "ready":
        print("add sent file")
        #добавить отправку файла

def get_file(socket):
    socket.send("get_file")
    data = socket.recv(1024)
    #добавить сохранение файла файла



server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
server_sock.bind(("", 3))
server_sock.listen(1)

port = server_sock.getsockname()[1]

uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"

bluetooth.advertise_service(server_sock, "SampleServer", service_id=uuid,
                            service_classes=[uuid, bluetooth.SERIAL_PORT_CLASS],
                            profiles=[bluetooth.SERIAL_PORT_PROFILE],
                            # protocols=[bluetooth.OBEX_UUID]
                            )

print("Waiting for connection on RFCOMM channel", port)

client_sock, client_info = server_sock.accept()
print("Accepted connection from", client_info)

try:
    while True:
        data = client_sock.recv(1024)
        parse_input(data)
        print("Received", data)
        client_sock.send(data)
        print("Send", data)
except OSError:
    pass

print("Disconnected.")

client_sock.close()
server_sock.close()
print("All done.")