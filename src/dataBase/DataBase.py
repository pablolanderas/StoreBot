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
        self.db = connect(dirDB)

    def funSelect(self, table:str, columns="*", conditions=None, order=None):
        # Consulta base
        consult = f"SELECT {', '.join(columns)} FROM {table}"
        # Condicionales
        if conditions is not None:
            consult += f" WHERE {' AND '.join(conditions)}"
        # Orden
        if order is not None:
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
            consult += f" WHERE {' AND '.join(conditions)}"
        # Ejecutar el codigo
        self.db.execute(consult)
        if commit: self.db.commit()

    def funUpdate(self, table, conditions=None, commit=True, **kwargs):
        # Consulta base
        consult = f"UPDATE {table} SET {', '.join(map(lambda x: f'{x[0]} = {adaptTipe(x[1])}' ,kwargs.items()))}"
        # Condicionales
        if conditions is not None:
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

    def saveUsuario(self, user:Usuario):
        # Check if the arg is correct
        if type(user) != Usuario:
            raise ValueError("The type of user is incorrect")
        # Save in the DB
        self.funInsert(TABLAS.Usuarios, commit=False, chatId=user.chatId, username=user.username)
        # Save the messages
        for message in user.chatMessages:
            self.saveMensaje(message, commit=False)
        self.db.commit()

    def saveMensaje(self, message:Mensaje, commit=True): 
        # Check if the arg is correct
        if type(message) != Mensaje:
            raise ValueError("The type of message is incorrect")
        # Save in the DB
        self.funInsert(TABLAS.Mensajes, commit=commit, 
                       messageId=message.messageId, chatId=message.chatId)

    def savePeticion(self, request:Peticion):
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
        self.db.commit()
        return requestId
    
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

        
if __name__ == "__main__":
    DataBase.startDataBase("./database.db", "./resources/database.sql")
    db = DataBase("./database.db")
    db.funDelete(TABLAS.Usuarios)
    db.funDelete(TABLAS.Mensajes)
    db.funDelete(TABLAS.Productos)
    db.funDelete(TABLAS.Peticiones)
    db.funDelete(TABLAS.Deseado)
    db.funDelete(TABLAS.TagName)
    db.funDelete(TABLAS.Tag)
    Peticion.funcionNotificarUsuario = lambda x: print(x)

    user = Usuario("usuario", 23441)
    db.saveUsuario(user)
    prod = Producto.inicaProducto("https://www.zara.com/es/es/top-popelin-palabra-de-honor-abalorios-p00881007.html?v1=271552262")
    db.saveProducto(prod)
    req = Peticion(user, prod)
    #req.deseados.append(Deseado(None, None, ["tag1", "tag2", "tag3"], req))
    req.deseados.append(Deseado(None, Mensaje(None, None, None, None, 23445234), ["tag1", "tag2", "tag3"], req))
    db.savePeticion(req)

    print("Usuarios:", db.funSelect(TABLAS.Usuarios))
    print("Productos:", db.funSelect(TABLAS.Productos))
    print("Peticiones:", db.funSelect(TABLAS.Peticiones))
    print("Deseados:", db.funSelect(TABLAS.Deseado))
    print("Tag:", db.funSelect(TABLAS.Tag))
    print("TagName:", db.funSelect(TABLAS.TagName))

    
