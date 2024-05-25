from dominio import Peticion, Mensaje
from os import path

from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup

# Format functions
def negrita_html(texto:str): return f"<b>{texto}</b>"
def subrayado_html(texto:str): return f"<u>{texto}</u>"
def enclace_html(texto, enlace): return f'<a href="{enlace}">{texto}</a>'
def negrita_markdown(message): return f"*{message}*"
def enlace_markdown(texto, enlace): return f'[{texto}]("{enlace}")'

# Functions for the bot
def generateButtons(buttons) -> InlineKeyboardMarkup:
    obtButtons = []
    for fila in buttons:
        obtButtons.append(list(map(
            lambda x: InlineKeyboardButton(x[0], callback_data=x[1]), 
        fila)))
    return InlineKeyboardMarkup(obtButtons)

def funToSendAdvise(peticion: Peticion, message: Mensaje, codigo: str, bot)-> Mensaje:
    producto = peticion.producto
    message = negrita_html("Nuevo precio para "+enclace_html(producto.nombre, producto.url)) + "\n\n" + message
    photo = producto.obtenFoto()
    if codigo == "precio":
        buttons = [[("Borrar peticion", f"del_request {peticion.idPeticion}")]]
    else:
        buttons = [[("Borrar peticion", f"del_request {peticion.idPeticion}"), ("Borrar deseado", f"del_whised {peticion.idPeticion} {codigo}")]]
    buttons.append([("Cerrar aviso", f"del_notification {peticion.idPeticion} {codigo}")])
    return bot.sendMessage(peticion.usuario, message, buttons=buttons, photo=photo, saveMessage=False)

def funToDeleteMessage(peticion: Peticion, message: Mensaje, bot):
    message.chatId = peticion.usuario.chatId
    bot.deleteMessage(message)

# The formats
HTML_FORMAT = "html"

# The bot commands
COMANDOS = [
    ("cmd_start",  "Inicio", "Vuelve al inicio"),
    ("cmd_products_list",  "Lista de peticiones", "Muestra una lista con todas tus peticiones de productos"),
    ("cmd_add_product", "Añadir producto", "Añade un nuevo producto"),
    ("cmd_help",  "Mostrar ayuda", "Muestra ayuda de como funciona el bot"),
]

BARRA_SEPARADORA = "______________________________________"

"""
The views returns 4 objects in the same orden alwais
text, photo, butons, parseMode
"""

def START_VIEW():
    # The text
    text = f"{negrita_html('Bienvenido a StoreBot')}\n\n"
    text += f"{subrayado_html('Estos son las funciones que puedes hacer:')}\n" 
    # The photo
    photo = open(path.join(".", "resources", "TiendaOnline.jpg"), "rb")
    # The buttones
    buttons = []
    for cmd, shortText, longText in COMANDOS[1:]:
            buttons.append([(shortText, cmd)])

    return text, photo, buttons, HTML_FORMAT

def HELP_VIEW():
    # The text
    text = f"{subrayado_html(negrita_html('Estas son todas las funciones posibles:'))}\n\n"
    for cmd, shortText, longText in COMANDOS:
        text += f"{subrayado_html(negrita_html(shortText))}: {longText}\n\n"
    # The photo
    photo = open(path.join(".", "resources", "ayuda.png"), "rb")
    # The buttones
    buttons = [[("Volver inicio", "cmd_start")]]

    return text, photo, buttons, HTML_FORMAT

def PRODUCT_LIST_HEADER_VIEW():
    # The text
    text = negrita_html(subrayado_html("Lista de productos:"))+"\n"+BARRA_SEPARADORA
    # The photo
    photo = open(path.join(".", "resources", "lista.png"), "rb")
    # The buttones
    buttons = None

    return text, photo, buttons, HTML_FORMAT

def PRODUCT_LIST_FOOTER_VIEW():
    # The text
    text = BARRA_SEPARADORA
    # The photo
    photo = None
    # The buttones
    buttons = [[("Volver inicio", "cmd_start")]]

    return text, photo, buttons, HTML_FORMAT

def REQUEST_VIEW(request: Peticion):
    product = request.producto
    # The text
    text  = f"{enclace_html(product.nombre, product.url)}\n\n"
    #text += f"{enclace_html('Enlace', product.url)}\n\n"
    text += f"{subrayado_html('Avisos:')}\n"
    text += f"-Bajada de precio\n"
    for wished in request.deseados:
        text += f"-{' - '.join(wished.tags)}\n"
    # The photo
    photo = product.obtenFoto()
    # The buttons
    buttons = None

    return text, photo, buttons, HTML_FORMAT

def ADD_PRODUCT_VIEW():
    # The text
    text = "Introduce el URL del producto que quieres comprobar"
    # The photo
    photo = open(path.join(".", "resources", "enlace.png"), "rb")
    # The buttones
    buttons = [[("Volver inicio", "cmd_start")]]

    return text, photo, buttons, HTML_FORMAT
