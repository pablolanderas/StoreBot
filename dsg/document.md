# Documentacion añadir nuevas tiendas

Para añadir nuevas tiendas se hace a traves de herencia del la clase ``Prodcuto`` con la implementacion aqui explicada`'

## Indice

1. [Ubicacion](#ubicacion)  
2. [Funciones](#funciones)  
    2.1 [Constantes](#constantes)  
    2.2 [Inicializador](#inicializador)  
    2.3 [Descarga datos](#descarga_datos)  
    2.4 [Inicia nombre](#inicia_nombre)  
    2.5 [Actualiza tags](#actualiza_tags)  
    2.6 [Obten precio](#obten_precio)  
    2.7 [Obten foto](#obten_foto)  
    2.8 [Equal](#equal)  
    2.9 [String](#string)  
3. [Implementacion](#implementacion)
4. [Consejos](#consejos)

## Ubicacion <a id="ubicacion"/>

La ubicación de los productos ha de ser en la carpeta de ser dentro del dominio, en la carpeta de productos

## Funciones <a id="funciones"/>

Estas son las funicones que has de implementar para realizar una correcta clase que pueda utilizar el gestor

**Constantes** <a id="constantes">

La clase ha de tener una constante que indique cual es el dominio de la tienda, aparte de esto, es recomendable tener tambien tener una constante de la direccion de la peticion que hay que realizar y otra del los headers de la peticion

**Inicializador** <a id="inicializador">

~~~python
def __init__(self, url, id) -> None:
~~~

Al inicializar la funcion se deben de inicializar todos los datos necesarios para la gestion del producto, sin realizar ninguna peticion, esto se hara en el siguiente paso. Que no se te olvide llamar a la clase padre con ``super().__init__(url, id)``. Aparte, esta función tambien ha de lanzar una excepcion ``ValueError(THE ERROR)``. Esta excepcion se lanzara en caso de no haber escrito un producto correcto

**Descargar datos** <a id="descarga_datos">

~~~python
def descargaDatos(self) -> None:
~~~

Esta funcion unicamente se encarga de descargar los datos y guardarlos en la clase, no hace ningun otro tipo de operacion. Esta funcion tambien lanza una excepcion ``RuntimeError(THE ERROR)`` en caso de que suceda algun problema a la hora de la descarga de los datos

**Inicia nombre** <a id="inicia_nombre">

~~~python
def iniciaNombre(self) -> None:
~~~

Esta funcion unicamente debe de inicializar el nombre del producto con los datos descargados previamente

**Actualiza tags** <a id="actualiza_tags">

~~~python
def actualizaTags(self) -> None:
~~~

Con los datos descargados, esta funcion debe de actualizar los tags del producto. Los tags son un diccionario de obligatoriamente un elemento. En cada clave puede haber o un ``bool`` o otro ``dic``. El buleano indica si hay stock de los datos anteriores y el diccionario indica otro tipo de dato distinto. Un ejemplo del tag puede ser el siguiente:

~~~json
    {
        "rojo": {
            "L": true,
            "M": true,
            "S": false
        },
        "azul": {
            "L": true,
            "M": true,
            "S": false
        }
    }
~~~

**Obten precio** <a id="obten_precio">

~~~python
def obtenPrecio(self) -> float:
~~~

Obtiene el precio de los datos descargados y lo devuelve como un ``float``, no lo actualiza, unicamente lo devuelve

**Obten foto** <a id="obten_foto">

~~~python
def obtenFoto(self) -> bytes:
~~~

Obtiene la foto del producto en formato ``bytes`` ("rb") y lo retorna. En caso de no tener foto o no encontrar la forma de obtenerla devolver ``None``

**Equal** <a id="equal">

~~~python
def __eq__(self, __value: object) -> bool:
~~~

Necesita crear la funcion para comprobar si dos productos son iguales. Importante que compruebe si es del mismo tipo de producto primero y despues lo compare con lo que deberian de ser iguales

**String** <a id="string">

~~~python
def __str__(self) -> str:
~~~

Para facilitar su debugueo, implementar la clase para que al ser pintado el objeto se pueda mostrar correctametne de que tipo es e informacion relevante sobre el mismo. Recomendable identificarlo con el nombre del producto y un valor caracteristico de la tienda

## Implementacion <a id="implementacion"/>

Para la implementacion de la clase y que funcione correctamente hay que añadir el producto al archivo ``ListaProductos.py``. Para esto hay que importarlo desde la carpeta y añadirlo al diccionario, la llave debe de ser el dominio del producto y el valor la clase heredada

## Consejos <a id="consejos"/>

Puedes utilizar la funcion ``pprint()`` de la libreria pprint para pintar por pantalla los ``json`` y poder trabajar mejor con ellos
