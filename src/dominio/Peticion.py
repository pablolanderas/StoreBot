from dominio.Producto import Producto
from dominio.Deseado import Deseado
from dominio.Mensaje import Mensaje

class Peticion:
    
    idPeticion : int
    usuario : None
    producto : Producto
    ultPrecio : float
    deseados : list[Deseado]
    notificacionPrecio : Mensaje
    funcionNotificarUsuario = None

    def __init__(self, usuario, producto:Producto, idPeticion=None, ultPrecio=None) -> None:
        if self.funcionNotificarUsuario is None: 
            raise NotImplemented("No ha sido fijada la funcion de notificar")
        self.idPeticion = idPeticion
        self.usuario = usuario
        self.producto = producto
        if ultPrecio is None: ultPrecio = producto.obtenPrecio()
        self.ultPrecio = ultPrecio
        self.deseados = []
        self.notificacionPrecio = None

    def comprueba(self):
        if self.producto.precio < self.ultPrecio:
            self.notificacionPrecio = self.notificaPrecio()
            self.ultPrecio = self.producto.precio
        for deseado in self.deseados:
            if deseado.mensaje is None:
                temp = self.producto.tags
                for key in deseado.tags:
                    temp = temp[key]
                if temp:
                    deseado.mensaje = self.notificaStock(deseado.tags)

    def notificaPrecio(self) -> Deseado:
        msj = self.obtenTextoNotificaPrecio()
        return self.funcionNotificarUsuario(self, msj)

    def obtenTextoNotificaPrecio(self):
        msj =  f"Nuevo precio disponible para {self.producto.nombre}\n"
        msj += f"Antes: {self.ultPrecio}€\n"
        msj += f"Ahora: {self.producto.precio}€"
        return msj

    def notificaStock(self, cadena) -> Deseado:
        msj = self.obtenTextoNotificaStock(cadena)
        return self.funcionNotificarUsuario(self, msj)

    def obtenTextoNotificaStock(self, cadena):
        msj =  f"Nuevo stock disponible para {self.producto.nombre}\n"
        msj += f"Diponible: "
        for tipo in cadena:
            msj += f"{tipo} "
        return msj

    def anhadeTags(self, tags):
        self.deseados.append(tags)

    def __repr__(self) -> str:
        return self.__str__()

    def __str__(self) -> str:
        return f"[Peticion:@{self.idPeticion}]:NotPrecio={self.notificacionPrecio}"