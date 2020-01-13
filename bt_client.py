import sys
import bluetooth
import io
from PIL import Image
from PIL import ImageFile
import pyautogui
import ntpath
ImageFile.LOAD_TRUNCATED_IMAGES = True

def image_to_byte_array(image: Image):
  imgByteArr = io.BytesIO()
  image.save(imgByteArr, format='PNG')
  imgByteArr = imgByteArr.getvalue()
  return imgByteArr

local_mac = "e8:b1:fc:35:46:4c"
serv_mac = "E4:70:B8:7A:69:A7"

def recieve_bt(socket):
    data = bytearray()
    socket.settimeout(2)
    print("start recieve")
    while True:
        try:
            b = socket.recv(1024)
            if b.__len__() == 0:
                break
            data+=b
        except Exception as e:
            print(e)
            break
    return data

def print_menu():
    print("1.Send screenshot")
    print("2.Get screenshot")
    print("3.Send file")
    print("4.Get file")

def choose_cmd(input, socket):
    if input == 1:
        send_screenshot(socket)
    if input == 2:
        get_screenshot(socket)
    if input == 3:
        send_file(socket)
    if input == 4:
        get_file(socket)

def send_screenshot(socket):
    socket.send("send_screenshot")
    screenshot = pyautogui.screenshot()
    screenshot.save("my_screenshot.png")
    data = image_to_byte_array(screenshot)
    print(data.__len__())
    socket.send(data)
    data = socket.recv(1024)
    print(data)
    if data != b'ready':
        print("error send ss")
    else:
        print("send screenshot success")
    
def get_screenshot(socket):
    socket.send("get_screenshot")
    data = recieve_bt(socket)
    print(len(data))
    image = Image.open(io.BytesIO(data))
    image.save("out_screenshot.png")
    print("ss saved")

def send_file(socket):
    socket.send("send_file")
    print("input path")
    path = input()
    file = open(path, "rb")
    filename = ntpath.basename(path)
    file_data = file.read()
    file.close()
    socket.send(filename)
    socket.send(file_data)
    data = socket.recv(1024)
    if data != b'ready':
        print("error send file")
        return
    else:
        print("send file success")
    #добавить отправку файла

def get_file(socket):
    socket.send("get_file")
    print("input remote path to file")
    path = input()
    filename = ntpath.basename(path)
    socket.send(path)
    data = socket.recv(1024)
    if data == b'ready':
        print("recieving file")
        data = recieve_bt(socket)
        file = open(filename, 'wb')
        file.write(data)
        file.close()
        socket.send("ready")
        print("file recieved")
    else:
        print(encode(data))

    #добавить сохранение файла файла

def connect_to_dev():
    nearby_devices = bluetooth.discover_devices()
    i = 1
    port = 1
    for bdaddr in nearby_devices:
        print(i,'.',bluetooth.lookup_name(bdaddr))
        i = i + 1
    dev_index = -1
    dev_num = nearby_devices.__len__()
    while(dev_index>dev_num or dev_index<0):
        print("choose device to connect")
        dev_index = int(input())
    chosen_dev = nearby_devices[dev_index-1]
    print(chosen_dev)
    return chosen_dev

# chosen_dev = connect_to_dev()
sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
sock.connect((serv_mac, 1))
print("connected")

try:
    while True:
        # sock.send("hello")
        # print("send")
        # data = sock.recv(1024)
        # print("recv ",data)
        print_menu()
        cmd = int(input())
        choose_cmd(cmd, sock)
except Exception as e:
    print(e)
sock.close()