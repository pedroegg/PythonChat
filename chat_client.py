from socket import *
import _thread
from tkinter import *
import chat_utils as utils
import chat_interfaceChat as interfaceChat
import chat_interfaceLista as interfaceChatLista


def receberMensagens(atoa):
    while True:
        try:
            data = sockObj.recv(1024)
            if data:
                mensagemRecebida = utils.decryptMessage(data)
                if utils.checkEvent(mensagemRecebida, utils.NEWCLIENTEVENT):
                    nick = utils.pegarNickMensagem(mensagemRecebida)

                    interface.adicionarLabelCliente(nick)
                    interfaceLista.adicionarLabelCliente(nick)

                if utils.checkEvent(mensagemRecebida, utils.DISCONNECTEVENT):
                    nick = utils.pegarNickMensagem(mensagemRecebida)

                    interface.removerLabelCliente(nick)
                    interfaceLista.removerLabelCliente(nick)

                if utils.checkEvent(mensagemRecebida, utils.STOPPEDTYPINGEVENT):
                    nick = utils.pegarNickMensagem(mensagemRecebida)

                    interface.removerLabelDigitando(nick)

                    continue

                if utils.checkEvent(mensagemRecebida, utils.TYPINGEVENT):
                    nick = utils.pegarNickMensagem(mensagemRecebida)

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

    mensagem = utils.encryptMessage(utils.NEWCONNECTIONEVENT + ' ' + nickname)

    sockObj.sendall(mensagem)

    print("Enviado -> " + mensagem.decode('utf-8'))

    # sockObj.close()
    # root.quit()


serverHost = '0.tcp.sa.ngrok.io'

serverPort = 15264

nickname = 'Pedro Egg'

sockObj = socket(AF_INET, SOCK_STREAM)
sockObj.connect((serverHost, serverPort))

root = Tk()

root.title("Chat em grupo")

root.geometry("800x480")

interface = interfaceChat.InterfaceGrafica(root, sockObj)
interfaceLista = interfaceChatLista.InterfaceGrafica(sockObj)

# root.bind('<FocusIn>', interface.setarFocusInput)
root.after(100, iniciarThreadEscutar)

root.mainloop()
