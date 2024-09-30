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

**inicializeCommands** <a id="startMainLoop"/>

Esta funcion inicializa los siguientes comandos del bot:

- La funcion que atendera las respuestas por texto que recibe el bot llamando a [`messageReciber`](#messageReciber)
- La funcion que al el bot y cuando se utiliza su comando `/start`. Esta llama a [`buttonsControler`](#buttonsControler) con el comando de inicio
- La funcion que gestiona cuando se pulsa un boton, llamando a [`buttonsControler`](#buttonsControler) con el comando del boton que se haya pulsado 

**buttonsControler** <a id="buttonsControler">

Esta funcion se lanza cuando el usuario ha pulsado un boton en la interfaz de telegram. Esta recibe un usuario y los datos a procesar. Los datos son una cadena de caracteres, en la que hay varaias instrucciones separadas por `_-_`, la primera es el comando a utilizar, y el resto los argumentos que recibe. Gestiona los siguientes comandos

- *cmd_start*: el comando que se ejecuta cuando se va a la pagina principal del bot, llama a la funcion [`cmd_start`](#cmd_start)
- *cmd_help*: el comando que se ejecuta cuando se va a la pagina de ayuda del bot, llama a la funcion [`cmd_help`](#cmd_help)
- *cmd_products_list*: el comando que gestiona la pagina de los productos del usuario. Este, si no recibe ningun argumento lo que hace es mostrar la pagina con los productos del usuario llamando a la funcion [`cmd_products_list`](#cmd_products_list). En caso de tener argumentos, puede tener 2:
    - `remove`: este elimina la peticion con el id que reciba como argumento. Esto lo hace eliminandolo del gestor y seguido refrescando la vista del usuario llamando a [`cmd_products_list`](#cmd_products_list) 
    - `edit`: este abre la vista para poder editar la peticion con el id que reciba de argumento. Para esto llama a [`showAddingRequest`](#showAddingRequest) habiendo fijado la peticion como la editable
- *cmd_add_product*: el comando que se ejecuta cuando se va a la pagina de añadir un producto del bot, llama a la funcion [`cmd_add_product`](#cmd_add_product)
- *add_product*: el comando que se llama para gestionar un producto que se esta gestionando o añadiendo. Este puede recibir los siguinetes argumentos:
    - `addTags`: este inicializa los valores para poder añadir un deseado a la peticion de un producto. Despues llama a [`showAddingTagsToRequest`](#showAddingTagsToRequest) para que muestre la seleccion de las tags
    - `save`: este guarda la peticion del producto que esta añadiendo el usuario a traves del gestor, y despues llama a [`cmd_add_product`](#cmd_add_product) para volver a la vista de añadir un producto con el aviso de que se ha guardado el producto correctamente
    - `tagSelected`: recive una tag para añadir a un deseado de una peticion. En caso de ser la ultima tag que se pueda añadir al deseado, crea el objeto del deseado y lo añade a la peticion temporal del usuario, despues vuelve a la vista para editar la peticion llamando a [`showAddingRequest`](#showAddingRequest). En caso no ser la ultima, se actualiza la vista para seguir añadiendo tags al deseado llamando a [`showAddingTagsToRequest`](#showAddingTagsToRequest)
    - `cancelAddTags`: cancela el proceso de seleccionar los tags de un deseado y vuelve a la vista del prodcuto con [`showAddingRequest`](#showAddingRequest)
    - `cleanTags`: elimina la lisa de deseados que tiene la peticion que se esta editando y se recarga la vista llamando a [`showAddingRequest`](#showAddingRequest)
- *del_notification*: el comando se utiliza para eliminar la notificacion que le ha saltado al usuario, esta recibe 2 valores, primero el id de la peticion de la que es la notificacion, y despues el id del deseado del la peticion del que es la notificacion. Con esto, a traves del gestor, elimina la notificacion
- *del_request*: el comando se utiliza para eliminar una peticion recibiendo su id como parametro. Con este id y una llamada al gestor elimina la peticion
- *del_whised*: el comando se utiliza para eliminar un deseado de una peticion recibiendo dos parametros. Primero el id de la peticion y despues el id del deseado. Con estos ids y una llamada al gestor elimina el deseado de la peticion

**messageReciber** <a id="messageReciber">

Esta funcion se lanza cuando el usuario escribe un mensaje en el chat de telegram, siempre que no sea el comando `/start`. Esta funcion recibe el usuario que ha escrito el mensaje y el mensaje que ha escrito. Lo primero que hace es comprobar si el usuario esta en la vista correcta para mostrar un producto, en caso contrario, sale de la funcion. Despues, te avisa de que esta procesando el prodcuto y trata de cargar el producto que ha tratado de añadir el usuario, aqui puede suceder 3 cosas:
- *Un url la cual no esta en las tiendas disponibles*: en este caso, te avisara de que la pagina que estas intentando añadir no esta disponible
- *La url es de una tienda disponible pero no correcta o no funciona*: en este caso te avisa de que el producto que estas intentando añadir no es correcto o no existe
- *El prodcuto es correcto*: en este caso te mostrara la vista del prodcuto llamando a la funcion [`showAddingRequest`](#showAddingRequest)

**cmd_start** <a id="cmd_start">

Esa funcion inicializa los valores del usuario para la interfaz y muestra la vista principal que se obtiene de las vistas del archivo de las funciones del bot en `./src/bot/botFunctions.py`. Recibe el usuario sobre el que se van a realizar las acciones

**cmd_help** <a id="cmd_help">

Esta funcion muestra la vista de de la ayuda que se obtiene de las vistas del archivo de las funciones del bot en `./src/bot/botFunctions.py`. Recibe el usuario sobre el que se van a realizar las acciones

**cmd_product_list** <a id="cmd_product_list">

Esta funcion muestra los productos que esta registrando el usuario. Recibe el usuario sobre el que se van a realizar las acciones. Lo primero que hace es mostrar el principio de la vista que se obtiene de las vistas del archivo de las funciones del bot en `./src/bot/botFunctions.py`, seguido muestra por pantalla todos los productos del usuario, y para acabar muestra el final de la vista que se encuentra tambien en el archivo de las funciones

**cmd_add_product** <a id="cmd_add_product">

Esa funcion inicializa los valores del usuario para añadir un producto y muestra la vista de añadir un producto que se obtiene de las vistas del archivo de las funciones del bot en `./src/bot/botFunctions.py`. Recibe el usuario sobre el que se van a realizar las acciones y un mensaje opcional el cual se puede mostrar antes de la vista

**deleteMessage** <a id="deleteMessage">

Esta funcion elimina un mensaje en el chat del usuario. Esta recibe el mensaje que se quiere eliminar, que debe de tener el id del chat y del mensaje que se quiere eliminar. En caso de eliminarse correctamente devuelve `True`, en caso contrario puede pasar 3 cosas, que no se haya podido eliminar porque ya no existe el mensaje (el usuario lo ha borrado) y en este caso devuelve `False`, tambien puede pasar que no sea capaz de borrarlo porque es el mensaje de un grupo y el bot no puede eliminar esos mensajes, en este caso devuelve `False` y avisa por el canal de error lo que ha pasado. Por ultimo, que sea un error extraño que no esta completado, que en ese caso lance el error.

**sendMessage** <a id="sendMessage">

Esta funcion envia un mensaje a un usuario y lo devuelve una vez enviado. Esta funcion recibe los siguientes valores obligatorios:
- *user*: el usuario al que se le quiere enviar el mensaje
- *text*: el texto del mensaje que se quiere enviar, como maximo solo se pueden enviar los 4096 primeros caracteres, por lo que si es de mayor tamaño solo se enviaran esa cantidad de caracteres.

Estos valores ya son opcionales, no son obligatorios:
- *buttons*: Los botones que va a tener el mensaje, debe de tener un formato especifico. Debe de ser una lista, cada elemento de la lista es una fila, despues cada fila debe de tener una lista, que es cada columna de la fila, y por ultimo, cada columna debe de tener una tupla, en la que el primer valor es el texto que va a aparecer en el boton y el segundo el comando que el boton va a enviar. Aqui un ejemplo de como seria:

    ~~~ python
    [[("Bot 1", "cmd_1"), ("Bot 2", "cmd_2")], [("Bot 3", "cmd_3")]]
    ~~~

    Esto, mostraria lo siguiente:

    ~~~
    -----------------
    | Bot 1 | Bot 2 |
    -----------------
    |     Bot 3     |
    -----------------
    ~~~

- *parseMode*: la forma en la que parsea el mensaje para darle estilo al texto, por defecto esta en html y en el archivo de las funciones del bot en `./src/bot/botFunctions.py` hay funciones para formatear con este formato en negrita, subrayado o con enlaces.
- *saveMenssage*: si quieres que el mensaje lo guarde el gestor, esto hace que cuando se eliminen todos los mensajes de un usuario este tambien se borre, por defecto esta a `True`
- *photo*: en caso de que el mensaje vaya con una foto la puedes enviar aqui, la foto debe de estar en formato bytes
- *disableNotification*: si quieres que la notificacion no le suene al usuario puedes activar esta opcion a `True`, por defecto estara en `False`

**sendNotification** <a id="sendNotification">

Esta funcion envia una notificacion a un usuario y lo devuelve una vez enviado. Ademas de esto tambien lo guarda en el gestor como una notificacion. Por dentro lo que hace es llamar a [`sendMessage`](#sendMessage) y guardar el mensaje antes de devolverlo. Recibe los mismos argumentos que [`sendMessage`](#sendMessage) pero sin *saveMenssage* ya que la notificacion no se guarda como un mensaje si no como una notificaion, ni tampoco usa *disableNotification* ya que siempre quieres que suene la notificacion

**getUserAndMessageFromBotsMessageType** <a id="getUserAndMessageFromBotsMessageType">

Esta funcion recibe una clase `Message` de Telebot y si quiere que se elimine el mensaje que se acaba de recibir. Despues esta devuelve el usuario y el mensaje que ha escrito el usuario con la clase que utiliza nuestro bot `Mensaje`.

**copyUsersMessagesToDelete** <a id="copyUsersMessagesToDelete">

Esta funcion recibe un usuario, lo que hace es obtener los mensajes que tiene en su chat y eliminarlos del gestor. Despues, los añade a una varible en la que guarda los mensajes de todos los usuarios para que cuando se llame a la funcion [`deleteCopiedMessages`](#deleteCopiedMessages) se eliminen todos juntos

**deleteCopiedMessages** <a id="deleteCopiedMessages">

Esta funcion recibe un usuario y elimina todos los mensajes del usuario guardados en el bot al utilizar la funcion [`copyUsersMessagesToDelete`](#copyUsersMessagesToDelete)

**showRequest** <a id="showRequest">

Esta funcion recibe una peticion y la muestra con el formato que se obtiene de las vistas del archivo de las funciones del bot en `./src/bot/botFunctions.py`

**showAddingRequest** <a id="showAddingRequest">



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
