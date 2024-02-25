from dominio.Peticion import Peticion

from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup

# Functions for the bot
def generateButtons(buttons) -> InlineKeyboardMarkup:
    obtButtons = []
    for fila in buttons:
        obtButtons.append(list(map(
            lambda x: InlineKeyboardButton(x[0], callback_data=x[1]), 
        fila)))
    return InlineKeyboardMarkup(obtButtons)

# The formats
HTML_FORMAT = "html"

# Format functions
def negrita_html(texto:str): return f"<b>{texto}</b>"
def subrayado_html(texto:str): return f"<u>{texto}</u>"
def enclace_html(texto, enlace): return f'<a href="{enlace}">{texto}</a>'
def negrita_markdown(message): return f"*{message}*"
def enlace_markdown(texto, enlace): return f'[{texto}]("{enlace}")'

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
    photo = open("./resources/TiendaOnline.jpg", "rb")
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
    photo = open("./resources/ayuda.png", "rb")
    # The buttones
    buttons = [[("Volver inicio", "cmd_start")]]

    return text, photo, buttons, HTML_FORMAT

def PRODUCT_LIST_HEADER_VIEW():
    # The text
    text = negrita_html(subrayado_html("Lista de productos:"))+"\n"+BARRA_SEPARADORA
    # The photo
    photo = open("./resources/lista.png", "rb")
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
    # The buttones
    buttons = None

    return text, photo, buttons, HTML_FORMAT

def ADD_PRODUCT_VIEW():
    # The text
    text = "Introduce el URL del producto que quieres comprobar"
    # The photo
    photo = open("./resources/enlace.png", "rb")
    # The buttones
    buttons = [[("Volver inicio", "cmd_start")]]

    return text, photo, buttons, HTML_FORMAT
