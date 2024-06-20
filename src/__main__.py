from dominio import Deseado, Mensaje, Peticion, Producto, Usuario, Gestor
from bot.StoreBot import StoreBot
from bot.botFunctions import funToDeleteMessage, funToSendAdvise, HTML_FORMAT
from constantes import BOT_TOKEN, ID_CHAT_AVISOS, ID_CHAT_ERRORES

from dataBase.DataBase import DataBase
from os.path import exists

from os import chdir, path, getcwd
from threading import Thread
from time import sleep
from sys import argv

DIR_DATABASE = path.join(".", "dataBase", "database.db")
DIR_SQL = path.join(".", "dataBase", "database.sql")

def main(test=False):

    # Start the database if not exists
    if not exists(DIR_DATABASE):
        # Obtener el path completo de la direccion actual mas DIR_DATABASE
        dirFInal = path.join(getcwd(), path.normpath(DIR_DATABASE))
        resp = input("[INFO]:{No existe la base de datos en \""+dirFInal+"\", escribe \"y\" para crearla}")
        if resp.lower() != "y":
            print("[INFO]:{Creacion de base de datos cancelada}")
            return
        DataBase.startDataBase(DIR_DATABASE, DIR_SQL)
        print("[INFO]:{Database created}")

    # Inicialize the reporters
    Peticion.funcionNotificarUsuario = "TODO"
    Peticion.funcionEliminaNotificacion = "TODO"
    Gestor.funError = lambda obt, x: print("[ERROR]:{", x, "}")
    Gestor.funReporte = lambda obj, x: print("[INFO]:{", x, "}")

    # Load the database
    db = DataBase(path.join(".", "dataBase", "database.db"))
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
    if not test:
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
    sleep(3)
    if test:
        input("[ Press enter to stop the bot ]\n")
        bot.stop_polling()
        gestor.stopMainLoop()


if __name__ == "__main__":
    # Move to the file directory
    dirAct = path.dirname(path.abspath(__file__))
    chdir(dirAct)

    # Execute the main
    tests = False
    if len(argv) > 1:
        if argv[1] == "test":
            tests = True
        else:
            print("[ERROR]:{Argumento invalido}")
            exit(1)
    main(tests)