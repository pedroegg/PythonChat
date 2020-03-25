from socket import *
from tkinter import *
import _thread
import chat_utils as utils
import chat_interfaceChatWindow as interfaceChat


class InterfaceGrafica(Toplevel):
    def __init__(self, socket):
        self.sockObj = socket
        self.interface = None

        Toplevel.__init__(self)
        self.geometry("200x480+1100+100")
        self.title("Lista Usuários")

        self.usuariosConectados = []

        self.fontePadrao = ("Arial", "12")

        self.containerTitulo = Frame(self)
        self.containerTitulo.pack(anchor='center', fill=X)

        self.tituloParticipantes = Label(
            self.containerTitulo, text="Usuários Online: ")
        self.tituloParticipantes["font"] = ("Arial", "14")
        self.tituloParticipantes.pack(side=TOP)

        # self.separador = ttk.Separator(self.primeiroContainer, orient=HORIZONTAL)
        # self.separador.pack()

        self.separadorTituloLista = Frame(
            self, height=2, bd=5, bg='grey', relief=RAISED)
        self.separadorTituloLista.pack(fill=X)

        self.containerLista = Frame(self, width=200)
        self.containerLista.pack(anchor='n', fill=Y, expand=YES)

        """

        self.containerScrollLista = Frame(
            self.containerLista, width=20, bg='black')
        self.containerScrollLista.pack(side=RIGHT, fill=Y)

        self.scrollBarLista = Scrollbar(
            self.containerScrollLista, command=self.containerLista.yview)
        self.scrollBarLista.pack(expand=YES, fill=BOTH)

        self.containerLista['yscrollcommand'] = self.scrollBarLista.set
        
        """

    def adicionarLabelCliente(self, nickCliente):
        label = Label(self.containerLista, text=nickCliente,
                      borderwidth=2, relief="raised", width=200)

        label["font"] = ("Arial", "14")

        label.bind(
            "<Button-1>", lambda event, nickname=nickCliente: self.abrirChatPrivado(nickname))

        label.pack(side=TOP, anchor='center', fill=X)

        self.usuariosConectados.append(label)

    def removerLabelCliente(self, nickCliente):
        for x in self.labelsUsuarios:
            if x.cget('text') == nickCliente:
                x.pack_forget()

                self.usuariosConectados.remove(x)

    def abrirChatPrivado(self, nickname):
        self.interface = interfaceChat.InterfaceGrafica(
            str(nickname), self.sockObj)
