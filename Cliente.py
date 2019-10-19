from socket import *
import _thread
import threading
from time import strftime
from tkinter import *
from time import sleep


def getHorario():
    return strftime("%d/%m/%Y %H:%M:%S")


def pegarNickMensagem(mensagemParametro):
    nickRetorno = ''
    x = 0
    while mensagemParametro[x] != '{':
        x += 1
    x = x + 1
    while mensagemParametro[x] != '}':
        nickRetorno += mensagemParametro[x]
        x += 1

    return nickRetorno


def receberMensagens(atoa):
    while True:
        try:
            data = sockObj.recv(1024)
            if data:
                mensagemRecebida = descriptografar(data.decode('utf-8'))
                if 'xls8123476-213' in mensagemRecebida:
                    nick = pegarNickMensagem(mensagemRecebida)
                    interface.adicionarLabelCliente(nick)
                if 'xls8123476-208' in mensagemRecebida:
                    nick = pegarNickMensagem(mensagemRecebida)
                    interface.adicionarLabelClienteInicio(nick)
                    continue
                elif 'xls8123476-211' in mensagemRecebida:
                    nick = pegarNickMensagem(mensagemRecebida)
                    interface.removerLabelCliente(nick)
                elif 'xls8123476-210' in mensagemRecebida:
                    nick = pegarNickMensagem(mensagemRecebida)
                    interface.removerLabelDigitando(nick)
                    continue
                elif 'xls8123476-209' in mensagemRecebida:
                    nick = pegarNickMensagem(mensagemRecebida)
                    interface.setarLabelDigitando(nick)
                    continue
                print("Recebi -> " + data.decode('utf-8'))
                interface.inserirMensagemChat(mensagemRecebida)
        except:
            break
            print('Finalizando thread de escutar mensagens')
            sockObj.close()
            _thread.exit()


def atualizarInterface(atoa):
    while True:
        root.update_idletasks()
        root.update()


def iniciarThreadEscutar():
    _thread.start_new_thread(atualizarInterface, tuple([25]))
    _thread.start_new_thread(receberMensagens, tuple([25]))
    mensagem = criptografar('xls8123476-212 ' + nickname)
    sockObj.sendall(mensagem.encode('utf-8'))
    print("Enviado -> " + mensagem)

    # sockObj.close()
    # root.quit()


def criptografar(textoParametro):
    textoRetorno = ''
    kIterador = 0
    x = 0
    while x < len(textoParametro):
        textoRetorno = textoRetorno + chr(soma(ord(textoParametro[x]), ord(palavraChave[kIterador])))
        if kIterador < len(palavraChave)-1:
            kIterador = kIterador + 1
        else:
            kIterador = 0
        x = x + 1
    return textoRetorno


def descriptografar(textoParametro):
    textoRetorno = ''
    kIterador = 0
    x = 0
    while x < len(textoParametro):
        textoRetorno = textoRetorno + chr(subtrair(ord(textoParametro[x]), ord(palavraChave[kIterador])))
        if kIterador < len(palavraChave)-1:
            kIterador = kIterador + 1
        else:
            kIterador = 0
        x = x + 1
    return textoRetorno


def soma(valor1, valor2):

    if valor1 + valor2 > 126:
        valorReal = valor1
        for x in range(0, valor2, 1):
            if valorReal + 1 == 127:
                valorReal = 32
            else:
                valorReal = valorReal + 1
        return valorReal
    else:
        return valor1 + valor2


def subtrair(valor1, valor2):

    if valor1 - valor2 < 32:
        valorReal = valor1
        for x in range(0, valor2, 1):
            if valorReal - 1 == 31:
                valorReal = 126
            else:
                valorReal = valorReal - 1
        return valorReal
    else:
        return valor1 - valor2


