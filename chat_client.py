from socket import *
import _thread
from tkinter import *
import chat_utils as utils
import chat_interfaceChat as interfaceChat
import chat_interfaceLista as interfaceChatLista

# Função que recebe as mensagens do socket da conexão e faz as ações necessárias


def receberMensagens(atoa):
    # Loop infinito para escutar o socket
    while True:
        try:
            # Recebendo a mensagem
            data = sockObj.recv(1024)
            if data:
                # Descriptografando
                mensagemRecebida = utils.decryptMessage(data)

                # Checagem do evento da mensagem (se é ou não e qual é o evento se for)
                if utils.checkEvent(mensagemRecebida, utils.PRIVATEMESSAGE):
                    nick = utils.pegarNickMensagem(mensagemRecebida, 1)

                    if interfaceLista.interface == None:
                        interfaceLista.abrirChatPrivado(nick)

                    interfaceLista.interface.inserirMensagemChat(
                        nick + ': ' + mensagemRecebida.split('}')[2])

                    continue

                if utils.checkEvent(mensagemRecebida, utils.NEWCLIENTEVENT):
                    nick = utils.pegarNickMensagem(mensagemRecebida, 1)

                    interface.adicionarLabelCliente(nick)
                    interfaceLista.adicionarLabelCliente(nick)

                if utils.checkEvent(mensagemRecebida, utils.GETCLIENTS):
                    nick = utils.pegarNickMensagem(mensagemRecebida, 1)

                    interface.adicionarLabelCliente(nick)
                    interfaceLista.adicionarLabelCliente(nick)

                    continue

                if utils.checkEvent(mensagemRecebida, utils.DISCONNECTEVENT):
                    nick = utils.pegarNickMensagem(mensagemRecebida, 1)

                    interface.removerLabelCliente(nick)
                    interfaceLista.removerLabelCliente(nick)

                if utils.checkEvent(mensagemRecebida, utils.STOPPEDTYPINGEVENT):
                    nick = utils.pegarNickMensagem(mensagemRecebida, 1)

                    interface.removerLabelDigitando(nick)

                    continue

                if utils.checkEvent(mensagemRecebida, utils.TYPINGEVENT):
                    nick = utils.pegarNickMensagem(mensagemRecebida, 1)

                    interface.setarLabelDigitando(nick)

                    continue

                # Mensagem recebida printada
                print("Recebi -> " + data.decode('utf-8'))

                # Se chegar aqui, a mensagem é inserida no chat de grupo
                interface.inserirMensagemChat(mensagemRecebida)
        except:
            # Caso ocorra algum erro, a conexão é finalizada e para o loop que escuta o socket
            break

            print('Finalizando thread de escutar mensagens')

            sockObj.close()

            _thread.exit()

# Thread que vai ficar atualizando a interface gráfica


def atualizarInterface(atoa):
    while True:
        root.update_idletasks()
        root.update()

# Função que inicia as threads que vão escutar o socket e atualizar a interface gráfica


def iniciarThreadEscutar():
    _thread.start_new_thread(atualizarInterface, tuple([25]))

    _thread.start_new_thread(receberMensagens, tuple([25]))

    # Mensagem enviada para o servidor ao conectar, passando o meu nickname
    mensagem = utils.encryptMessage(utils.NEWCONNECTIONEVENT + ' ' + nickname)

    # Comando que envia a mensagem
    sockObj.sendall(mensagem)

    print("Enviado -> " + mensagem.decode('utf-8'))

    # sockObj.close()
    # root.quit()


# Host
serverHost = '0.tcp.sa.ngrok.io'
# Porta do servidor
serverPort = 15264
# Nick
nickname = 'Pedro Egg'

# Declarando o socket
sockObj = socket(AF_INET, SOCK_STREAM)
sockObj.connect((serverHost, serverPort))

# Declarando e iniciando a interface gráfica
root = Tk()

root.title("Chat em grupo")

root.geometry("800x480")

# Interface Do chat em grupo
interface = interfaceChat.InterfaceGrafica(root, sockObj)
# Interface da lista de conectados
interfaceLista = interfaceChatLista.InterfaceGrafica(sockObj, nickname)

root.after(100, iniciarThreadEscutar)

root.mainloop()
