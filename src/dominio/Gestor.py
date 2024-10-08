from dominio.Usuario import Usuario 
from dominio.Producto import Producto
from dominio.Mensaje import Mensaje
from dominio.Peticion import Peticion
from dominio.Deseado import Deseado
from bot.botFunctions import enclace_html
from traceback import format_exception
from time import sleep

from dataBase.DataBase import DataBase
from bot.botFunctions import enclace_html


class Gestor:

    dataBase : DataBase
    enBuclePrincipal : bool
    usuarios : dict[int:Usuario]
    productos : dict[int:Producto]
    funReporte = None
    funError = None
    funDelMessage = None
    funNotificateUser = None

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
            user = self.usuarios[message.chatId]
            # Update the username if changed
            if user.username != message.username:
                user.username = message.username
                self.dataBase.updateUsuarioUsername(user)
            return user
        # Create the new user
        user = Usuario(message.username, message.chatId)
        self.dataBase.saveUsuario(user)
        self.usuarios[user.chatId] = user
        self.funReporte(f"El usuario {user.username} con ID {user.chatId} se acaba de registrar")
        return user

    def deleteUsersMessages(self, user: Usuario) -> list[Mensaje]:
        messages = user.chatMessages.copy()
        self.dataBase.deleteAllMensajesFromUsuario(user)
        return messages
    
    def saveMessage(self, message: Mensaje) -> None:
        user: Usuario = self.usuarios[message.chatId]
        if message not in user.chatMessages:
            user.chatMessages.append(message)
        self.dataBase.saveMensaje(message)

    def saveNotification(self, message: Mensaje) -> None:
        user: Usuario = self.usuarios[message.chatId]
        if message not in user.notifications:
            user.notifications.append(message)
        self.dataBase.saveNotificacion(message)

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
        if product in self.productos.values():
            products :list[Producto] = list(self.productos.values())
            product = products[products.index(product)]
            request.producto = product
        # Else add the product
        else:
            self.dataBase.saveProducto(product)
            self.productos[product.id] = product
            self.funReporte(f"Se ha añadido el producto {product}")
        # Save the request in the DB
        if request.idPeticion is None:
            self.dataBase.savePeticion(request)
            self.funReporte(f"El {user} ha añadido la petición {request}")
        else:
            for wished in self.dataBase.getWishedsForRequest(request):
                if wished.mensaje:
                    self.funDelMessage(wished.mensaje)
            self.dataBase.updatePeticion(request)
            self.funReporte(f"El {user} ha actualizado la petición {request}")
        # Add the request to the user
        user.peticiones[request.idPeticion] = request
        # Cear the temp
        user.temporal = None

    def removeRequest(self, user: Usuario, idPeticion: int):
        # Get the request and the product
        request: Peticion = user.peticiones[idPeticion]
        product = request.producto
        # Remove the request
        del user.peticiones[idPeticion]
        # Delete the messges from the request
        if request.notificacionPrecio:
            self.funDelMessage(request.notificacionPrecio)
        for wished in request.deseados:
            if wished.mensaje:
                self.funDelMessage(wished.mensaje)
        # Delete the request from the DB
        self.dataBase.deletePeticion(request)
        self.funReporte(f"Se ha eliminado la petición {request}")
        # Delete the product if isnt in other request
        if not self.dataBase.checkIfProductInRequest(request.producto):
            del self.productos[product.id]
            self.dataBase.deleteProducto(product)
            self.funReporte(f"Se ha eliminado el producto {product} porque no tiene más peticiones")

    def deleteNotification(self, user: Usuario, idPeticion: int, idDeseado: str):
        # Get the request
        request = user.peticiones[idPeticion]
        # If the notification is the price
        if idDeseado == "precio":
            msg = request.notificacionPrecio
            # Delete in the db
            request.notificacionPrecio = None
            self.dataBase.deletePeticionPriceMessage(request)
            # Delete the notification
            self.funDelMessage(msg)
            return
        else:
            idDeseado = int(idDeseado)
        # Get the notification
        filtrate = list(filter(lambda x: x.idDeseado==idDeseado, request.deseados))
        if not filtrate: return
        deseado = filtrate[0]
        msg = deseado.mensaje
        # Delete the notification in the db
        deseado.mensaje = None
        self.dataBase.updateDeseado(deseado)
        # Delete the notification from the request
        deseado.mensaje = None
        # Delete the notification
        self.funDelMessage(msg)

    def deleteWished(self, user: Usuario, idPeticion: int, idDeseado: str):
        # Get the request
        request = user.peticiones[idPeticion]
        # Get the wished
        filtrate = list(filter(lambda x: x.idDeseado==idDeseado, request.deseados))
        if not filtrate: return
        deseado: Deseado = filtrate[0]
        # Delete the notification if exists
        if deseado.mensaje:
            self.funDelMessage(deseado.mensaje)
        # Delete the wished
        request.deseados.remove(deseado)
        self.dataBase.deleteDeseado(deseado)

    def startMainLoop(self, pintaActualizaciones=False):
        self.enBuclePrincipal = True
        while self.enBuclePrincipal:
            # Update the products
            for key in list(self.productos.keys()).copy():
                product = self.productos.get(key)
                if product:
                    try:
                        resp = product.actualiza()
                        if not resp:
                            self.funError(f"<b>Error en el bucle de productos</b>\nError al actualizar el producto {product} por un problema de conexión")
                        elif pintaActualizaciones: print(f"[Actualizado]: {product}")
                    except Exception as e:
                        self.mannageUpdateProductError(e, product, key)
            # Check the requests
            for key in self.usuarios.keys():
                user = self.usuarios.get(key)
                for key in list(user.peticiones.keys()).copy():
                    request = user.peticiones.get(key)
                    try:
                        result = request.comprueba()
                        # Save in the db
                        if result:
                            self.dataBase.updatePeticion(request)
                    except Exception as e:
                        self.mannageCheckRequestError(e, request, user)
            # Wait 1 minute
            sleep(60)

    def mannageUpdateProductError(self, error: Exception, product: Producto, productKey: int):
        # Delete the requests of the product and notify the user
        for key in self.usuarios.keys():
                user: Usuario = self.usuarios.get(key)
                requests = list(user.peticiones.values()).copy()
                productRequests = list(filter(lambda x: x.producto == product, requests))
                for request in productRequests:
                    self.removeRequest(user, request.idPeticion)
                    text = f"El producto {product} con ID {productKey} se ha eliminado por un error"
                    self.funNotificateUser(user, text)      
        # Notificate the error
        errList = format_exception(type(error), error, error.__traceback__)
        errList.insert(0, errList[-1])
        text =  f"<b>Error en el bucle de productos</b>\n"
        text += f"Se eliminio el producto: {product}\n"
        text += f"Con URL {enclace_html(product.url, product.url)}\n"
        text += f"Con ID {productKey}\n"
        text += f"Error: \n{''.join(errList[:-1])}"
        text += "\n----------------"

        self.funError(text)

    def mannageCheckRequestError(self, error: Exception, request: Peticion, user: Usuario):
        # Delete the request
        self.removeRequest(user, request.idPeticion)
        # Notificate the user
        text = f"Se ha eliminado la petición del producto {enclace_html(request.producto.nombre, request.producto.url)} por un error"
        self.funNotificateUser(user, text)
        # Notificate the error
        errList = format_exception(type(error), error, error.__traceback__)
        errList.insert(0, errList[-1])
        text =  f"<b>Error en el bucle decomprobación de peticiones</b>\n"
        text += f"Se eliminio la petición: \n{request}\n"
        text += f"Error: \n{''.join(errList[:-1])}\n"

        self.funError(text)

    def stopMainLoop(self):
        self.enBuclePrincipal = False