from socket import *
from tkinter import *
import chat_utils as utils

# Classe que manipula e mexe com a interface gráfica do chat de grupo


class InterfaceGrafica:
    def __init__(self, master=None, socket=None):
        self.master = master

        self.sockObj = socket

        self.corVerde = "color-" + 'green'
        self.corAzul = "color-" + 'blue'
        self.corCinza = "color-" + 'grey'

        self.labelsUsuarios = []
        self.labelsDigitando = []

        self.fontePadrao = ("Arial", "12")

        self.containerTitulo = Frame(master)
        self.containerTitulo.pack(anchor='nw', fill=X)

        self.tituloParticipantes = Label(
            self.containerTitulo, text="Participantes: ")
        self.tituloParticipantes["font"] = ("Arial", "14")
        self.tituloParticipantes.pack(side=LEFT)

        # self.separador = ttk.Separator(self.primeiroContainer, orient=HORIZONTAL)
        # self.separador.pack()

        self.separadorTituloChat = Frame(
            height=2, bd=5, bg='grey', relief=RAISED)
        self.separadorTituloChat.pack(fill=X)

        self.containerChat = Frame(height=350, bg='white')
        self.containerChat.pack(anchor='nw', fill=BOTH, expand=YES)

        self.containerScrollChat = Frame(
            self.containerChat, width=20, bg='black')
        self.containerScrollChat.pack(side=RIGHT, fill=Y)

        self.chatTextArea = Text(self.containerChat, bg='white', bd=2, font=self.fontePadrao, spacing1=2, spacing2=2, state=DISABLED,
                                 wrap=WORD, height=18)
        self.chatTextArea.pack(fill=BOTH, expand=YES)

        self.scrollBarChat = Scrollbar(
            self.containerScrollChat, command=self.chatTextArea.yview)
        self.scrollBarChat.pack(expand=YES, fill=BOTH)
        self.chatTextArea['yscrollcommand'] = self.scrollBarChat.set
        self.chatTextArea.tag_configure(self.corVerde, foreground='green')
        self.chatTextArea.tag_configure(self.corAzul, foreground='blue')

        self.separadorChatInput = Frame(
            height=25, bd=5, bg='#cbccc6', relief=FLAT)
        self.separadorChatInput.pack(fill=X)

        self.labelDigitando = Label(
            self.separadorChatInput, font=('Arial', '10'), bg='#cbccc6')
        self.labelDigitando.pack(side=LEFT, anchor='w', fill=X)

        self.containerInput = Frame(height=150, bg='white')
        self.containerInput.pack(anchor='nw', fill=BOTH, expand=YES)

        self.containerEnviarMensagem = Frame(
            self.containerInput, width=20, bg='white')
        self.containerEnviarMensagem.pack(side=RIGHT, fill=Y)

        self.containerScrollInput = Frame(
            self.containerInput, width=20, bg='white')
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

        self.botaoEnviarMensagem = Button(self.containerEnviarMensagem, bg='grey', bd=2,
                                          width=5, font=self.fontePadrao, text="Enviar", command=self.enviarMensagem)
        self.botaoEnviarMensagem.pack(fill=BOTH, expand=YES)

        self.scrollBarInput = Scrollbar(
            self.containerScrollInput, command=self.input.yview)
        self.scrollBarInput.pack(expand=YES, fill=BOTH)
        self.input['yscrollcommand'] = self.scrollBarInput.set

    # Função para adicionar o label de um novo conectado
    def adicionarLabelCliente(self, nickCliente):
        label = Label(self.containerTitulo, text=' "' + nickCliente + '" ')

        label["font"] = ("Arial", "14")

        label.pack(side=LEFT)

        self.labelsUsuarios.append(label)
    # Remover o label

    def removerLabelCliente(self, nickCliente):
        for x in self.labelsUsuarios:
            nome = x.cget('text')

            lenReplace = len(nome.replace('"', ''))

            if nome.replace('"', '')[1:lenReplace-1] == nickCliente:
                x.pack_forget()

                self.labelsUsuarios.remove(x)
    # Função que insere a mensagem recebida no chat de grupo

    def inserirMensagemChat(self, mensagem):
        textoDataHorario = utils.getHorario() + ' - '

        if utils.checkEvent(mensagem, utils.NEWCLIENTEVENT):
            textoNickname = 'Cliente ' + \
                utils.pegarNickMensagem(mensagem, 1) + ' conectado!'

            textoMensagem = ''

        elif utils.checkEvent(mensagem, utils.DISCONNECTEVENT):
            textoNickname = 'Cliente ' + \
                utils.pegarNickMensagem(mensagem, 1) + \
                ' desconectou-se do chat!'

            textoMensagem = ''

        else:
            mensagem = mensagem.replace('"', '')

            textoNickname = mensagem.split(': ', 1)[0] + ': '

            textoMensagem = mensagem.split(': ', 1)[1]

        self.chatTextArea.configure(state='normal')

        if len(self.chatTextArea.get('1.0', 'end-1c')) > 0:
            self.chatTextArea.insert(
                END, '\n' + textoDataHorario, self.corVerde)
        else:
            self.chatTextArea.insert(END, textoDataHorario, self.corVerde)

        self.chatTextArea.insert(END, textoNickname, self.corAzul)
        self.chatTextArea.insert(END, textoMensagem)

        self.chatTextArea.yview(END)

        self.chatTextArea.configure(state='disabled')

        self.input.focus_force()

        self.master.bell(displayof=0)
    # Função que envia a mensagem para o servidor

    def enviarMensagem(self):
        mensagem = utils.encryptMessage(
            '"' + self.input.get('1.0', 'end-1c') + '"')

        self.sockObj.sendall(mensagem)

        print("Enviado -> " + mensagem.decode('utf-8'))

        self.input.delete('1.0', 'end-1c')

        self.sockObj.sendall(utils.encryptMessage(utils.STOPPEDTYPINGEVENT))

        return 'break'
    # Funçao que coloca o label de digitando

    def setarLabelDigitando(self, nicknameDaPessoa):
        self.labelDigitando['text'] = nicknameDaPessoa + ' está digitando...'

        if nicknameDaPessoa not in self.labelsDigitando:

            self.labelsDigitando.append(nicknameDaPessoa)

    def removerLabelDigitando(self, nicknameDaPessoa):
        if nicknameDaPessoa in self.labelDigitando.cget('text'):
            if nicknameDaPessoa in self.labelsDigitando:
                self.labelsDigitando.remove(nicknameDaPessoa)

            if len(self.labelsDigitando) > 0:
                self.setarLabelDigitando(
                    self.labelsDigitando[len(self.labelsDigitando)-1])

            else:
                self.labelDigitando['text'] = ''

        else:
            if nicknameDaPessoa in self.labelsDigitando:
                self.labelsDigitando.remove(nicknameDaPessoa)
    # Função chamada após cada digitação de tecla

    def onTypeText(self, event):
        if event.keysym == 'BackSpace' and len(self.input.get('1.0', 'end-1c')) == 1:
            self.sockObj.sendall(utils.encryptMessage(
                utils.STOPPEDTYPINGEVENT))

        elif ('está digitando...' not in self.labelDigitando.cget('text')) and (len(self.input.get('1.0', 'end-1c'))) != 0:
            self.sockObj.sendall(utils.encryptMessage(utils.TYPINGEVENT))

        self.input.yview(END)

    def onFocusInput(self, event):
        if self.input.get('1.0', 'end-1c') == 'Digite aqui sua mensagem...':
            self.input.delete('1.0', 'end-1c')

    def onFocusOutInput(self, event):
        if self.input.get('1.0', 'end-1c') != 'Digite aqui sua mensagem...':
            self.input.insert(
                END, 'Digite aqui sua mensagem...', self.corCinza)

    def setarFocusInput(self, event):
        self.input.focus_set()
