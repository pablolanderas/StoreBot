from dominio.Usuario import Usuario
from dominio.Producto import Producto
from dominio.Mensaje import Mensaje
from dominio.Peticion import Peticion
from dominio.Deseado import Deseado

from dataBase.DataBase import DataBase


class Gestor:

    dataBase : DataBase
    enBuclePrincipal : bool
    usuarios : dict[int:Usuario]
    productos : dict[int:Producto]
    funReporte = None
    funError = None

    def __init__(self, dataBase:DataBase, cargarGestor=True) -> None:
        # Check if the functions have been inicializated
        if None in (self.funReporte, self.funError):
            raise ModuleNotFoundError("The functions to report the Gestor hasnt been inicializated") 
        # Inicializate the class
        self.dataBase = dataBase
        self.usuarios = {}
        self.productos = {}

        # Get the DB data
        if cargarGestor:
            dataBase.loadGestorData(self)

    def getUserFromMessage(self, message: Mensaje) -> Usuario:
        # Return the user if exists
        if message.chatId in self.usuarios:
            return self.usuarios[message.chatId]
        # Create the new user
        user = Usuario(message.username, message.chatId)
        self.dataBase.saveUsuario(user)
        self.usuarios[user.chatId] = user
        self.funReporte(f"El usuario {user.username} con ID {user.chatId} se acaba de registrar")
        return user

    def deleteUsersMessages(self, user: Usuario) -> list[Mensaje]:
        messages = user.chatMessages.copy()
        user.chatMessages.clear()
        self.dataBase.deleteAllMensajesFromUsuario(user)
        return messages
    
    def saveMessage(self, message: Mensaje) -> None:
        user: Usuario = self.usuarios[message.chatId]
        if message not in user.chatMessages:
            user.chatMessages.append(message)
        self.dataBase.saveMensaje(message)

    def startProduct(self, user: Usuario, url: str) -> int:
        # Get the product
        try:
            prod = Producto.inicaProducto(url)
        except NotImplementedError: # Pagina no permitida
            return -1
        except ValueError: # Error en la pagina
            return -2
        # Check if the user have the product in a request
        if (fil:=list(filter(lambda x:x.producto == prod, user.peticiones.values()))):
            user.temporal = fil[0]
        # Else
        else:
            user.temporal = Peticion(user, prod)
        user.tagsTemporal = []
        return 0

    def saveTemporalRequest(self, user: Usuario):
        # Inicializate the data
        request: Peticion = user.temporal
        product: Producto = request.producto
        # Case product in the manager
        if product.id in self.productos.values():
            products :list[Producto] = self.productos.values()
            product = products[products.index(product)]
            request.producto = product
        # Else add the product
        else:
            self.dataBase.saveProducto(product)
        # Save the request in the DB
        if request.idPeticion is None:
            self.dataBase.savePeticion(request)
        # Add the request to the user
        user.peticiones[request.idPeticion] = request
        # Cear the temp
        user.temporal = None

