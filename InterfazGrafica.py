from asyncio.windows_events import NULL
from tkinter import Tk, Label, Button
import tkinter.font as tkFont
import socket
import sys
import threading

#puerto_escucha = 50001
#puerto_envio = 50002

class InterfazGrafica:
    NODOS_ENVIO = [50001,50002,50003,50004,50005,50006]
    mi_id = 0
    puerto_escucha = 0
    puerto_envio = 0
    reloj_logico = 0
    estado = 'sin accion'
    cola_zona_1 = []
    cola_zona_2 = []
    lista_oks = []
    sock = NULL
    solicita_zona  = 'Solicita Zona Crítica 1'
    solicita_zona2 = 'Solicita Zona Crítica 2'
    sin_accion = 'Sin Acción'
    en_zona1 = 'En Zona Crítica 1'
    en_zona2 = 'En Zona Crítica 2'
    def __init__(self, master, puerto_escucha,puerto_envio, mi_id ):


        self.puerto_escucha = puerto_escucha
        self.puerto_envio = puerto_envio
        self.mi_id = mi_id-1

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(('127.0.0.1', self.puerto_envio))

        listener = threading.Thread(target=self.listen, daemon=True);
        listener.start()
        self.master = master

        titulo = tkFont.Font(family="Arial", size=18, weight="bold", slant="italic")
        boton = tkFont.Font(family="Arial", size=16, weight="bold")
        texto = tkFont.Font(family="Arial", size=16, weight="normal")
        textoBold = tkFont.Font(family="Arial", size=16, weight="bold")

        master.title("Exclusión mutua: por marcas de tiempo")

        self.etiquetaProceso = Label(master, text='Proceso {}'.format(self.mi_id+1))
        self.etiquetaProceso.configure(font=titulo)
        self.etiquetaProceso.pack(padx=60,pady=10)
        
        self.marcaTiempo = Label(master, text="Reloj Lógico: 0")
        self.marcaTiempo.configure(font=texto)
        self.marcaTiempo.pack(padx=60,pady=10)
        
        self.etiqueta = Label(master, text="Estado:")
        self.etiqueta.configure(font=textoBold)
        self.etiqueta.pack(padx=60,pady=10)
        self.lblEstado = Label(master, text=self.sin_accion)
        self.lblEstado.configure(font=texto)
        self.lblEstado.pack(padx=60,pady=10)
        self.cola1 = Label(master, text="Cola Zona Crítica 1[]")
        self.cola1.configure(font=texto)
        self.cola1.pack(padx=20,pady=10)
        self.cola2 = Label(master, text="Cola Zona Crítica 2[]")
        self.cola2.configure(font=texto)
        self.cola2.pack(padx=20,pady=10)
        self.lista_ok = Label(master, text="lista ok's[]")
        self.lista_ok.configure(font=texto)
        self.lista_ok.pack(padx=20,pady=10)

        self.botonZonaCritica = Button(master, text="→ Solicitar Zona crítica 1", command=self.solicitar_zona_1)
        self.botonZonaCritica.configure(font=boton)
        self.botonZonaCritica.pack(padx=20,pady=10)
        self.botonZonaCritica2 = Button(master, text="→ Solicitar Zona crítica 2", command=self.solicitar_zona_2)
        self.botonZonaCritica2.configure(font=boton)
        self.botonZonaCritica2.pack(padx=20,pady=10)
        self.SalirSonaCritica = Button(master, text="← Salir de a Zona crítica", command=self.enviar_todos)
        self.SalirSonaCritica.configure(font=boton)
        self.SalirSonaCritica.pack(padx=20,pady=10) 

    def solicitar_zona_1(self):
        if self.estado == self.solicita_zona or self.estado == self.en_zona1:
            return
        self.estado = self.solicita_zona
        self.lblEstado.config(text=self.estado)
        msg =f'{str(self.mi_id)},{self.solicita_zona},{self.reloj_logico},{1}'
        for i in self.NODOS_ENVIO:
            self.sock.sendto(msg.encode(), ('127.0.0.1', i))
    
    def solicitar_zona_2(self):
        if self.estado == self.solicita_zona2 or self.estado == self.en_zona2:
            return
        self.estado = self.solicita_zona2
        self.lblEstado.config(text=self.estado)
        msg =f'{str(self.mi_id)},{self.solicita_zona2},{self.reloj_logico},{2}'
        for i in self.NODOS_ENVIO:
            self.sock.sendto(msg.encode(), ('127.0.0.1', i))

    def responderMensajeOk(self,id_proceso, accion):
        if self.estado != self.solicita_zona and self.estado != self.en_zona:
            msg =f'{str(self.mi_id)},{self.solicita_zona},ok'
            self.sock.sendto(msg.encode(), ('127.0.0.1', self.NODOS_ENVIO[id_proceso]))

    def saludar(self):
        print("¡Hey!")

    def listen(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(('127.0.0.1', self.puerto_escucha))

        while True:
            data = sock.recv(1024)
            print('\rpeer: {}\n> '.format(data.decode()), end='')
            msg_rep = data.decode()
            msg_array = msg_rep.split(',')
            if msg_array[1] == self.solicita_zona:
                id_prceso_remitente = msg_array[0]

                self.responderMensajeOk(id_prceso_remitente)

            


   