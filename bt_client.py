import sys

import bluetooth

local_mac = "e8:b1:fc:35:46:4c"

def print_menu():
    print("1.Send screenshot")
    print("2.Get screenshot")
    print("3.Send file")
    print("4.Get screenshot")

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
    data = socket.recv(1024)
    if data == "ready":
        screenshot = pyautogui.screenshot()
        socket.send(screenshot)
    
def get_screenshot(socket):
    socket.send("get_screenshot")
    data = socket.recv(1024)
    data.save("screenshot.png")

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
    return chosen_dev

chosen_dev = connect_to_dev()
sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
sock.connect((chosen_dev, 3))


while True:
    print_menu()
    cmd = int(input())
    choose_cmd(cmd, sock)

sock.close()