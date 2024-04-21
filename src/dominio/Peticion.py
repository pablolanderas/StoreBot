from dominio.Producto import Producto
from dominio.Deseado import Deseado
from dominio.Mensaje import Mensaje

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from dataBase import DataBase

class Peticion:
    
    idPeticion : int
    usuario : None
    producto : Producto
    ultPrecio : float
    deseados : list[Deseado]
    notificacionPrecio : Mensaje
    funcionNotificarUsuario = None
    funcionEliminaNotificacion = None
    if TYPE_CHECKING: dataBase: DataBase
    else: dataBase = None

    def __init__(self, usuario, producto:Producto, idPeticion=None, ultPrecio=None) -> None:
        if self.funcionNotificarUsuario is None: 
            raise NotImplemented("No ha sido fijada la funcion de notificar")
        if self.funcionEliminaNotificacion is None:
            raise NotImplemented("No ha sido fijada la funcion de eliminar notificacion")
        self.idPeticion = idPeticion
        self.usuario = usuario
        self.producto = producto
        if ultPrecio is None: ultPrecio = producto.obtenPrecio()
        self.ultPrecio = ultPrecio
        self.deseados = []
        self.notificacionPrecio = None

    def comprueba(self) -> bool:
        cambios = False
        if self.producto.precio != self.ultPrecio:
            if self.notificacionPrecio is not None:
                self.funcionEliminaNotificacion(self.notificacionPrecio)
            if self.producto.precio < self.ultPrecio:
                self.notificacionPrecio = self.notificaPrecio()
            self.ultPrecio = self.producto.precio
            self.dataBase.updatePeticion(self, updateWisheds=False)
            cambios = True
        for deseado in self.deseados:
            temp = self.producto.tags
            for key in deseado.tags:
                temp = temp[key]
            if deseado.mensaje is None:
                if temp:
                    deseado.mensaje = self.notificaStock(deseado)
                    cambios = True
            else:
                if not temp:
                    self.funcionEliminaNotificacion(deseado.mensaje)
                    deseado.mensaje = None
                    cambios = True
        return cambios

    def notificaPrecio(self) -> Mensaje:
        msj = self.obtenTextoNotificaPrecio()
        return self.funcionNotificarUsuario(msj, "precio")

    def obtenTextoNotificaPrecio(self):
        msj = f"Antes: {self.ultPrecio}€\n"
        msj += f"Ahora: {self.producto.precio}€"
        return msj

    def notificaStock(self, deseado: Deseado) -> Mensaje:
        msj = self.obtenTextoNotificaStock(deseado.tags)
        return self.funcionNotificarUsuario(msj, deseado.idDeseado)

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
        text = f"[Peticion:@{self.idPeticion} de {self.usuario} de {self.producto}] Deseados = " + "{\n"
        for des in self.deseados:
            text += f"  {des}\n"
        text += "}"
        return text