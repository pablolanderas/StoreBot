from dominio.Deseado import Deseado
from dominio.Mensaje import Mensaje
from dominio.Peticion import Peticion
from dominio.Producto import Producto
from dominio.Usuario import Usuario
from dominio.Gestor import Gestor

from dataBase.DataBase import DataBase

from os import chdir

def main():

    # Move to the file directory
    dirAct = "\\".join(__file__.split("\\")[:-1])
    chdir(dirAct)

    DataBase.startDataBase("./dataBase/database.db", "./dataBase/database.sql")
    db = DataBase("./dataBase/database.db")
    Peticion.funcionNotificarUsuario = lambda x: print(x)

    user = Usuario("usuario", 23441)
    user.chatMessages.append(
        Mensaje(None, "Mensaje", user.chatId, user.username, 2)
    )
    user.chatMessages.append(
        Mensaje(None, "Mensjae", user.chatId, user.username, 1)
    )
    db.saveUsuario(user)
    prod = Producto.inicaProducto("https://www.zara.com/es/es/top-popelin-palabra-de-honor-abalorios-p00881007.html?v1=271552262")
    db.saveProducto(prod)
    req = Peticion(user, prod)
    req.notificacionPrecio = Mensaje(None, None, user.chatId, user.username, 223412)
    req.deseados.append(Deseado(None, None, ["tag1", "tag2", "tag3"], req))
    req.deseados.append(Deseado(None, Mensaje(None, None, None, None, 23445234), ["tag1", "tag2", "tag3", "tag4"], req))
    db.savePeticion(req)

    gestor = Gestor(db)

    for p in gestor.productos.values():
        print(p)

    print("-----------------------------------------------------------------")

    for u in gestor.usuarios.values(): 
        print(u, u.chatMessages)
        for p in u.peticiones.values():
            print(" ",p, "AVISO PRECIO:", p.notificacionPrecio)
            for d in p.deseados:
                print("     ", d)



if __name__ == "__main__":
    main()