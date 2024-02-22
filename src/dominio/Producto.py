
class Producto:

    id : int
    url : str
    nombre : str
    precio : float
    tags : dict

    def inicaProducto(url, id=None):
        from dominio.productos.ListaProductos import DIC_PRODUCTS
        for domain, obt in DIC_PRODUCTS.items():
            if domain in url:
                return obt(url, id)
        raise NotImplementedError("The domain not exist")

    def __init__(self, url, id) -> None:
        # Inicializamos los valores
        self.id = id
        self.url = url
        self.descargaDatos()
        self.calculaValores(True)

    def calculaValores(self, inicializate=False) -> None:
        # Inicializamos el nombre
        if inicializate:
            self.iniciaNombre()
        # Inicializamos las tags
        self.actualizaTags()
        # Obtenemos el precio
        self.precio = self.obtenPrecio()

    def actualiza(self) -> None:
        # Descargamos los datos necesarios
        self.descargaDatos()
        # Actualizamos los valores del producto
        self.calculaValores()   

    def compruebaDeseadosCorrecto(self, cadena:list):
        temp = self.tags
        for key in cadena:
            if not key in temp: return False
            temp = temp[key]
        return True   
    
    def __str__(self) -> str:
        return f"{type(self)}[@{self.url}]"

    def __repr__(self) -> str:
        return self.__str__()  

    def descargaDatos(self) -> None:
        pass

    def iniciaNombre(self) -> None:
        pass

    def actualizaTags(self) -> None:
        pass 

    def obtenPrecio(self) -> float:
        return 0
    
    def obtenFoto(self) -> bytes:
        return None