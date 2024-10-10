# StoreBot

### Indice

1. [Despliegue del bot](#depliegue)
2. [Documentación](#documentación)   
    2.1. [Documentación del bot](#bot)  
    2.2. [Documentación de la base de datos](#base_de_datos)  
    2.3. [Documentación del gestor](#gestor)  
    2.4. [Implementación de nuevas tiendas](#nuevos_productos)  
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
- *ID_CHAT_AVISOS:* El Id del chat en el que quieres que te lleguen los avisos de las acciones que se realizan en el bot, como registros o acciones de los usuarios
- *ID_CHAT_ERRORES:* El Id del chat en el que quieres que te lleguen los errores que saltan durante la ejecución
- *CREATE_DB*: Indica si quieres que se cree la base de datos durante la ejecución en caso de que no exista. Si no es la primera ejecución del bot, es recomendable dejarla en `false`, si quieres crearlo dejarlo en `true`
- *TESTING:* Indicar si quieres que se ejecute en modo de testing, por defecto dejar en `false`

Una vez creado el archivo se puede desplegar de 2 formas, la recomendable es [utilizando docker](#depliegue_docker), pero si en el dispositivo en el que lo quieres ejecutar no es suficientemente potente o prefieres ejecutarlo directamente, se puede ejecutar con un entorno de python

### Despliegue con docker <a id="depliegue_docker">

Para ejecutarlo utilizando docker simplemente hay que utilizar el siguiente comando:

~~~bash
docker compose up
~~~

En caso de recibir una actualización, añadir `--build` para que actualice el contenedor con los nuevos cambios

Si quieres que el contenedor corra en segundo plano, se puede utilizar `-d`

### Despliegue con entorno de python <a id="depliegue_env">

Para desplegar con un entorno de python, primero hay que crear el entorno, para eso se utiliza el siguiente comando desde el directorio raíz del proyecto:

~~~bash
python -m venv ./env
~~~

Una vez se ha creado el entorno, se descargan las dependencias del proyecto, para eso ejecutamos el pip del entorno descargando las dependencias que están en el proyecto con el siguiente comando:

~~~bash
.\env\Scripts\pip.exe install -r .\dsg\dependencies.txt
~~~

Por ultimo ejecutamos el programa desde el ejecutable del entorno:

~~~bash
.\env\Scripts\python.exe .\src\__main__.py
~~~

## Documentación <a id="documentacion">

Aquí se encuentra toda la documentación sobre el [bot](#bot), la [base de datos](#base_de_datos) y el [gestor](#gestor). Ademas, también esta la información de como [implementar nuevas tiendas](#nuevos_productos)

### Documentación del bot <a id="bot">

La implementación del bot se encuentra en `./src/bot/StoreBot.py`. Esta clase hereda de la clase `Telebot` de la librería telebot, con la que te facilita hacer las peticiones para la API de telegram. 

#### Funcionamiento

A la hora de inicializar el bot, este recibe el token del bot de la API de telegram y la clase del [gestor](#gestor) que va a utilizar. Una vez inicializado el bot aun no funciona, hay que llamar a la función [`startMainLoop()`](#startMainLoop) la cual inicia un bucle infinito que comienza a controlar las peticiones

**startMainLoop** <a id="startMainLoop"/>

Esta función inicia el bucle infinito de escucha del bot, este comprueba constantemente las actualizaciones del bot llamando a la función correspondiente de `Telebot`, esto siempre que no se haya detenido fijando la variable del bucle a `false`

**inicializeCommands** <a id="startMainLoop"/>

Esta función inicializa los siguientes comandos del bot:

- La función que atenderá las respuestas por texto que recibe el bot llamando a [`messageReciber`](#messageReciber)
- La función que al el bot y cuando se utiliza su comando `/start`. Esta llama a [`buttonsControler`](#buttonsControler) con el comando de inicio
- La función que gestiona cuando se pulsa un botón, llamando a [`buttonsControler`](#buttonsControler) con el comando del botón que se haya pulsado 

**buttonsControler** <a id="buttonsControler">

Esta función se lanza cuando el usuario ha pulsado un botón en la interfaz de telegram. Esta recibe un usuario y los datos a procesar. Los datos son una cadena de caracteres, en la que hay varias instrucciones separadas por `_-_`, la primera es el comando a utilizar, y el resto los argumentos que recibe. Gestiona los siguientes comandos

- *cmd_start*: el comando que se ejecuta cuando se va a la pagina principal del bot, llama a la función [`cmd_start`](#cmd_start)
- *cmd_help*: el comando que se ejecuta cuando se va a la pagina de ayuda del bot, llama a la función [`cmd_help`](#cmd_help)
- *cmd_products_list*: el comando que gestiona la pagina de los productos del usuario. Este, si no recibe ningún argumento lo que hace es mostrar la pagina con los productos del usuario llamando a la función [`cmd_products_list`](#cmd_products_list). En caso de tener argumentos, puede tener 2:
    - `remove`: este elimina la petición con el id que reciba como argumento. Esto lo hace eliminándolo del gestor y seguido refrescando la vista del usuario llamando a [`cmd_products_list`](#cmd_products_list) 
    - `edit`: este abre la vista para poder editar la petición con el id que reciba de argumento. Para esto llama a [`showAddingRequest`](#showAddingRequest) habiendo fijado la petición como la editable
- *cmd_add_product*: el comando que se ejecuta cuando se va a la pagina de añadir un producto del bot, llama a la función [`cmd_add_product`](#cmd_add_product)
- *add_product*: el comando que se llama para gestionar un producto que se esta gestionando o añadiendo. Este puede recibir los siguientes argumentos:
    - `addTags`: este inicializa los valores para poder añadir un deseado a la petición de un producto. Después llama a [`showAddingTagsToRequest`](#showAddingTagsToRequest) para que muestre la selección de las tags
    - `save`: este guarda la petición del producto que esta añadiendo el usuario a través del gestor, y después llama a [`cmd_add_product`](#cmd_add_product) para volver a la vista de añadir un producto con el aviso de que se ha guardado el producto correctamente
    - `tagSelected`: recibe una tag para añadir a un deseado de una petición. En caso de ser la ultima tag que se pueda añadir al deseado, crea el objeto del deseado y lo añade a la petición temporal del usuario, después vuelve a la vista para editar la petición llamando a [`showAddingRequest`](#showAddingRequest). En caso no ser la ultima, se actualiza la vista para seguir añadiendo tags al deseado llamando a [`showAddingTagsToRequest`](#showAddingTagsToRequest)
    - `cancelAddTags`: cancela el proceso de seleccionar los tags de un deseado y vuelve a la vista del producto con [`showAddingRequest`](#showAddingRequest)
    - `cleanTags`: elimina la lisa de deseados que tiene la petición que se esta editando y se recarga la vista llamando a [`showAddingRequest`](#showAddingRequest)
- *del_notification*: el comando se utiliza para eliminar la notificación que le ha saltado al usuario, esta recibe 2 valores, primero el id de la petición de la que es la notificación, y después el id del deseado del la petición del que es la notificación. Con esto, a través del gestor, elimina la notificación
- *del_request*: el comando se utiliza para eliminar una petición recibiendo su id como parámetro. Con este id y una llamada al gestor elimina la petición
- *del_whised*: el comando se utiliza para eliminar un deseado de una petición recibiendo dos parámetros. Primero el id de la petición y después el id del deseado. Con estos ids y una llamada al gestor elimina el deseado de la petición

**messageReciber** <a id="messageReciber">

Esta función se lanza cuando el usuario escribe un mensaje en el chat de telegram, siempre que no sea el comando `/start`. Esta función recibe el usuario que ha escrito el mensaje y el mensaje que ha escrito. Lo primero que hace es comprobar si el usuario esta en la vista correcta para mostrar un producto, en caso contrario, sale de la función. Después, te avisa de que esta procesando el producto y trata de cargar el producto que ha tratado de añadir el usuario, aquí puede suceder 3 cosas:
- *Un url la cual no esta en las tiendas disponibles*: en este caso, te avisara de que la pagina que estas intentando añadir no esta disponible
- *La url es de una tienda disponible pero no correcta o no funciona*: en este caso te avisa de que el producto que estas intentando añadir no es correcto o no existe
- *El producto es correcto*: en este caso te mostrara la vista del producto llamando a la función [`showAddingRequest`](#showAddingRequest)

**cmd_start** <a id="cmd_start">

Esa función inicializa los valores del usuario para la interfaz y muestra la vista principal que se obtiene de las vistas del archivo de las funciones del bot en `./src/bot/botFunctions.py`. Recibe el usuario sobre el que se van a realizar las acciones

**cmd_help** <a id="cmd_help">

Esta función muestra la vista de de la ayuda que se obtiene de las vistas del archivo de las funciones del bot en `./src/bot/botFunctions.py`. Recibe el usuario sobre el que se van a realizar las acciones

**cmd_product_list** <a id="cmd_product_list">

Esta función muestra los productos que esta registrando el usuario. Recibe el usuario sobre el que se van a realizar las acciones. Lo primero que hace es mostrar el principio de la vista que se obtiene de las vistas del archivo de las funciones del bot en `./src/bot/botFunctions.py`, seguido muestra por pantalla todos los productos del usuario, y para acabar muestra el final de la vista que se encuentra también en el archivo de las funciones

**cmd_add_product** <a id="cmd_add_product">

Esa función inicializa los valores del usuario para añadir un producto y muestra la vista de añadir un producto que se obtiene de las vistas del archivo de las funciones del bot en `./src/bot/botFunctions.py`. Recibe el usuario sobre el que se van a realizar las acciones y un mensaje opcional el cual se puede mostrar antes de la vista

**deleteMessage** <a id="deleteMessage">

Esta función elimina un mensaje en el chat del usuario. Esta recibe el mensaje que se quiere eliminar, que debe de tener el id del chat y del mensaje que se quiere eliminar. En caso de eliminarse correctamente devuelve `True`, en caso contrario puede pasar 3 cosas, que no se haya podido eliminar porque ya no existe el mensaje (el usuario lo ha borrado) y en este caso devuelve `False`, también puede pasar que no sea capaz de borrarlo porque es el mensaje de un grupo y el bot no puede eliminar esos mensajes, en este caso devuelve `False` y avisa por el canal de error lo que ha pasado. Por ultimo, que sea un error extraño que no esta completado, que en ese caso lance el error.

**sendMessage** <a id="sendMessage">

Esta función envía un mensaje a un usuario y lo devuelve una vez enviado. Esta función recibe los siguientes valores obligatorios:
- *user*: el usuario al que se le quiere enviar el mensaje
- *text*: el texto del mensaje que se quiere enviar, como máximo solo se pueden enviar los 4096 primeros caracteres, por lo que si es de mayor tamaño solo se enviaran esa cantidad de caracteres.

Estos valores ya son opcionales, no son obligatorios:
- *buttons*: Los botones que va a tener el mensaje, debe de tener un formato especifico. Debe de ser una lista, cada elemento de la lista es una fila, después cada fila debe de tener una lista, que es cada columna de la fila, y por ultimo, cada columna debe de tener una tupla, en la que el primer valor es el texto que va a aparecer en el botón y el segundo el comando que el botón va a enviar. Aquí un ejemplo de como seria:

    ~~~ python
    [[("Bot 1", "cmd_1"), ("Bot 2", "cmd_2")], [("Bot 3", "cmd_3")]]
    ~~~

    Esto, mostraría lo siguiente:

    ~~~
    -----------------
    | Bot 1 | Bot 2 |
    -----------------
    |     Bot 3     |
    -----------------
    ~~~

- *parseMode*: la forma en la que paresa el mensaje para darle estilo al texto, por defecto esta en html y en el archivo de las funciones del bot en `./src/bot/botFunctions.py` hay funciones para formatear con este formato en negrita, subrayado o con enlaces.
- *saveMenssage*: si quieres que el mensaje lo guarde el gestor, esto hace que cuando se eliminen todos los mensajes de un usuario este también se borre, por defecto esta a `True`
- *photo*: en caso de que el mensaje vaya con una foto la puedes enviar aquí, la foto debe de estar en formato bytes
- *disableNotification*: si quieres que la notificación no le suene al usuario puedes activar esta opción a `True`, por defecto estará en `False`

**sendNotification** <a id="sendNotification">

Esta función envía una notificación a un usuario y lo devuelve una vez enviado. Ademas de esto también lo guarda en el gestor como una notificación. Por dentro lo que hace es llamar a [`sendMessage`](#sendMessage) y guardar el mensaje antes de devolverlo. Recibe los mismos argumentos que [`sendMessage`](#sendMessage) pero sin *saveMenssage* ya que la notificación no se guarda como un mensaje si no como una notificaron, ni tampoco usa *disableNotification* ya que siempre quieres que suene la notificación

**getUserAndMessageFromBotsMessageType** <a id="getUserAndMessageFromBotsMessageType">

Esta función recibe una clase `Message` de Telebot y si quiere que se elimine el mensaje que se acaba de recibir. Después esta devuelve el usuario y el mensaje que ha escrito el usuario con la clase que utiliza nuestro bot `Mensaje`.

**copyUsersMessagesToDelete** <a id="copyUsersMessagesToDelete">

Esta función recibe un usuario, lo que hace es obtener los mensajes que tiene en su chat y eliminarlos del gestor. Después, los añade a una variable en la que guarda los mensajes de todos los usuarios para que cuando se llame a la función [`deleteCopiedMessages`](#deleteCopiedMessages) se eliminen todos juntos

**deleteCopiedMessages** <a id="deleteCopiedMessages">

Esta función recibe un usuario y elimina todos los mensajes del usuario guardados en el bot al utilizar la función [`copyUsersMessagesToDelete`](#copyUsersMessagesToDelete)

**showRequest** <a id="showRequest">

Esta función recibe una petición y la muestra con el formato que se obtiene de las vistas del archivo de las funciones del bot en `./src/bot/botFunctions.py`

**showAddingRequest** <a id="showAddingRequest">

Esta función recibe un usuario y un mensaje opcional extra. Esta lo que hace es mostrar el producto que esta añadiendo el usuario con los botones necesarios para interactuar con el y poderle añadir avisos, limpiar los avisos que ya tenga, guardar el producto como esta o cancelar lo que se esta haciendo con el producto. Esto lo hace llamando a [`showRequest`](#showRequest) con los botones necesarios para llamar a esas funcionalidades. Por ultimo, si había un mensaje opcional extra, lo envías

**showAddingTagsToRequest** <a id="showAddingTagsToRequest">

Esta función recibe un usuario y lo que hace es mostrar las tags que puede seguir seleccionando y llama a [`showRequest`](#showRequest) con ellas. Ademas también añade otro botón para cancelar el seguir añadiendo tags.

### Documentación de la base de datos <a id="base_de_datos">

La base de datos esta implementada en una base de datos SQLite, el archivo con el que se crea esta se encuentra en `src/dataBase/database.sql`. Esta esta diseñada de la siguiente forma:

![Descripción de la imagen](dsg/Base%20de%20datos.PNG)

Toda la base de datos se gestiona desde la clase `src/dataBase/DataBase.py`. En ese archivo hay unas clases para utilizar las tablas y los atributos de las tablas como constantes. La el constructor de clase `Database` recibe la dirección en la que se encuentra el archivo de la base de datos, que en caso de no existir lanza un error. Si no esta creada la base de datos, hay que llamar antes al método estático de la clase `startDataBase`, que recibe la dirección donde quieres crear el archivo de la base de datos (en caso de ya existir el archivo cuidado que lo eliminará) y el archivo con el que se genera la base de datos. 

#### Funciones para el uso del SQL

Para la gestión de todas las instrucciones SQL se utilizan unas funciones base para hacer mucho mas sencilla su utilización y evitar los errores. Estas son la funciones [`funSelect`](#funSelect), [`funInsert`](#funInsert), [`funDelete`](#funDelete) y [`funUpdate`](#funUpdate)

**funSelect** <a id="funSelect">

Esta función sirve para hacer un select a la base de datos, esta recibe la tabla sobre la que se quiere hacer hacer el select. A parte de esto, también puede recibir unos valores opcionales:

- *columns:* una lista de las columnas que quieres obtener, por defecto son todas.

- *conditions:* una lista de las condiciones que quieres que cumplan tus resultados, esta debe de ser una lista de strings con condiciones, estas <u>se separan siempre por un AND</u>.

- *order:* una lista con los valores que se quieren utilizar para ordenar los resultados

**funInsert** <a id="funInsert">

Esta función sirve para hacer un insert a la base de datos, esta recibe la tabla sobre la que se quiere hacer hacer el insert, si quieres que se realice el commit después de la instrucción (por defecto si) y por ultimo los valores que hay que añadir, referenciando, por ejemplo asi se añadiría un usuario nuevo

~~~python
funInsert(TABLAS.Usuarios, commit=False, chatId=122323, username="usuario")
~~~

**funDelete** <a id="funDelete">

Esta función sirve para hacer un delete a la base de datos, esta recibe la tabla sobre la que se quiere hacer hacer el delete. A parte de esto, también puede recibir unos valores opcionales:

- *conditions:* una lista de las condiciones que quieres que cumplan tus resultados, esta debe de ser una lista de strings con condiciones, estas <u>se separan siempre por un AND</u>.

- *commit:* indica si quieres que se guarde la base de datos después de la instrucción, por defecto si

**funUpdate** <a id="funUpdate">

Esta función sirve para hacer un update a la base de datos, esta recibe la tabla sobre la que se quiere hacer hacer el update. A parte de esto, también puede recibir unos valores opcionales:

- *conditions:* una lista de las condiciones que quieres que cumplan las filas que quieres que se editen, esta debe de ser una lista de strings con condiciones, estas <u>se separan siempre por un AND</u>.

- *commit:* indica si quieres que se guarde la base de datos después de la instrucción, por defecto si

- *valores a editar:* los valores que hay que editar, los referencias, como se hacia en [`funInsert`](#funInsert) para añadir

#### Funciones externas

Una vez creadas las funciones para acceder a base de datos, se crean las siguientes funciones para que el [`Gestor`](#gestor) pueda acceder a la base de datos de forma sencilla. Estas son las funciones que puedes hacer:

**loadGestorData** <a id="loadGestorData">

Esta función recibe un [`Gestor`](#gestor) y lo carga con los datos de la base de datos. Esta es una función compleja que debe de cargar todos los productos, por ello si el [`Gestor`](#gestor) tiene definía la [`funReporte`](#funReporte) notifica la cantidad de productos carga.

**Añadir una nueva instancia** <a id="anhadir_instancia">

Existen las siguientes funciones para añadir una nueva instancia en base de datos: `saveProducto`, `saveMensaje`, `saveNotificacion`, `savePeticion`, `saveDeseado` y `saveUsuario`. Todas reciben la clase que se quiere guardar y opcionalmente puede pasarse el valor de commit, que si lo pasas a false no hará un commit de la base de datos, este por defecto esta a True.

**Eliminar de la base de datos** <a id="eliminar_instacia">

Para eliminar de la base de datos existen varias funciones, todas estas pueden recibir una variable `commit` para indicar si quieres que se guarden los cambios o no al final de la función. Las funciones son las siguientes:

- *deleteProducto:* recibe un producto y lo elimina de la base de datos
- *deleteAllMensajesFromUsuario:* recibe un usuario y elimina todos los mensajes de  tanto de la clase como de la base de datos.
- *deletePeticion:* recibe una petición y la elimina de la base de datos, tanto a la petición como los deseados y avisos
- *deleteDeseado:* recibe un deseado y lo elimina de base de datos, ademas si la tabla de `TagName` se queda sin elementos que referenciar lo elimina también
- *deletePeticionPriceMessage:* recibe una petición y elimina de base de datos el deseado asignado al aviso de bajada de precio

**Actualizar la base de datos** <a id="actulizar_instancia">

Para actualizar información en la base de datos existen varias funciones, todas estas pueden recibir una variable `commit` para indicar si quieres que se guarden los cambios o no al final de la función. Las funciones son las siguientes:

- *updateUsuarioUsername:* recibe un usuario, al cual le actualiza el user name en la base de datos
- *updatePeticion:* recibe una petición y si quieres que se actualicen los deseados o no. Si no actualizas los deseados no se actualizaran las notificaciones
- *updatePeticionPriceMessage:* recibe una petición y actualiza en base de datos el mensaje del aviso del precio en caso de haber, y si no hay lo crea
- *updateDeseado:* recibe un deseado y edita su mensaje en la base de datos. Cuidado ya que este método no edita las tags, unicamente edita el mensaje

**Obtener información de la base de datos** <a id="get_instancia">

Para obtener información de la base de datos están las siguientes funciones:

- *checkIfProductInRequest:* recibe un producto y retorna un booleano que te indica si el producto se encuentra en alguna petición
- *getWishedsForRequest:* recibe una petición y retorna una lista con todos los deseados asignados a esa petición
- *getTagNameId:* recibe un nombre a asignar a una tag, en caso de existir la tag devuelve su id en base de datos, en caso de no existir la crea y devuelve su id
- *getWishedTags:* recibe el id de un deseado y devuelve una lista con las tags en orden
- *getAllProducts:* esta función se encarga de cargar todos los productos en un diccionario en el que la clave es el id del producto y el valor el propio producto. Como es una función pesada ya que cargar todos los productos implica hacer muchas peticiones y cargar mucha información puede recibir un notificar (no obligatorio, por defecto es `None`), que es una función la cual debe de poder recibir un string, y cada vez que carga un producto lo notifica diciendo cuantos lleva y el nombre del producto que ha cargado.

### Documentación del gestor <a id="gestor">

El gestor es una clase intermedia que se encarga de la comunicación entre el bot y la base de datos. Este también se encarga de ir actualizando los precios y stocks de los productos y avisar en caso de ser necesario al bot para lanzar los avisos a los usuarios.

Para inicializar el gestor son necesarios los siguientes pasos:
- Inicializar al gestor llamando a su constructor, este recibe la clase `DataBase` que va a utilizar y un bolean opcional para indicar si se quieren cargar los datos de la base de datos en el gestor en el momento de inicializar o no, recomendable al principio en False para asignarle otros valores al gestor antes.
- Fijar la función `funDelMessage`, que es la que se utilizara para intentar borrar un mensaje enviado a un usuario, como notificaciones. Para esto debemos de fijarle una función que llame al bot para eliminar el mensaje que reciba como parámetro
- Fijar la función `funNotificateUser`, que se utilizara para notificar al usuario, esta debe de recibir 2 argumentos, el usuario al que se va a notificar y el texto del mensaje que se le va a enviar
- Fijar la función `funError`, la cual debe de recibir un string. Esta la utilizan el gestor y el bot para notificar errores al desarrollador. En este caso esta hecho para que si en esta en modo test (editable en las variables de entorno) lo pinte por la terminal, y si no lo haga por el chat de telegram que este indicado en las constantes
- Fijar la función `funReporte` <a id="funReporte">, esta tiene la misma función que la función anterior `funError`. Esta en vez de notificar errores, notifica avisos al desarrollador sobre lo que esta sucediendo.
- Iniciar el gestor, para esto se llama a la función `initTheGestor` que carga todos los datos de la base de datos, este proceso es lento, por lo que se utiliza `funReporte` para ir avisando sobre la carga de productos
- Por ultimo hay que llamar a la función `startMainLoop`, que comienza el bucle que actualiza los productos y notifica a los usuarios. En este caso se hace en un hilo, para poder lanzar mas procesos.

Las funciones que tiene el gestor son las siguientes:

**initTheGestor** <a id="initTheGestor">

Comprueba que las funciones para el funcionamiento del bot han sido iniciadas y carga la base de datos

**getUserFromMessage** <a id="getUserFromMessage">

Recibe un mensaje retorna el usuario del mensaje. En caso de existir en la base de datos comprueba si ha cambiado el username antes de devolverlo, para así actualizarlo. En caso de no estar en la base de datos lo añade y manda un reporte de que lo ha añadido

**deleteUsersMessages** <a id="deleteUsersMessages">

Recibe un usuario, elimina sus mensajes de la base de datos y de la clase del usuario y retorna una copia de los mensajes que ha eliminado

**saveMessage** <a id="saveMessage">

Recibe un mensaje, lo añade al usuario y lo añade a la base de datos

**saveNotification** <a id="saveNotification">

Recibe un mensaje, lo añade al usuario como una notificación y la guarda en la base de datos como una notificación

**startProduct** <a id="startProduct">

Recibe un usuario y la url de un producto. En caso de ser un producto de un dominio que no se encuentra en el bot devuelve un -1, en caso de no se un producto válido devuelve un -2 y en caso de ser un producto valido, se crea una petición con ese producto en la petición temporal de usuario (en caso de ya haber una petición de ese producto por el usuario fija esa misma) y retorna un 0

**saveTemporalRequest** <a id="saveTemporalRequest">

Recibe un usuario y guarda la petición temporal que esta editando. En caso de el producto no estar en el gestor, lo añade y lo guarda en la base de datos. Por ultimo, comprueba si la petición es nueva o la esta editando, si es nueva la añade y la crea, y si la esta editando actualiza sus valores

**removeRequest** <a id="removeRequest">

Recibe un usuario y el id de una petición, elimina la petición del usuario, elimina las notificaciones de la petición en caso de tener y elimina la petición de la base de datos. En caso de que el producto no lo utilice ninguna otra petición, lo elimina del gestor y de la base de datos.

**deleteNotification** <a id="deleteNotification">

Recibe un usuario, el id de una petición y el id de un deseado. Si el id del deseado es "precio", elimina la notificación del precio. Si no, elimina la notificación del deseado con ese id

**deleteWished** <a id="deleteWished">

Recibe un usuario, el id de una petición y el id de un deseado. Si el deseado de la petición existe, lo elimina y en caso de tener una notificación también lo elimina

**startMainLoop** <a id="startMainLoop">

Bucle principal que actualiza los productos y notifica a los usuarios cuando cuando tiene una petición disponible. Esta función puede recibir un booleano para que pinte por consola las actualizaciones, por defecto a False

**mannageUpdateProductError** <a id="mannageUpdateProductError">

Se llama a esta función cuando ha ocurrido un error al actualizar un producto en el bucle principal. Esta avisa del error.

**mannageCheckRequestError** <a id="mannageCheckRequestError">

Se llama a esta función cuando ha ocurrido un error comprobar una petición en el bucle principal. Esta avisa del error.

**stopMainLoop** <a id="stopMainLoop"> 

Esta función se encarga de detener el bucle principal en el momento que acabe la iteración actual

### Implementación de nuevas tiendas <a id="nuevos_productos">

Para añadir nuevas tiendas se hace a través de herencia del la clase ``Producto`` con la implementación aquí explicada`'

1. [Ubicación](#ubicacion)  
2. [Funciones](#funciones)  
    2.1 [Constantes](#constantes)  
    2.2 [Inicializador](#inicializador)  
    2.3 [Descarga datos](#descarga_datos)  
    2.4 [Inicia nombre](#inicia_nombre)  
    2.5 [Actualiza tags](#actualiza_tags)  
    2.6 [Obtén precio](#obten_precio)  
    2.7 [Obtén foto](#obten_foto)  
    2.8 [Equal](#equal)  
    2.9 [String](#string)  
3. [Implementación](#implementación)
4. [Consejos](#consejos)

#### Ubicación <a id="ubicacion"/>

La ubicación de los productos ha de ser en la carpeta de ser dentro del dominio, en la carpeta de productos

#### Funciones <a id="funciones"/>

Estas son las funciones que has de implementar para realizar una correcta clase que pueda utilizar el gestor

**Constantes** <a id="constantes">

La clase ha de tener una constante que indique cual es el dominio de la tienda, aparte de esto, es recomendable tener también tener una constante de la dirección de la petición que hay que realizar y otra del los headers de la petición

**Inicializador** <a id="inicializador">

~~~python
def __init__(self, url, id) -> None:
~~~

Al inicializar la función se deben de inicializar todos los datos necesarios para la gestión del producto, sin realizar ninguna petición, esto se hará en el siguiente paso. Que no se te olvide llamar a la clase padre con ``super().__init__(url, id)``. Aparte, esta función también ha de lanzar una excepción ``ValueError(THE ERROR)``. Esta excepción se lanzara en caso de no haber escrito un producto correcto

**Descargar datos** <a id="descarga_datos">

~~~python
def descargaDatos(self) -> None:
~~~

Esta función unicamente se encarga de descargar los datos y guardarlos en la clase, no hace ningún otro tipo de operación. Esta función también lanza una excepción ``RuntimeError(THE ERROR)`` en caso de que suceda algún problema a la hora de la descarga de los datos

**Inicia nombre** <a id="inicia_nombre">

~~~python
def iniciaNombre(self) -> None:
~~~

Esta función unicamente debe de inicializar el nombre del producto con los datos descargados previamente

**Actualiza tags** <a id="actualiza_tags">

~~~python
def actualizaTags(self) -> None:
~~~

Con los datos descargados, esta función debe de actualizar los tags del producto. Los tags son un diccionario de obligatoriamente un elemento. En cada clave puede haber o un ``bool`` o otro ``dic``. El booleano indica si hay stock de los datos anteriores y el diccionario indica otro tipo de dato distinto. Un ejemplo del tag puede ser el siguiente:

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

**Obtén precio** <a id="obten_precio">

~~~python
def obtenPrecio(self) -> float:
~~~

Obtiene el precio de los datos descargados y lo devuelve como un ``float``, no lo actualiza, unicamente lo devuelve

**Obtén foto** <a id="obten_foto">

~~~python
def obtenFoto(self) -> bytes:
~~~

Obtiene la foto del producto en formato ``bytes`` ("rb") y lo retorna. En caso de no tener foto o no encontrar la forma de obtenerla devolver ``None``

**Equal** <a id="equal">

~~~python
def __eq__(self, __value: object) -> bool:
~~~

Necesita crear la función para comprobar si dos productos son iguales. Importante que compruebe si es del mismo tipo de producto primero y después lo compare con lo que deberían de ser iguales

**String** <a id="string">

~~~python
def __str__(self) -> str:
~~~

Para facilitar su debug, implementar la clase para que al ser pintado el objeto se pueda mostrar correctamente de que tipo es e información relevante sobre el mismo. Recomendable identificarlo con el nombre del producto y un valor característico de la tienda

#### Implementación <a id="implementacion"/>

Para la implementación de la clase y que funcione correctamente hay que añadir el producto al archivo ``ListaProductos.py``. Para esto hay que importarlo desde la carpeta y añadirlo al diccionario, la llave debe de ser el dominio del producto y el valor la clase heredada

#### Consejos <a id="consejos"/>

Puedes utilizar la función ``pprint()`` de la librería pprint para pintar por pantalla los ``json`` y poder trabajar mejor con ellos

## Sobre mi <a id="sobre_mi">

Hecho por Pablo Landeras, estudiante de ingeniería informática en la universidad de Cantabria.

**Contacto**:  
- Email: pablolanderas@gmail.com  
- LinkedIn: [https://www.linkedin.com/in/pablo-landeras/](https://www.linkedin.com/in/pablo-landeras/)
