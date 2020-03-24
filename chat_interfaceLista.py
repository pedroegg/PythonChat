from socket import *
from tkinter import *
import _thread
import chat_utils as utils
import chat_interfaceChatWindow as interfaceChat


class InterfaceGrafica(Toplevel):
    def __init__(self, socket, mynick):
        self.sockObj = socket

        self.interface = None

        self.mynickname = mynick

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

    def adicionarLabelCliente(self, nickCliente):
        label = Label(self.containerLista, text=' "' + nickCliente + '" ',
                      borderwidth=2, relief="raised", width=200)

        label["font"] = ("Arial", "14")

        label.bind(
            "<Button-1>", lambda event, nickname=nickCliente: self.abrirChatPrivado(nickname))

        label.pack(side=TOP, anchor='center', fill=X)

        self.usuariosConectados.append(label)

    def removerLabelCliente(self, nickCliente):
        for x in self.usuariosConectados:
            nome = x.cget('text')

            lenReplace = len(nome.replace('"', ''))

            if nome.replace('"', '')[1:lenReplace-1] == nickCliente:
                x.pack_forget()

                self.usuariosConectados.remove(x)

    def abrirChatPrivado(self, nickname):
        print("nickname = ", nickname)
        print("mynickname = ", self.mynickname)
        if nickname != self.mynickname:
            self.interface = interfaceChat.InterfaceGrafica(
                nickname, self.mynickname, self.sockObj)
