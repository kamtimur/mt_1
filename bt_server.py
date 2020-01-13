from bluetooth import *
import pyautogui
from PIL import Image
import io
import ntpath


def image_to_byte_array(image: Image):
  imgByteArr = io.BytesIO()
  image.save(imgByteArr, format='PNG')
  imgByteArr = imgByteArr.getvalue()
  return imgByteArr


def recieve_bt(socket):
    data = bytearray()
    socket.settimeout(2)
    print("start recieve")
    while True:
        try:
            b = socket.recv(1024)
            if b.__len__() == 0:
                break
            data += b
        except Exception as e:
            print(e)
            break
    return data


def parse_input(data, socket):
    if data == b'send_screenshot':
        send_screenshot(socket)
    if data == b'get_screenshot':
        get_screenshot(socket)
    if data == b'send_file':
        send_file(socket)
    if data == b'get_file':
        get_file(socket)

def send_screenshot(socket):
    print("send_screenshot")
    data = recieve_bt(socket)

    print(len(data))
    image = Image.open(io.BytesIO(data))
    image.save("out_screenshot.png")
    print("ss saved")
    socket.send("ready")
    
def get_screenshot(socket):
    print("get_screenshot")

    screenshot = pyautogui.screenshot()
    screenshot.save("screenshot.png")
    data = image_to_byte_array(screenshot)
    print(data.__len__())
    socket.send(data)

def send_file(socket):
    print("send_file")
    filename = socket.recv(1024)
    print("filename", filename)
    data = recieve_bt(socket)
    print("file_data", data)
    file = open(filename, 'wb')
    file.write(data)
    file.close()
    socket.send("ready")


def get_file(socket):
    print("get_file")
    path = socket.recv(1024)
    file = open(path, "rb")
    if file == None:
        socket.send("error")
        return
    socket.send("ready")
    file_data = file.read()
    file.close()
    socket.send(file_data)
    data = socket.recv(1024)
    if data == b'ready':
        print("file sent success")



server_sock = BluetoothSocket(RFCOMM)
server_sock.bind(("", PORT_ANY))
server_sock.listen(1)

port = server_sock.getsockname()[1]

uuid = "58369c20-ecf6-11e3-ba36-82687f4fc15c"

advertise_service(server_sock, "SampleServer",
                    service_id=uuid,
                    service_classes=[uuid, SERIAL_PORT_CLASS],
                    profiles=[SERIAL_PORT_PROFILE]
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
