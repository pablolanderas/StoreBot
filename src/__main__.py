from dominio import Deseado, Mensaje, Peticion, Producto, Usuario, Gestor
from bot.StoreBot import StoreBot
from bot.botFunctions import funToDeleteMessage, funToSendAdvise, HTML_FORMAT
from constantes.Constantes import BOT_TOKEN

from dataBase.DataBase import DataBase

from os import chdir
from threading import Thread

def main(checkDB):

    if checkDB:
        # Inicializate the reporters
        Peticion.funcionNotificarUsuario = lambda x: print(x)
        Gestor.funError = lambda obj, x: print("[ERROR]:{", x, "}")
        Gestor.funReporte = lambda obj, x: print("[INFO]:{", x, "}")

        DataBase.startDataBase("./dataBase/database.db", "./dataBase/database.sql")
        db = DataBase("./dataBase/database.db")

    else:
        # Inicialize the reporters
        Peticion.funcionNotificarUsuario = "TODO"
        Peticion.funcionEliminaNotificacion = "TODO"
        Gestor.funError = lambda obt, x: print("[ERROR]:{", x, "}")
        Gestor.funReporte = lambda obj, x: print("[INFO]:{", x, "}")

        # Load the database
        db = DataBase("./dataBase/database.db")
        # Load the database to the classes
        Peticion.dataBase = db
        # Initialize the gestor
        gestor = Gestor(db)
        # Initialize the bot
        bot = StoreBot(BOT_TOKEN, gestor)
        # Finalize the reportesrs
        Peticion.funcionNotificarUsuario = lambda peticion, message, codigo: funToSendAdvise(peticion, message, codigo, bot)
        Peticion.funcionEliminaNotificacion = lambda peticion, message: funToDeleteMessage(peticion, message, bot)
        gestor.funDelMessage = lambda message: bot.deleteMessage(message)
        gestor.funNotificateUser = lambda user, message: bot.sendMessage(user, message, parseMode=HTML_FORMAT)
        # Create the threads
        gestor_thread = Thread(target=gestor.startMainLoop)
        # Start the threads
        gestor_thread.start()
        bot.infinity_polling()
        gestor_thread.join(timeout=1)


if __name__ == "__main__":
    # Move to the file directory
    dirAct = "\\".join(__file__.split("\\")[:-1])
    chdir(dirAct)

    # Execute the main
    #main(checkDB=True)
    main(checkDB=False)