class InterfaceGrafica:
    def __init__(self, master=None):
        self.corVerde = "color-" + 'green'
        self.corAzul = "color-" + 'blue'
        self.corCinza= "color-" + 'grey'
        self.labelsUsuarios = []
        self.labelsDigitando = []

        self.primeiraVez = True

        self.fontePadrao = ("Arial", "12")

        self.containerTitulo = Frame(master)
        self.containerTitulo.pack(anchor='nw', fill=X)

        self.tituloParticipantes = Label(self.containerTitulo, text="Participantes: ")
        self.tituloParticipantes["font"] = ("Arial", "14")
        self.tituloParticipantes.pack(side=LEFT)

        # self.separador = ttk.Separator(self.primeiroContainer, orient=HORIZONTAL)
        # self.separador.pack()

        self.separadorTituloChat = Frame(height=2, bd=5, bg='grey', relief=RAISED)
        self.separadorTituloChat.pack(fill=X)

        self.containerChat = Frame(height=350, bg='white')
        self.containerChat.pack(anchor='nw', fill=BOTH, expand=YES)

        self.containerScrollChat = Frame(self.containerChat, width=20, bg='black')
        self.containerScrollChat.pack(side=RIGHT, fill=Y)

        self.chatTextArea = Text(self.containerChat, bg='white', bd=2, font=self.fontePadrao, spacing1=2, spacing2=2, state=DISABLED,
                                 wrap=WORD, height=18)
        self.chatTextArea.pack(fill=BOTH, expand=YES)

        self.scrollBarChat = Scrollbar(self.containerScrollChat, command=self.chatTextArea.yview)
        self.scrollBarChat.pack(expand=YES, fill=BOTH)
        self.chatTextArea['yscrollcommand'] = self.scrollBarChat.set
        self.chatTextArea.tag_configure(self.corVerde, foreground='green')
        self.chatTextArea.tag_configure(self.corAzul, foreground='blue')

        self.separadorChatInput = Frame(height=25, bd=5, bg='#cbccc6', relief=FLAT)
        self.separadorChatInput.pack(fill=X)

        self.labelDigitando = Label(self.separadorChatInput, font=('Arial', '10'), bg='#cbccc6')
        self.labelDigitando.pack(side=LEFT, anchor='w', fill=X)

        self.containerInput = Frame(height=150, bg='white')
        self.containerInput.pack(anchor='nw', fill=BOTH, expand=YES)

        self.containerEnviarMensagem = Frame(self.containerInput, width=20, bg='white')
        self.containerEnviarMensagem.pack(side=RIGHT, fill=Y)

        self.containerScrollInput = Frame(self.containerInput, width=20, bg='white')
        self.containerScrollInput.pack(side=RIGHT, fill=Y)

        # sv = StringVar()
        # sv.trace_add("write", self.onTypeText)
        self.input = Text(self.containerInput, bd=1, bg='#e7e2e2', font=self.fontePadrao, spacing1=2, spacing2=2,
                          state=NORMAL, wrap=WORD, height=5)
        self.input.insert(END, 'Digite aqui sua mensagem...', self.corCinza)
        self.input.bind('<Return>', (lambda event: self.enviarMensagem()))
        self.input.bind('<FocusIn>', self.onFocusInput)
        self.input.bind('<FocusOut>', self.onFocusOutInput)
        self.input.bind('<Key>', self.onTypeText)
        self.input.pack(fill=BOTH, expand=YES)

        self.botaoEnviarMensagem = Button(self.containerEnviarMensagem, bg='grey', bd=2, width=5, font=self.fontePadrao, text="Enviar", command=self.enviarMensagem)
        self.botaoEnviarMensagem.pack(fill=BOTH, expand=YES)

        self.scrollBarInput = Scrollbar(self.containerScrollInput, command=self.input.yview)
        self.scrollBarInput.pack(expand=YES, fill=BOTH)
        self.input['yscrollcommand'] = self.scrollBarInput.set

    def adicionarLabelCliente(self, nickCliente):
        label = None
        if self.primeiraVez:
            label = Label(self.containerTitulo, text=nickCliente)
            self.primeiraVez = False
        else:
            label = Label(self.containerTitulo, text=',' + nickCliente)
        label["font"] = ("Arial", "14")
        label.pack(side=LEFT)
        self.labelsUsuarios.append(label)

    def adicionarLabelClienteInicio(self, nickCliente):
        label = Label(self.containerTitulo, text=',' + nickCliente)
        label["font"] = ("Arial", "14")
        label.pack(side=LEFT)
        self.labelsUsuarios.append(label)

    def removerLabelCliente(self, nickCliente):
        for x in self.labelsUsuarios:
            if x.cget('text') == nickCliente:
                x.pack_forget()
                self.labelsUsuarios.remove(x)

    def inserirMensagemChat(self, mensagem):
        textoDataHorario = getHorario() + ' - '
        if 'xls8123476-213' in mensagem:
            textoNickname = 'Cliente ' + pegarNickMensagem(mensagem) + ' conectado!'
            textoMensagem = ''
        elif 'xls8123476-211' in mensagem:
            textoNickname = 'Cliente ' + pegarNickMensagem(mensagem) + ' desconectou-se do chat!'
            textoMensagem = ''
        else:
            textoNickname = mensagem.split(': ', 1)[0] + ': '
            textoMensagem = mensagem.split(': ', 1)[1]
        self.chatTextArea.configure(state='normal')
        if len(self.chatTextArea.get('1.0', 'end-1c')) > 0:
            self.chatTextArea.insert(END, '\n' + textoDataHorario, self.corVerde)
        else:
            self.chatTextArea.insert(END, textoDataHorario, self.corVerde)
        self.chatTextArea.insert(END, textoNickname, self.corAzul)
        self.chatTextArea.insert(END, textoMensagem)
        self.chatTextArea.yview(END)
        self.chatTextArea.configure(state='disabled')
        self.input.focus_force()
        root.bell(displayof=0)

    def enviarMensagem(self):
        mensagem = criptografar(self.input.get('1.0', 'end-1c'))
        sockObj.sendall(mensagem.encode('utf-8'))
        print("Enviado -> " + mensagem)
        self.input.delete('1.0', 'end-1c')
        sockObj.sendall(criptografar('xls8123476-210').encode('utf-8'))
        return 'break'

    def setarLabelDigitando(self, nicknameDaPessoa):
        self.labelDigitando['text'] = nicknameDaPessoa + ' está digitando...'
        if nicknameDaPessoa not in self.labelsDigitando:
            self.labelsDigitando.append(nicknameDaPessoa)

    def removerLabelDigitando(self, nicknameDaPessoa):
        if nicknameDaPessoa in self.labelDigitando.cget('text'):
            if nicknameDaPessoa in self.labelsDigitando:
                self.labelsDigitando.remove(nicknameDaPessoa)
            if len(self.labelsDigitando) > 0:
                self.setarLabelDigitando(self.labelsDigitando[len(self.labelsDigitando)-1])
            else:
                self.labelDigitando['text'] = ''
        else:
            if nicknameDaPessoa in self.labelsDigitando:
                self.labelsDigitando.remove(nicknameDaPessoa)

    def onTypeText(self, event):
        if event.keysym == 'BackSpace' and len(self.input.get('1.0', 'end-1c')) == 1:
            sockObj.sendall(criptografar('xls8123476-210').encode('utf-8'))
        elif ('está digitando...' not in self.labelDigitando.cget('text')) and (len(self.input.get('1.0', 'end-1c'))) != 0:
            sockObj.sendall(criptografar('xls8123476-209').encode('utf-8'))
        self.input.yview(END)

    def onFocusInput(self, event):
        if self.input.get('1.0', 'end-1c') == 'Digite aqui sua mensagem...':
            self.input.delete('1.0', 'end-1c')

    def onFocusOutInput(self, event):
        if self.input.get('1.0', 'end-1c') != 'Digite aqui sua mensagem...':
            self.input.insert(END, 'Digite aqui sua mensagem...', self.corCinza)

    def setarFocusInput(self, event):
        self.input.focus_set()


serverHost = '0.tcp.ngrok.io'
serverPort = 11352
nickname = 'Pedro Egg'
palavraChave = 'Lampada'

sockObj = socket(AF_INET, SOCK_STREAM)
sockObj.connect((serverHost, serverPort))

root = Tk()
root.title("Chat do Egg")
root.geometry("800x480")
interface = InterfaceGrafica(root)
# root.bind('<FocusIn>', interface.setarFocusInput)
root.after(100, iniciarThreadEscutar)
root.mainloop()
