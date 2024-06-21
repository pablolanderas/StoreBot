from dominio.Producto import Producto
from dominio.Usuario import Usuario
from dominio.Mensaje import Mensaje
from dominio.Peticion import Peticion
from dominio.Deseado import Deseado

from sqlite3 import connect, Connection
from os import path, remove

class TABLAS:
    Productos = "Productos"
    Usuarios = "Usuarios"
    Peticiones = "Peticiones"
    Mensajes = "Mensajes"
    Notificacion = "Notificacion"
    TagName = "TagName"
    Tag = "Tag"
    Deseado = "Deseado"

class ATRIBUTOS:

    class Productos:
        productId = "productId"
        url = "url"

    class Usuarios:
        chatId = "chatId"
        username = "username"

    class Peticiones:
        requestId = "requestId"
        usuarioId = "usuarioId"
        productId = "productId"
        ultPrecio = "ultPrecio"

    class Mensajes:
        messageId = "messageId"
        chatId = "chatId"

    class Notificacion:
        messageId = "messageId"
        chatId = "chatId"

    class TagName:
        tagId = "tagId"
        nombre = "nombre"

    class Tag:
        deseadoId = "deseadoId"
        posicion = "posicion"
        tagName = "tagName"

    class Deseado:
        deseadoId = "deseadoId"
        requestId = "requestId"
        messageId = "messageId"
        tipoPrecio = "tipoPrecio"

def adaptTipe(val) -> str:
    t = type(val)
    if t is int:
        val = str(val)
    elif t is float:
        val = str(val)
    elif t is str:
        val = "'" + val + "'"
    elif val is None:
        val = "NULL"
    else:
        raise ValueError(f"The type {t} is not acepted. Data: {val}")
    return val
        
