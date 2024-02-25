# StoreBot

**TODOS:**

    -Gestionar que hacer con las notificaciones cuando se elimina un Deseado que   
     ha sido notificado.  
    -Mismo problema cuando se elimina una peticion con el aviso del precio
    -Info delpliegue
    -Info "Sobre mi"
    -Gestionar caso de no escribir los chat de aviso del bot en las constantes

## Indice

1. [Despligue del bot](#depliegue)
2. [Documentacion](#documentacion)   
    2.1. [Documentacion del bot](#bot)  
    2.2. [Docuemtnacion de la base de datos](#base_de_datos)  
    2.3. [Documentacion del gestor](#gestor)  
    2.4. [Implementacion de nuevas tiendas](#nuevos_productos)  
3. [Sobre mi](#sobre_mi)

## Despliegue <a id="depliegue">

*Estos son los pasos para poder desplegar el bot:* 

Lo primero es iniciar el entorno virtual ``env`` con el siguiente comando:
    
    py -m venv env

Despues hay que activar el entorno virutal, este paso se ha de realizar siempre que se salga del mismo para poder ejecutar correctamente el programa. Para poder entrar al entorno virual se haría con el siguiente comando:

    .\env\Scripts\activate

Ahora habria que descargar las dependencias del proyecto, para esto hay que introducir el siguiente comando:

    pip install -r .\dsg\dependencies

Complentar la plantilla de las constantes con el token del bot y llamar al archilvo ``Constantes.py``. Opcionalmente, puedes escribir dos ``ChatId`` para que los reportes y errores del bot los notifique por esos chats. En caso de no escribir estas variables, dejar el valor de esas a ``None`` y la informacion unicamente se escribira por la consola

Por ultimo, puedes ejecutar el bot con el siguiente comando:

    py .\src\__main__.py

Si en cualquier momento deseas salir del entorno, simplemente seria escribir lo siguiente en el terminal:

    deactivate

## Documentacion <a id="documentacion">

Aqui se encuentra toda la documentacion sobre el [bot](#bot), la [base de datos](#base_de_datos) y el [gestor](#gestor). Ademas, tambien esta la informacion de como [implementar nuevas tiendas](#nuevos_productos)

**Documentacion del bot** <a id="bot">

**Documentacion de la base de datos** <a id="base_de_datos">

**Documentacion del gestor** <a id="gestor">

**Implementacion de nuevas tiendas** <a id="nuevos_productos">

Toda la informacion de referencia sobre este tema se encuentra [aqui](https://github.com/pablolanderas/StoreBot/blob/main/dsg/document.md)

## Sobre mi <a id="sobre_mi">

Hecho por [Pablo Landeras](pablolanderas@gmail.com)
