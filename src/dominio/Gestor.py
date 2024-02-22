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

    def __init__(self, dataBase:DataBase) -> None:
        # Inicializate the class
        self.dataBase = dataBase
        self.usuarios = {}
        self.productos = {}

        # Get the DB data
        dataBase.loadGestorData(self)
