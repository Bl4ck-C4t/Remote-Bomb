import socket
from struct import unpack_from
import json

BOMB_PROT_ID = 0xC4C4
s1 = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(0x0003))
print("Listening for bomb frames...")
while True:
    all_data = s1.recv(80)

    layer2 = unpack_from("!6B6BH", all_data)
    if layer2[-1] != 0xc4c4:
        continue
    print("Received commands!")
    print(all_data)
    commands = json.loads(all_data[14:].decode())
    print(commands)

    print("Listening for bomb frames...")
