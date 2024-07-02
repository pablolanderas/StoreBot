from dominio import Deseado, Mensaje, Peticion, Producto, Usuario, Gestor
from bot.StoreBot import StoreBot
from bot.botFunctions import funToDeleteMessage, funToSendAdvise, HTML_FORMAT
from constantes import BOT_TOKEN, ID_CHAT_AVISOS, ID_CHAT_ERRORES, TESTING, CREATE_DB

from dataBase.DataBase import DataBase
from os.path import exists

from os import chdir, path, kill, getpid, remove
from threading import Thread
from time import sleep
from signal import signal, SIGTERM, SIG_DFL

DIR_DATA= path.join("..", "data")
DIR_DATABASE = path.join(DIR_DATA, "database.db")
DIR_SQL = path.join(".", "dataBase", "database.sql")
DIR_AVISOS_MANTENIMIENTO = path.join(DIR_DATA, "avisosMantenimiento.txt")

def notifyAllUsersMaintenance(bot: StoreBot, gestor: Gestor):
    # Restaurar el manejador de señal
    signal(SIGTERM, SIG_DFL)
    # Enviar mensajes
    msj_txt = "El sistema se encuentra en mantenimiento, por favor espere unos minutos"
    mensajes = []
    for user in gestor.usuarios.values():
        foto = open(path.join(".", "resources", "mantenimiento.png"), "rb")
        bot.copyUsersMessagesToDelete(user)
        msj = bot.sendMessage(user, msj_txt, saveMessage=False, photo=foto, disableNotification=True)
        bot.deleteCopiedMessages(user)
        mensajes.append(f"{msj.chatId}={msj.messageId}")
    # Escribir el archivo
    with open(DIR_AVISOS_MANTENIMIENTO, "w") as file:
        file.write("\n".join(mensajes))
    # Llamar a la funcion original
    kill(getpid(), SIGTERM)

def restoreAllUsersMaintenance(bot: StoreBot):
    if path.exists(DIR_AVISOS_MANTENIMIENTO):
        with open(DIR_AVISOS_MANTENIMIENTO, "r") as file:
            for line in file.readlines():
                chatId, messageId = line.strip().split("=")
                msj = Mensaje(None, chatId=chatId, messageId=messageId)
                bot.deleteMessage(msj)
                bot.cmd_start(Usuario(None, chatId))
        remove(DIR_AVISOS_MANTENIMIENTO)

def main():
    
    # Start the database if not exists
    if not exists(DIR_DATABASE):
        if not CREATE_DB:
            print("[ERROR]: { The database not exists, and you not want create it, modify it in the .env }")
            exit(-1)
        DataBase.startDataBase(DIR_DATABASE, DIR_SQL)
        print("[INFO]:{ Database created }")

    # Inicialize the reporters
    Peticion.funcionNotificarUsuario = "TODO"
    Peticion.funcionEliminaNotificacion = "TODO"
    Gestor.funError = lambda obt, x: print("[ERROR]:{", x, "}")
    Gestor.funReporte = lambda obj, x: print("[INFO]:{", x, "}")

    # Load the database
    db = DataBase(DIR_DATABASE)
    # Load the database to the classes
    Peticion.dataBase = db
    # Initialize the gestor
    gestor = Gestor(db, False)
    # Initialize the bot
    bot = StoreBot(BOT_TOKEN, gestor)
    # Finalize the reportesrs
    Peticion.funcionNotificarUsuario = lambda peticion, message, codigo: funToSendAdvise(peticion, message, codigo, bot)
    Peticion.funcionEliminaNotificacion = lambda peticion, message: funToDeleteMessage(peticion, message, bot)
    gestor.funDelMessage = lambda message: bot.deleteMessage(message)
    gestor.funNotificateUser = lambda user, message: bot.sendMessage(user, message, parseMode=HTML_FORMAT)
    bot.notifyError = lambda obt, x: print("[ERROR]:{", x, "}")
    if not TESTING:
        # The users of the chats
        userAvisos = Usuario(None, ID_CHAT_AVISOS)
        userErrores = Usuario(None, ID_CHAT_ERRORES)
        funError = lambda obt, x: bot.sendMessage(userErrores, x, saveMessage=False, parseMode=HTML_FORMAT)
        Gestor.funError = funError
        bot.notifyError = funError
        Gestor.funReporte = lambda obj, x: bot.sendMessage(userAvisos, x, saveMessage=False, parseMode=HTML_FORMAT)
    # Create the threads
    Gestor.funReporte(Gestor, f"Inicialdo el bot")
    Gestor.funReporte(Gestor, f"Iniciando el gestor...")
    gestor.dataBase.loadGestorData(gestor)
    Gestor.funReporte(Gestor, f"Gestor iniciado")
    gestor_thread = Thread(target=gestor.startMainLoop)
    bot_thread = Thread(target=bot.infinity_polling)
    # Start the threads
    gestor_thread.start()
    Gestor.funReporte(Gestor, f"Gestor iniciado con el pid [{gestor_thread.ident}]")
    bot_thread.start()
    Gestor.funReporte(StoreBot, f"Bot iniciado con el pid [{bot_thread.ident}]")
    # Restore the messages
    restoreAllUsersMaintenance(bot)
    Gestor.funReporte(StoreBot, f"Reiniciados los chats")
    signal(SIGTERM, lambda x, y:notifyAllUsersMaintenance(bot, gestor))
    sleep(3)


if __name__ == "__main__":
    # Move to the file directory
    dirAct = path.dirname(path.abspath(__file__))
    chdir(dirAct)

    # Start the main function
    main()