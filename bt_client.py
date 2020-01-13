import bluetooth
from common import *

local_mac = "e8:b1:fc:35:46:4c"
serv_mac = "E4:70:B8:7A:69:A7"

def print_menu():
    print("1.Send screenshot")
    print("2.Get screenshot")
    print("3.Send file")
    print("4.Get file")

def choose_cmd(input, socket):
    if input == 1:
        send_screenshot_cl(socket)
    if input == 2:
        get_screenshot_cl(socket)
    if input == 3:
        send_file_cl(socket)
    if input == 4:
        get_file_cl(socket)

def send_screenshot_cl(socket):
    socket.send("send_screenshot")
    send_screenshot(socket)
    recv_ready(socket)
    
def get_screenshot_cl(socket):
    socket.send("get_screenshot")
    get_screenshot(socket)
    send_ready(socket)

def send_file_cl(socket):
    socket.send("send_file")
    print("input path")
    path = input()
    send_file(path, socket)
    recv_ready(socket)

def get_file(socket):
    socket.send("get_file")
    print("input remote path to file")
    path = input()
    socket.send(path)
    recv_file(socket)
    send_ready(socket)

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
