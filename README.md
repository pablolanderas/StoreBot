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

Para desplegar el bot, primero hay que crear las variables de entorno, para esto hay que crear un archivo `.env` en el directorio del proyecto. Este archivo debe de tener lo siguiente:

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

Una vez creado este archivo, simplemente hay que utilizar el siguiente comando:

~~~bash
docker compose up
~~~

En caso de recibir una actualizacion, añadir `--build` para que actualice el conetenedor con los nuevos cambios

Si quieres que el contenedor corra en segundo plano, se puede utilizar `-d`

## Documentacion <a id="documentacion">

Aqui se encuentra toda la documentacion sobre el [bot](#bot), la [base de datos](#base_de_datos) y el [gestor](#gestor). Ademas, tambien esta la informacion de como [implementar nuevas tiendas](#nuevos_productos)

**Documentacion del bot** <a id="bot">

**Documentacion de la base de datos** <a id="base_de_datos">

**Documentacion del gestor** <a id="gestor">

**Implementacion de nuevas tiendas** <a id="nuevos_productos">

Toda la informacion de referencia sobre este tema se encuentra [aqui](https://github.com/pablolanderas/StoreBot/blob/main/dsg/document.md)

## Sobre mi <a id="sobre_mi">

Hecho por Pablo Landeras, estudiante de ingenieria informatica en la universidad de Cantabria.

**Contacto**:  
- Email: pablolanderas@gmail.com  
- [Linkedin](#https://www.linkedin.com/in/pablo-landeras-583578242/)
