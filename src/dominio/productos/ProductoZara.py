from dominio.Producto import Producto

from requests import get as getRequest
#from pprint import pprint

DIR_PETICION = "https://www.zara.com/es/es/products-details?productIds="
HEADERS = { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:100.0) Gecko/20100101 Firefox/100.0' }
DOMAIN_ZARA = "www.zara.com"

def obtenerCodigoProdcucto( url:str ) -> str: pass
def peticionProducto( codProducto:str ) -> str: return DIR_PETICION+codProducto

class ProductoZara(Producto):

    descarga : dict
    codigoProdcucto : str

    def __init__(self, url, id) -> None:
        self.codigoProdcucto = obtenerCodigoProdcucto(url)
        super().__init__(url, id)

    def descargaDatos(self) -> None:
        # Realizar la peticion
        try:
            resp = getRequest(peticionProducto(self.codigoProdcucto), headers=HEADERS)
        except:
            raise RuntimeError("Error during the request")
        # Comprobar que la peticion se ha respondido correctamente
        if resp.status_code != 200: raise RuntimeError("Error in the return of the request")
        # Comprobar que se ha escogido un producto correcto
        content = resp.json()
        if not content: raise ValueError("The code is not valid")
        # Fijar los datos
        self.descarga = content[0]

    def iniciaNombre(self) -> None:
        self.nombre = self.descarga["name"]

    def actualizaTags(self) -> None:
        # Obtener todos los colores
        colores = list(map(lambda x:x["name"], self.descarga["detail"]["colors"]))
        # Crear el diccionario
        self.tags = {color:{} for color in colores}
        # Anhadir a cada color sus tayas con disponibilidad
        for index, color in enumerate(colores):
            self.tags[color] = {size["name"]:size["availability"] != "out_of_stock" 
                                    for size in self.descarga["detail"]["colors"][index]["sizes"]}

    def obtenPrecio(self) -> float:
        prec = self.descarga["detail"]["colors"][0]["price"]/100
        return prec
    
    def obtenFoto(self) -> bytes:
        return open("./bot/img/logoZara.jpg", "rb")
    
    def __eq__(self, __value: object) -> bool:
        return type(__value) == ProductoZara and __value.codigoProdcucto == self.codigoProdcucto
    
    def __str__(self) -> str:
        return f"[ProdcutoZara|Nombre='{self.nombre}'|Codigo={self.codigoProdcucto}]"


def obtenerCodigoProdcucto( url:str ) -> str:
    posicion = url.find("v1=")
    if posicion == -1: raise ValueError("The url hasnt a product code")
    try:
        return url[posicion+3:posicion+12] 
    except: raise ValueError("The url hasnt a product code")

if __name__ == "__main__":
    p1 = ProductoZara(
        "https://www.zara.com/es/es/top-capa-punto-con-lana-p09598164.html?v1=278853934&v2=2354495"
    )
    p2 = ProductoZara(
        "https://www.zara.com/es/es/top-capa-punto-con-lana-p09598164.html?v1=278853934&v2=2354495"
    )