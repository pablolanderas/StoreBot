from dominio.productos.ProductoZara import ProductoZara
from os import chdir

dirAct = "\\".join(__file__.split("\\")[:-1])
chdir(dirAct)

URL = "https://www.zara.com/es/es/pnt-bttns-12-p03175241.html?v1=355920208&v2=2352540"

prod = ProductoZara(URL, None)
prod.obtenFoto()