import socket
import sys
import threading
from tkinter import Tk
from InterfazGrafica import InterfazGrafica

sport = 50001
dport = 50002

def listen():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('127.0.0.1', sport))

    while True:
        data = sock.recv(1024)
        print('\rpeer: {}\n> '.format(data.decode()), end='')

root = Tk()
InterfazGrafica(root)
root.mainloop()

listener = threading.Thread(target=listen, daemon=True);
listener.start()


# sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# sock.bind(('127.0.0.1', dport))

# while True:
#     opc = input('> ')
#     if opc == 1:
#         pass
#         #funcion
#     else:
#         sock.sendto(msg.encode(), ('127.0.0.1', 50003))