class DataBase:

    def startDataBase(dirBD, dirScript):
        if path.exists(dirBD):
            remove(dirBD)
        if not path.exists(dirScript):
            raise ValueError("No se ha encontrado el script")
        db = connect(dirBD)
        with open(dirScript, "r") as file:
            sql = file.read()
        db.executescript(sql)
        db.close()

    db : Connection

    def __init__(self, dirDB:str) -> None:
        if not path.exists(dirDB):
            raise ValueError(f"The database doesnt exist at {dirDB}")
        self.db = connect(dirDB, check_same_thread=False)

    def funSelect(self, table:str, columns="*", conditions=None, order=None):
        # Consulta base
        if type(columns) not in (list, tuple): columns = (columns,)
        consult = f"SELECT {', '.join(columns)} FROM {table}"
        # Condicionales
        if conditions is not None:
            if type(conditions) not in (list, tuple): conditions = (conditions,)
            consult += f" WHERE {' AND '.join(conditions)}"
        # Orden
        if order is not None:
            if type(order) not in (list, tuple): order = (order,)
            consult += f" ORDER BY {', '.join(order)}"
        
        return list(self.db.execute(consult))

    def funInsert(self, table, commit=True, **kwargs) -> int:
        # Inicializar los valores
        keys = list(map(adaptTipe, kwargs.keys()))
        vals = list(map(adaptTipe, kwargs.values()))
        cur = self.db.cursor()
        # Crear la consulta
        constult = f"INSERT INTO {table} ({', '.join(keys)}) VALUES ({', '.join(vals)})"
        # Ejecutarla y guardarla en caso de hacerlo
        cur.execute(constult)
        cur.close()
        if commit: self.db.commit()
        # Return the last Id
        return cur.lastrowid

    def funDelete(self, table, conditions=None, commit=True):
        # Inicia la consulta
        consult = f"DELETE FROM {table}"
        # Anhade los condicionales
        if conditions is not None:
            if type(conditions) not in (list, tuple): conditions = (conditions,)
            consult += f" WHERE {' AND '.join(conditions)}"
        # Ejecutar el codigo
        self.db.execute(consult)
        if commit: self.db.commit()

    def funUpdate(self, table, conditions=None, commit=True, **kwargs):
        # Consulta base
        consult = f"UPDATE {table} SET {', '.join(map(lambda x: f'{x[0]} = {adaptTipe(x[1])}' ,kwargs.items()))}"
        # Condicionales
        if conditions is not None:
            if type(conditions) not in (list, tuple): conditions = (conditions,)
            consult += f" WHERE {' AND '.join(conditions)}"
        # Ejecutar la consulta
        self.db.execute(consult)
        if commit: self.db.commit()

    def saveProducto(self, product:Producto) -> int:
        # Check if the arg is correct
        if not isinstance(product, Producto): 
            raise ValueError("The type of product is incorrect")
        # Save in the DB
        Id = self.funInsert(TABLAS.Productos, url=product.url)
        product.id = Id
        # Return de Id
        return Id

    def deleteProducto(self, product:Producto):
        # Check if the arg is correct
        if not isinstance(product, Producto):
            raise ValueError("The type of product is incorrect")
        # Delete the product
        self.funDelete(TABLAS.Productos, f"{ATRIBUTOS.Productos.productId} = {product.id}")

    def checkIfProductInRequest(self, product:Producto) -> bool:
        query = self.funSelect(TABLAS.Peticiones, ATRIBUTOS.Peticiones.productId, f"{ATRIBUTOS.Peticiones.productId} = {product.id}")
        return len(query) > 0

    def saveUsuario(self, user:Usuario, commit=True):
        # Check if the arg is correct
        if type(user) != Usuario:
            raise ValueError("The type of user is incorrect")
        # Save in the DB
        self.funInsert(TABLAS.Usuarios, commit=False, chatId=user.chatId, username=user.username)
        # Save the messages
        for message in user.chatMessages:
            self.saveMensaje(message, commit=False)
        # Save the notifications
        for message in user.notificaciones:
            self.saveNotificacion(message, commit=False)
        # Commit the changes
        if commit: self.db.commit()

    def updateUsuarioUsername(self, user:Usuario, commit=True):
        self.funUpdate(TABLAS.Usuarios, f"{ATRIBUTOS.Usuarios.chatId} = {user.chatId}", commit=False, username=user.username)
        if commit: self.db.commit()

    def deleteAllMensajesFromUsuario(self, user: Usuario):
        self.funDelete(TABLAS.Mensajes, (f"{ATRIBUTOS.Mensajes.chatId} = {user.chatId}",))

    def saveMensaje(self, message:Mensaje, commit=True): 
        # Check if the arg is correct
        if type(message) != Mensaje:
            raise ValueError("The type of message is incorrect")
        # Save in the DB
        self.funInsert(TABLAS.Mensajes, commit=commit, 
                       messageId=message.messageId, chatId=message.chatId)

    def saveNotificacion(self, message:Mensaje, commit=True):
        # Check if the arg is correct
        if type(message) != Mensaje:
            raise ValueError("The type of message is incorrect")
        # Save in the DB
        self.funInsert(TABLAS.Notificacion, commit=commit,
                       messageId=message.messageId, chatId=message.chatId)

    def savePeticion(self, request: Peticion, commit=True):
        # Check if the arg is correct
        if type(request) != Peticion:
            raise ValueError("The type of request is incorrect")
        # Save in the DB
        requestId = self.funInsert(TABLAS.Peticiones, commit=False,
                                   usuarioId=request.usuario.chatId, 
                                   productId=request.producto.id, 
                                   ultPrecio=request.ultPrecio)
        request.idPeticion = requestId
        # Save the price wish
        if request.notificacionPrecio != None:
            self.funInsert(TABLAS.Deseado, commit=False,
                        requestId=requestId, 
                        messageId=request.notificacionPrecio.messageId, 
                        tipoPrecio=1)
        # Save the wishes
        for wished in request.deseados:
            self.saveDeseado(wished, commit=False)
        # End the query
        if commit: self.db.commit()
        return requestId

    def deletePeticion(self, request: Peticion):
        # Check if the arg is correct
        if type(request) != Peticion:
            raise ValueError("The type of request is incorrect")
        # Delete the request
        self.funDelete(TABLAS.Peticiones, f"{ATRIBUTOS.Peticiones.requestId} = {request.idPeticion}", commit=False)
        # Delete the wishes
        for wished in request.deseados:
            self.deleteDeseado(wished, commit=False)
        # Delete the price wish
        self.deletePeticionPriceMessage(request, commit=False)
        # Commit the changes
        self.db.commit()

    # IMPORTANT: This metod doesnt save the notifications
    def updatePeticion(self, request: Peticion, commit=True, updateWisheds=True):
        if type(request) != Peticion:
            raise ValueError("The type of request is incorrect")
        # Update the request
        self.funUpdate(TABLAS.Peticiones, f"{ATRIBUTOS.Peticiones.requestId} = {request.idPeticion}",
                       commit=False,
                       usuarioId=request.usuario.chatId,
                       productId=request.producto.id,
                       ultPrecio=request.ultPrecio)
        # Update the wisheds
        if updateWisheds:
            ids = []
            for wished in request.deseados:
                if wished.idDeseado is None:
                    self.saveDeseado(wished, commit=False)
                else:
                    self.updateDeseado(wished, commit=False)
                ids.append(wished.idDeseado)
            # Save the price wish
            if request.notificacionPrecio != None:
                priceId = self.updatePeticionPriceMessage(request, commit=False)
                ids.append(priceId)
        # Delete the all wisheds
            query = self.funSelect(TABLAS.Deseado, ATRIBUTOS.Deseado.deseadoId, conditions=(
                f"{ATRIBUTOS.Deseado.requestId} = {request.idPeticion}",
                f"{ATRIBUTOS.Deseado.deseadoId} NOT IN ({', '.join(map(lambda x:str(x), ids))})"))
            for (wishedId,) in query:
                wished = Deseado(wishedId, None, None, request)
                self.deleteDeseado(wished, commit=False)
        # Commit the changes
        if commit: self.db.commit()

    def deletePeticionPriceMessage(self, request:Peticion, commit=True):
        if type(request) != Peticion:
            raise ValueError("The type of request is incorrect")
        # Delete the price wish
        self.funDelete(TABLAS.Deseado, conditions=(
                f"{ATRIBUTOS.Deseado.requestId} = {request.idPeticion}",
                f"{ATRIBUTOS.Deseado.tipoPrecio} = 1"))
        # Commit the changes
        if commit: self.db.commit()

    def updatePeticionPriceMessage(self, request:Peticion, commit=True):
        if type(request) != Peticion:
            raise ValueError("The type of request is incorrect")
        # Update the price wish
        resp = self.funSelect(TABLAS.Deseado, ATRIBUTOS.Deseado.deseadoId, conditions=(
                    f"{ATRIBUTOS.Deseado.requestId} = {request.idPeticion}",
                    f"{ATRIBUTOS.Deseado.tipoPrecio} = 1"))
        if resp:
            priceId = resp[0][0]
            self.funUpdate(TABLAS.Deseado, f"{ATRIBUTOS.Deseado.deseadoId} = {priceId}", 
                            messageId=request.notificacionPrecio.messageId, commit=False)
        else:
            priceId = self.funInsert(TABLAS.Deseado, commit=False,
                            requestId=request.idPeticion, 
                            messageId=request.notificacionPrecio.messageId, 
                            tipoPrecio=1)
        # Commit the changes
        if commit:
            self.db.commit()
        return priceId

    def saveDeseado(self, wished:Deseado, commit=True):
        # Check if the arg is correct
        if type(wished) != Deseado:
            raise ValueError("The type of wished is incorrect")
        # Save the wished
        messageId = None
        if wished.mensaje is not None: 
            messageId = wished.mensaje.messageId
        wishedId = self.funInsert(TABLAS.Deseado, commit=False,
                                  requestId=wished.peticion.idPeticion,
                                  messageId=messageId,
                                  tipoPrecio=0)
        wished.idDeseado = wishedId
        # Save the tags
        for index, tag in enumerate(wished.tags):
            tagNameId = self.getTagNameId(tag, commit=False)
            self.funInsert(TABLAS.Tag, commit=False,
                           deseadoId=wishedId,
                           posicion=index,
                           tagName=tagNameId)        
        # Save the DB
        if commit: self.db.commit()

    def getWishedsForRequest(self, request:Peticion, getTags=True) -> list[Deseado]:
        # Exit if the type is bad
        if type(request) != Peticion:
            raise ValueError("The type of request is incorrect")
        query = self.funSelect(TABLAS.Deseado, 
                               conditions=f"{ATRIBUTOS.Deseado.requestId} = {request.idPeticion}")
        wisheds = []
        for (wishedId, _, messageId, tipoPrecioId) in query:
            if not tipoPrecioId:
                if messageId is None: msg = None
                else: msg = Mensaje(None, None, request.usuario.chatId, None, messageId)
                wished = Deseado(wishedId, msg, [], request)
                if getTags:
                    wished.tags = self.getWishedTags(wishedId)
                wisheds.append(wished)
        return wisheds

    # IMPORTANT: This metod doesnt edit the tags, only edits de message
    def updateDeseado(self, wished: Deseado, commit=True):
        wis = self.funSelect(TABLAS.Deseado, ATRIBUTOS.Deseado.messageId, f"{ATRIBUTOS.Deseado.deseadoId} = {wished.idDeseado}")
        if not wis:
            raise ValueError("The wished you are trying to edit doesnt exist")
        # Save the data
        if wished.mensaje is not None:
            messageId = wished.mensaje.messageId
        else:
            messageId = None
        self.funUpdate(TABLAS.Deseado, f"{ATRIBUTOS.Deseado.deseadoId} = {wished.idDeseado}",
                        messageId=messageId, commit=False)
        # Commit the changes
        if commit: self.db.commit()

    def deleteDeseado(self, wished: Deseado, commit=True):
        # Get the tagNames
        query = self.funSelect(TABLAS.Tag, ATRIBUTOS.Tag.tagName, 
                               conditions=f"{ATRIBUTOS.Deseado.deseadoId} = {wished.idDeseado}")
        # Delete the wished and the tags
        self.funDelete(TABLAS.Deseado, f"{ATRIBUTOS.Deseado.deseadoId} = {wished.idDeseado}", commit=False)
        self.funDelete(TABLAS.Tag, f"{ATRIBUTOS.Tag.deseadoId} = {wished.idDeseado}", commit=False)
        # Delete the tagName if is unique
        for (tadNameId,) in query:
            if not self.funSelect(TABLAS.Tag, conditions=f"{ATRIBUTOS.Tag.tagName} = {tadNameId}"):
                self.funDelete(TABLAS.TagName, f"{ATRIBUTOS.TagName.tagId} = {tadNameId}", commit=False)
        # Commit the changes
        if commit: self.db.commit()

    def getTagNameId(self, tagName:str, commit=True) -> int:
        # Get the id
        val = self.funSelect(TABLAS.TagName, 
                        columns=(ATRIBUTOS.TagName.tagId,),
                        conditions=(f"{ATRIBUTOS.TagName.nombre} = {adaptTipe(tagName)}",))
        # Case havent been created
        if not val:
            return self.funInsert(TABLAS.TagName, commit=commit, nombre=tagName)
        else:
            return val[0][0]

    def getWishedTags(self, wishedId:int) -> list[str]:
        query = f"""
                SELECT TagName.nombre
                FROM Tag
                JOIN TagName ON Tag.tagName = TagName.tagId
                WHERE Tag.deseadoId = {wishedId}
                ORDER BY Tag.posicion ASC;
            """
        return list(map(lambda x:x[0], self.db.execute(query)))

    def getAllProducts(self) -> dict[int:Producto]:
        productsQuery = self.funSelect(TABLAS.Productos, columns=(
            ATRIBUTOS.Productos.productId, ATRIBUTOS.Productos.url 
        ))
        products = {}
        for productid, url in productsQuery:
            product = Producto.inicaProducto(url, productid)
            products[productid] = product
        return products

    def loadGestorData(self, gestor):
        # Start with the products
        gestor.productos.update(self.getAllProducts())
        # Now with the users
        usersQuery = self.funSelect(TABLAS.Usuarios, columns=(
            ATRIBUTOS.Usuarios.username, ATRIBUTOS.Usuarios.chatId
        ))
        for username, chatId in usersQuery:
            user = Usuario(username, chatId)
            gestor.usuarios[chatId] = user
            # Add the messages
            messagesQuery = self.funSelect(TABLAS.Mensajes, 
                                           columns=(ATRIBUTOS.Mensajes.messageId,),
                                           conditions=(f"{ATRIBUTOS.Mensajes.chatId} = {chatId}",),
                                           order=(ATRIBUTOS.Mensajes.messageId,))
            for messageId in messagesQuery:
                messageId = messageId[0]
                message = Mensaje(None, None, chatId, username, messageId)
                user.chatMessages.append(message)
            # Add the notifications
            notificationsQuery = self.funSelect(TABLAS.Notificacion, 
                                               columns=(ATRIBUTOS.Notificacion.messageId,),
                                               conditions=(f"{ATRIBUTOS.Notificacion.chatId} = {chatId}",),
                                               order=(ATRIBUTOS.Notificacion.messageId,))
            for messageId in notificationsQuery:
                messageId = messageId[0]
                message = Mensaje(None, None, chatId, username, messageId)
                user.notifications.append(message) 
            # Add the request
            requestQuery = self.funSelect(TABLAS.Peticiones, columns=(
                ATRIBUTOS.Peticiones.requestId, ATRIBUTOS.Peticiones.productId, ATRIBUTOS.Peticiones.ultPrecio
                ), conditions=(f"{ATRIBUTOS.Peticiones.usuarioId} = {chatId}",))
            for requestId, productId, ultPrecio in requestQuery:
                product = gestor.productos[productId]
                request = Peticion(user, product, requestId, ultPrecio)
                user.peticiones[requestId] = request
                # Add the wishes
                wishesQuery = self.funSelect(TABLAS.Deseado, columns=(
                    ATRIBUTOS.Deseado.deseadoId, ATRIBUTOS.Deseado.messageId, ATRIBUTOS.Deseado.tipoPrecio
                    ), conditions=(f"{ATRIBUTOS.Deseado.requestId} = {requestId}",))
                for wishedId, messageId, typePrice in wishesQuery:
                    if messageId is None: message = None
                    else:
                        message = Mensaje(None, None, chatId, username, messageId)
                    if typePrice: # Case price
                        request.notificacionPrecio = message
                    else: # Case wished
                        tags = self.getWishedTags(wishedId)
                        wished = Deseado(wishedId, message, tags, request)
                        request.deseados.append(wished)

    
