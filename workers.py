import asyncio
import datetime
import random
import bluetooth

sleep_time = 0.001
listen_port = 3
connected = False

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


async def server(server_sock, num, loop):
    print("accepting connection")
    try:
        print("accepting connection")
        # client_sock,address = server_sock.accept()
    except Exception as e:	
        print("Closing socket")
        client.close()
    print("accepted connection")
    while True:
        # data = client_sock.recv(1024)
        await asyncio.sleep(sleep_time)

async def client(client_sock, num, loop):
    chosen_dev = connect_to_dev()
    print("try to connect")
    try:
        client_sock.connect((chosen_dev, listen_port))
    except Exception as e:
        print("Closing socket")
        client_sock.close()
    global connected
    connected = True
    while True:
        print("Loop: {} Time: {}".format(num, datetime.datetime.now()))
        await asyncio.sleep(sleep_time)



def main():
    global listen_port
    # listen_port = 4
    server_sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )
    server_sock.bind(("",listen_port))
    server_sock.listen(4)
    
    client_sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )

    loop = asyncio.get_event_loop()
    loop.create_task(server(server_sock, 1, loop))
    loop.create_task(client(client_sock, 2, loop))

    loop.run_forever()

main()