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

def recieve_data(socket):
    len = int(socket.recv(1024))
    print(len)
    data = bytearray()
    # socket.settimeout(2)
    print("start recieve")
    while True:
        try:
            b = socket.recv(1024)
            data+=b
            if data.__len__() == len:
                break
        except Exception as e:
            print(e)
            break
    return data


def send_data(socket, data):
    socket.send(data.__len__())
    socket.send(data)

def send_screenshot(socket):
    screenshot = pyautogui.screenshot()
    screenshot.save("my_screenshot.png")
    data = image_to_byte_array(screenshot)
    send_data(socket, data)
    
def get_screenshot(socket):
    data = recieve_data(socket)
    print(len(data))
    image = Image.open(io.BytesIO(data))
    image.save("out_screenshot.png")
    print("screenshot saved")

def send_file(path, socket):
    file = open(path, "rb")
    filename = ntpath.basename(path)
    file_data = file.read()
    file.close()
    socket.send(filename)
    print("filename sent")
    send_data(socket, file_data)
    print("filedata sent")
    
def recv_file(socket):
    print("recieve filename")
    filename = socket.recv(1024)
    print("recieving file")
    data = recieve_data(socket)
    file = open(filename, 'wb')
    file.write(data)
    file.close()


def send_ready(socket):
    socket.send("ready")

def recv_ready(socket):
    data = socket.recv(1024)
    print(data)
    if data != b'ready':
        print("error send ss")
    else:
        print("send screenshot success")
