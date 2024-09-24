from os import environ as varEntorno
from dotenv import load_dotenv

load_dotenv()

try:
    BOT_TOKEN = varEntorno['BOT_TOKEN']
    ID_CHAT_AVISOS = varEntorno['ID_CHAT_AVISOS']
    ID_CHAT_ERRORES = varEntorno['ID_CHAT_ERRORES']
    TESTING = varEntorno['TESTING'] in ('True', 'true', '1')
    CREATE_DB = varEntorno['CREATE_DB'] in ('True', 'true', '1')
except KeyError as e:
    print(f"[ERROR]: No se encontro la variable de entorno \"{e.args[0]}\"")
    exit(-1)
