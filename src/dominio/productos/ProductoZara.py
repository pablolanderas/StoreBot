from dominio.Producto import Producto

from requests import get as getRequest
from bs4 import BeautifulSoup

DIR_PETICION = "https://www.zara.com/es/es/products-details?productIds="
HEADERS = { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:100.0) Gecko/20100101 Firefox/100.0' }
DOMAIN_ZARA = "www.zara.com"

def obtenerCodigoProdcucto( url:str ) -> str: pass
def peticionProducto( codProducto:str ) -> str: return DIR_PETICION+codProducto

class ProductoZara(Producto):

    descarga : dict
    codigoProdcucto : str
    urlFoto : str

    def __init__(self, url, id) -> None:
        self.codigoProdcucto = obtenerCodigoProdcucto(url)
        self.urlFoto = None
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
        if self.urlFoto is None:
            return self.obtenFotoBasica()
        return getRequest(self.urlFoto, headers=HEADERS).content

    def iniciaFoto(self) -> None:
        pagWeb = getRequest(self.url, headers=HEADERS)
        if pagWeb.status_code != 200: 
            return 
        # Encontrar el html original
        soup = BeautifulSoup(pagWeb.text, 'html.parser')
        head_tag = soup.head
        url = None
        for tag in head_tag.find_all('meta'):
            if cont:=tag.get('content', False):
                dividido = cont.split("URL=")
                if len(dividido) == 2:
                    url = "http://"+ DOMAIN_ZARA + dividido[1][1:-1]
                    break
        if url is None:
            return
        # Encontrar la url de la imagen
        pagWeb = getRequest(url, headers=HEADERS)
        if pagWeb.status_code != 200: 
            return
        soup = BeautifulSoup(pagWeb.text, 'html.parser')
        head_tag = soup.head
        og_image_meta = head_tag.find('meta', {'property': 'og:image'})
        if og_image_meta:
            self.urlFoto = og_image_meta['content']

    def obtenFotoBasica(self) -> bytes:
        return open("./resources/logoZara.jpg", "rb")
    
    def __eq__(self, __value: object) -> bool:
        return type(__value) == ProductoZara and __value.codigoProdcucto == self.codigoProdcucto
    
    def __str__(self) -> str:
        return f"[ProdcutoZara|Nombre='{self.nombre}'|Codigo={self.codigoProdcucto}] {self.id}"


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