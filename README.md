# StoreBot

### Indice

1. [Despligue del bot](#depliegue)
2. [Documentacion](#documentacion)   
    2.1. [Documentacion del bot](#bot)  
    2.2. [Docuemtnacion de la base de datos](#base_de_datos)  
    2.3. [Documentacion del gestor](#gestor)  
    2.4. [Implementacion de nuevas tiendas](#nuevos_productos)  
3. [Sobre mi](#sobre_mi)

## Despliegue <a id="depliegue">

Para desplegar el bot, primero hay que crear las variables de entorno, para esto hay que crear un archivo `.env` en el directorio `src` del proyecto (`src/.env`). Este archivo debe de tener lo siguiente:

~~~bash
BOT_TOKEN="{API_KEY_TOKEN}"
ID_CHAT_AVISOS={CHAT_ID_PARA_AVISOS}
ID_CHAT_ERRORES={CHAT_ID_PARA_ERRORES}

CREATE_DB={CREAR_BASE_DE_DATOS}
TESTING={MODO_TESTING}
~~~

Cada valor significa lo siguiente:

- *BOT_TOKEN:* La API Key del bot en el que quieres despegar el servicio
- *ID_CHAT_AVISOS:* El Id del chat en el que quieres que te llegen los avisos de las acciones que se realizan en el bot, como registros o acciones de los usuarios
- *ID_CHAT_ERRORES:* El Id del chat en el que quieres que te llegen los errores que saltan durante la ejecución
- *CREATE_DB*: Indica si quieres que se cree la base de datos durante la ejecución en caso de que no exista. Si no es la primera ejecucion del bot, es recomendable dejarla en `false`, si quieres crearlo dejarlo en `true`
- *TESTING:* Indicar si quieres que se ejecute en modo de testing, por defecto dejar en `false`

Una vez creado el archivo se puede desplegar de 2 formas, la recoendable es [utilizando docker](#depliegue_docker), pero si en el dispositivo en el que lo quieres ejecutar no es suficientemente potente o prefieres ejecutarlo directamente, se puede ejecutar con un entorno de python

### Despliegue con docker <a id="depliegue_docker">

Para ejecutarlo utilizando docker simplemente hay que utilizar el siguiente comando:

~~~bash
docker compose up
~~~

En caso de recibir una actualizacion, añadir `--build` para que actualice el conetenedor con los nuevos cambios

Si quieres que el contenedor corra en segundo plano, se puede utilizar `-d`

### Despliegue con entorno de python <a id="depliegue_env">

Para desplegarlo con un entorno de python, primero hay que crear el entorno, para eso se utiliza el siguiente comando desde el directorio raiz del proyecto:

~~~bash
python -m venv ./env
~~~

Una vez se ha creado el entorno, se descargan las dependencias del proyecto, para eso ejecutamos el pip del entorno descargando las dependencias que estan en el proyecto con el siguiente comando:

~~~bash
.\env\Scripts\pip.exe install -r .\dsg\dependencies.txt
~~~

Por ultimo ejecutamos el programa desde el ejecutable del entorno:

~~~bash
.\env\Scripts\python.exe .\src\__main__.py
~~~

## Documentacion <a id="documentacion">

Aqui se encuentra toda la documentacion sobre el [bot](#bot), la [base de datos](#base_de_datos) y el [gestor](#gestor). Ademas, tambien esta la informacion de como [implementar nuevas tiendas](#nuevos_productos)

### Documentacion del bot <a id="bot">

La implementacion del bot se encuentra en `./src/bot/StoreBot.py`. Esta clase hereda de la clase `Telebot` de la libreria telebot, con la que te facilita hacer las peticiones para la API de telegram. 

#### Funcionamiento

A la hora de inicializar el bot, este recibe el token del bot de la API de telegram y la clase del [gestor](#gestor) que va a utilizar. Una vez inicializado el bot aun no funciona, hay que llamar a la funcion [`startMainLoop()`](#startMainLoop) la cual inicia un bucle infinito que comienza a controlar las peticiones

**startMainLoop** <a id="startMainLoop"/>

Esta funcion inicia el bucle infinito de escucha del bot, este comprueba constantemente las acutalizaciones del bot llamando a la funcion correspondiente de `Telebot`, esto siempre que no se haya detenido fijando la variable del bucle a `false`

**startMainLoop** <a id="startMainLoop"/>

### Documentacion de la base de datos <a id="base_de_datos">

### Documentacion del gestor <a id="gestor">

### Implementacion de nuevas tiendas <a id="nuevos_productos">

Para añadir nuevas tiendas se hace a traves de herencia del la clase ``Prodcuto`` con la implementacion aqui explicada`'

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

#### Ubicacion <a id="ubicacion"/>

La ubicación de los productos ha de ser en la carpeta de ser dentro del dominio, en la carpeta de productos

#### Funciones <a id="funciones"/>

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

#### Implementacion <a id="implementacion"/>

Para la implementacion de la clase y que funcione correctamente hay que añadir el producto al archivo ``ListaProductos.py``. Para esto hay que importarlo desde la carpeta y añadirlo al diccionario, la llave debe de ser el dominio del producto y el valor la clase heredada

#### Consejos <a id="consejos"/>

Puedes utilizar la funcion ``pprint()`` de la libreria pprint para pintar por pantalla los ``json`` y poder trabajar mejor con ellos

## Sobre mi <a id="sobre_mi">

Hecho por Pablo Landeras, estudiante de ingenieria informatica en la universidad de Cantabria.

**Contacto**:  
- Email: pablolanderas@gmail.com  
- Linkedin: [https://www.linkedin.com/in/pablo-landeras/](https://www.linkedin.com/in/pablo-landeras/)
