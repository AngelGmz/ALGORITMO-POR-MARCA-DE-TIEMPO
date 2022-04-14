from tkinter import Tk, Label, Button
import tkinter.font as tkFont



class InterfazGrafica:
    def __init__(self, master):
        self.master = master

        titulo = tkFont.Font(family="Arial", size=18, weight="bold", slant="italic")
        boton = tkFont.Font(family="Arial", size=16, weight="bold")
        texto = tkFont.Font(family="Arial", size=16, weight="normal")

        master.title("Exclusión mutua: por marcas de tiempo")

        self.etiquetaProceso = Label(master, text="Proceso 1")
        self.etiquetaProceso.configure(font=titulo)
        self.etiquetaProceso.pack(padx=60,pady=10)
        
        self.etiqueta = Label(master, text="Estado: Sin acción")
        self.etiqueta.configure(font=texto)
        self.etiqueta.pack(padx=60,pady=10)
        self.cola1 = Label(master, text="Cola Zona Crítica 1[]")
        self.cola1.configure(font=texto)
        self.cola1.pack(padx=20,pady=10)
        self.cola2 = Label(master, text="Cola Zona Crítica 2[]")
        self.cola2.configure(font=texto)
        self.cola2.pack(padx=20,pady=10)
        self.lista_ok = Label(master, text="lista ok's[]")
        self.lista_ok.configure(font=texto)
        self.lista_ok.pack(padx=20,pady=10)

        self.botonSaludo = Button(master, text="Solicitar Zona crítica", command=self.saludar)
        self.botonSaludo.configure(font=boton)
        self.botonSaludo.pack(padx=20,pady=10)
        self.SalirSonaCritica = Button(master, text="Salir de a Zona crítica", command=self.saludar)
        self.SalirSonaCritica.configure(font=boton)
        self.SalirSonaCritica.pack(padx=20,pady=10)
        
    
    def saludar(self):
        print("¡Hey!")

