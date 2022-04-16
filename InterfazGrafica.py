from asyncio.windows_events import NULL
import re
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
    estado = []
    cola_zona_1 = []
    cola_zona_2 = []
    numero_oks_zona1 = 0
    numero_oks_zona2 = 0
    sock = NULL
    solicita_zona  = 'Solicita Zona Crítica 1'
    solicita_zona2 = 'Solicita Zona Crítica 2'
    en_zona = 'En Zona Crítica 1'
    en_zona2 = 'En Zona Crítica 2'
    sin_accion = 'Sin Acción'

    def __init__(self, master, puerto_escucha,puerto_envio, mi_id, reloj_inicial ):
        self.reloj_logico = reloj_inicial
        self.estado = [self.sin_accion,self.sin_accion]

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
        self.lblEstado = Label(master, text='')
        self.lblEstado.config(text=f'{self.estado[0]},{self.estado[1]}')
        self.lblEstado.configure(font=texto)
        self.lblEstado.pack(padx=60,pady=10)
        self.cola1 = Label(master, text="Cola Zona Crítica 1[]")
        self.cola1.configure(font=texto)
        self.cola1.pack(padx=20,pady=10)
        self.cola2 = Label(master, text="Cola Zona Crítica 2[]")
        self.cola2.configure(font=texto)
        self.cola2.pack(padx=20,pady=10)

        self.lista_ok = Label(master, text="lista ok'")
        self.lista_ok.configure(font=textoBold)
        self.lista_ok.pack(padx=20,pady=10)

        self.lista_ok1 = Label(master, text=self.numero_oks_zona1)
        self.lista_ok1.configure(font=texto)
        self.lista_ok1.pack(padx=60,pady=10)
        self.lista_ok2 = Label(master, text=self.numero_oks_zona2)
        self.lista_ok2.configure(font=texto)
        self.lista_ok2.pack(padx=60,pady=10)

        self.botonZonaCritica = Button(master, text="→ Solicitar Zona crítica 1", command=self.solicitar_zona1)
        self.botonZonaCritica.configure(font=boton)
        self.botonZonaCritica.pack(padx=20,pady=10)
        self.botonZonaCritica2 = Button(master, text="→ Solicitar Zona crítica 2", command=self.solicitar_zona2)
        self.botonZonaCritica2.configure(font=boton)
        self.botonZonaCritica2.pack(padx=20,pady=10)
        self.SalirSonaCritica = Button(master, text="← Salir de a Zona crítica", command=self.salir_de_zona_actual)
        self.SalirSonaCritica.configure(font=boton)
        self.SalirSonaCritica.pack(padx=20,pady=10) 
        self.SalirSonaCritica2 = Button(master, text="← Salir de a Zona crítica 2", command=self.salir_de_zona_actual)
        self.SalirSonaCritica2.configure(font=boton)
        self.SalirSonaCritica2.pack(padx=20,pady=10) 
    
    def solicitar_zona1(self):
        if self.estado[0] == self.solicita_zona or self.estado[0] == self.en_zona:
                return
        self.estado[0] = self.solicita_zona
        self.lblEstado.config(text=f'{self.estado[0]},{self.estado[1]}')
        msg =f'{str(self.mi_id)},{self.solicita_zona},{self.reloj_logico},1'
        self.reloj_logico += 1
        self.enviar_mensaje_a_todos(msg)

    def solicitar_zona2(self):
        if self.estado[1] == self.solicita_zona or self.estado[1] == self.en_zona:
                return
        self.estado[1] = self.solicita_zona2
        self.lblEstado.config(text=f'{self.estado[0]},{self.estado[1]}')
        msg =f'{str(self.mi_id)},{self.solicita_zona},{self.reloj_logico},2'
        self.reloj_logico += 1
        self.enviar_mensaje_a_todos(msg)
        
    
    def enviar_mensaje_a_todos(self, msg):
        for i in self.NODOS_ENVIO:
            self.sock.sendto(msg.encode(), ('127.0.0.1', i))

    
    def salir_de_zona_actual():
        pass
   
    def responderMensajeOk(self,id_proceso, m_zona_pedida, reloj_logico):
        print(id_proceso,m_zona_pedida,reloj_logico)
        if m_zona_pedida == '1':
            if self.estado[0] == self.en_zona:
                print('estoy en zona')
                print('encola')
                #encola
                return
            if self.estado[0] == self.sin_accion:
                msg =f'{str(self.mi_id)},ok, {m_zona_pedida}'
                self.sock.sendto(msg.encode(), ('127.0.0.1', self.NODOS_ENVIO[int(id_proceso)]))
                return

            if  int(self.reloj_logico) > int(reloj_logico):
                msg =f'{str(self.mi_id)},ok, {m_zona_pedida}'
                self.sock.sendto(msg.encode(), ('127.0.0.1', self.NODOS_ENVIO[int(id_proceso)]))
                return
            
            print('encola')
        if m_zona_pedida == '2':
            if self.estado[1] == self.en_zona:
                print('encola')
                return
            if self.estado[1] == self.sin_accion:
                msg =f'{str(self.mi_id)},ok, {m_zona_pedida}'
                self.sock.sendto(msg.encode(), ('127.0.0.1', self.NODOS_ENVIO[int(id_proceso)]))
                return

            if  int(self.reloj_logico) > int(reloj_logico):
                msg =f'{str(self.mi_id)},ok, {m_zona_pedida}'
                self.sock.sendto(msg.encode(), ('127.0.0.1', self.NODOS_ENVIO[int(id_proceso)]))
                return
            
            print('encola')

    def actualziar_interfaz(self):
        self.lblEstado.config(text=f'{self.estado[0]},{self.estado[1]}')
        self.marcaTiempo.config(text=f'Reloj lógico: {self.reloj_logico}')
        self.lista_ok1.config(text=f'ok zona 1: {self.numero_oks_zona1}')
        self.lista_ok2.config(text=f'ok zona 2: {self.numero_oks_zona2}')
    
    def listen(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(('127.0.0.1', self.puerto_escucha))

        while True:
            data = sock.recv(1024)
            print('\rpeer: {}\n> '.format(data.decode()), end='')
            msg_rep = data.decode()
            msg_array = msg_rep.split(',')
            if msg_array[1] == self.solicita_zona:
                m_id_prceso_remitente = msg_array[0]
                m_reloj_logico = msg_array[2]
                m_zona_pedida = msg_array[3]
                self.responderMensajeOk(m_id_prceso_remitente, m_zona_pedida, m_reloj_logico)
            
            if msg_array[1] == 'ok':
                print(msg_array[2])
                if int(msg_array[2]) == 1:
                    print(msg_array[2])
                    self.numero_oks_zona1 += 1
                    if self.numero_oks_zona1 >= 6:
                        self.estado[0] = self.en_zona
                else:
                    #print(msg_array[2],'en zona 2')
                    self.numero_oks_zona2 += 1
                    if self.numero_oks_zona2 >= 6:
                            self.estado[1] = self.en_zona2
            self.actualziar_interfaz()



            


   