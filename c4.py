import socket
import sys
import threading
from tkinter import Tk
from InterfazGrafica import InterfazGrafica

#puerto_escucha = 50001
#puerto_envio = 50002


root = Tk()
InterfazGrafica(root, 50004, 50014, 4)
root.mainloop()


