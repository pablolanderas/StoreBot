from dominio import Producto

DOMAIN_PRUEBA = "ppp"

class ProductoPrueba(Producto):

    def __init__(self, url, id) -> None:
        self.contador = int(url[3:])
        super().__init__(url, id)
        self.url = "www.zara.com/es/es/top-palabra-de-honor-p02335160.html?v1=344072160"

    def iniciaNombre(self) -> None:
        self.nombre = "Producto de prueba"

    def descargaDatos(self) -> None:
        self.contador -= 1
        print("Datos de producto de prueba descargados: cont =", self.contador)

    def actualizaTags(self) -> None:
        self.tags = {f"tag{i}":False for i in range(5)}

    def obtenPrecio(self) -> float:
        if self.contador <= 0:
            return 10
        else:
            return 20
        
    def obtenFoto(self) -> bytes:
        return None
    
    def __eq__(self, value: object) -> bool:
        return type(value) == type(self)
    
    def __str__(self) -> str:
        return f"[Producto de prueba] Contador: {self.contador}"
