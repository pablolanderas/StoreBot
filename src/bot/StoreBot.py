from telebot.handler_backends import HandlerBackend
from telebot.storage import StateMemoryStorage, StateStorageBase
from dominio.Mensaje import Mensaje
from dominio.Gestor import Gestor
from dominio.Usuario import Usuario
from dominio.Peticion import Peticion
from bot.botFunctions import generateButtons, negrita_html, HTML_FORMAT, START_VIEW, HELP_VIEW, PRODUCT_LIST_HEADER_VIEW, PRODUCT_LIST_FOOTER_VIEW, REQUEST_VIEW, ADD_PRODUCT_VIEW

from telebot import ExceptionHandler, TeleBot
from telebot.types import BotCommand


class StoreBot(TeleBot):
    
    __copiedMessages : list[Mensaje]
    manager : Gestor

    def __init__(self, token: str, gestor: Gestor, parse_mode: str | None = None, threaded: bool | None = True, skip_pending: bool | None = False, num_threads: int | None = 2, next_step_backend: HandlerBackend | None = None, reply_backend: HandlerBackend | None = None, exception_handler: ExceptionHandler | None = None, last_update_id: int | None = 0, suppress_middleware_excepions: bool | None = False, state_storage: StateStorageBase | None = ..., use_class_middlewares: bool | None = False, disable_web_page_preview: bool | None = None, disable_notification: bool | None = None, protect_content: bool | None = None, allow_sending_without_reply: bool | None = None, colorful_logs: bool | None = False):
        super().__init__(token, parse_mode, threaded, skip_pending, num_threads, next_step_backend, reply_backend, exception_handler, last_update_id, suppress_middleware_excepions, state_storage, use_class_middlewares, disable_web_page_preview, disable_notification, protect_content, allow_sending_without_reply, colorful_logs)
        # Inicialize the manager
        self.manager = gestor
        # TODO: Choose the manager call functions
        # Inicialize the commands
        self.inicializeCommands()
        self.set_my_commands((BotCommand("start", "Comienza el bot"),))
        # Inicialize variables
        self.__copiedMessages = []

    def inicializeCommands(self) -> None:
        @self.message_handler(func=lambda message: True and not message.text.startswith('/start'))
        def start_caller(message): 
            user, message = self.getUserAndMessageFromBotsMessageType(message, True)
            self.messageReciber(user, message)
        @self.message_handler(commands=["start"])
        def start_caller(message): 
            user, _ = self.getUserAndMessageFromBotsMessageType(message, True)
            self.buttonsControler(user, "cmd_start")
        # Manejador de CallbackQuery
        @self.callback_query_handler(func=lambda call: True)
        def callback_query_handler(call):
            user, _ = self.getUserAndMessageFromBotsMessageType(call.message, False)
            self.buttonsControler(user, call.data)

    def buttonsControler(self, user: Usuario, data: str):
        match data:
            case "cmd_start":
                self.cmd_start(user)
            case "cmd_help":
                self.cmd_help(user)
            case "cmd_products_list":
                self.cmd_product_list(user)
            case "cmd_add_product":
                self.cmd_add_product(user)
            # add_product cases
            case "add_product save":
                self.manager.saveTemporalRequest(user)
                user.anhadiendoProducto = False
                user.temporal = None
                self.cmd_add_product(user, notice="El producto se ha guardado correctamente")
            case _:
                print("COMANDO RARO:", data)

    def messageReciber(self, user: Usuario, message: Mensaje):
        # Exit in case of bad window
        if not user.anhadiendoProducto or user.temporal is not None: return
        # Start the product
        answer = self.manager.startProduct(user, message.text)
        match answer:
            case -1:
                self.sendMessage(user, "La página que estas intentando añadir aun no esta disponible\nIntentelo con otra página")
            case -2:
                self.sendMessage(user, "El producto que estas intentando añadir no es correcto o no existe")
            case 0:
                self.showAddingRequest(user)

    def cmd_start(self, user:Usuario):
        self.copyUsersMessagesToDelete(user)
        # Inicializate the user state
        user.anhadiendoProducto = False
        user.temporal = None
        # Send the message
        text, photo, buttons, parseMode = START_VIEW()
        self.sendMessage(user, text, buttons, parseMode, photo=photo)
        # Delete the las messages
        self.deleteCopiedMessages()

    def cmd_help(self, user:Usuario):
        self.copyUsersMessagesToDelete(user)
        # Inicializate the user state
        user.anhadiendoProducto = False
        user.temporal = None
        # Send the message
        text, photo, buttons, parseMode = HELP_VIEW()
        self.sendMessage(user, text, buttons, parseMode, photo=photo)
        # Delete the las messages
        self.deleteCopiedMessages()

    def cmd_product_list(self, user:Usuario):
        self.copyUsersMessagesToDelete(user)
        # Inicializate the user state
        user.anhadiendoProducto = False
        user.temporal = None
        # Send the header
        text, photo, buttons, parseMode = PRODUCT_LIST_HEADER_VIEW()
        self.sendMessage(user, text, buttons, parseMode, photo=photo)
        # Show the products
        if not user.peticiones: # No requests
            text = negrita_html("No tienes peticiones guardadas")
            self.sendMessage(user, text, parseMode=HTML_FORMAT)
        else: # Case requests
            for request in user.peticiones.values():
                self.showRequest(request, [[("Eliminar", f"cmd_product_list remove {request.idPeticion}")]])
        # Show the footer
        text, photo, buttons, parseMode = PRODUCT_LIST_FOOTER_VIEW()
        self.sendMessage(user, text, buttons, parseMode, photo=photo)
        # Delete the las messages
        self.deleteCopiedMessages()

    def cmd_add_product(self, user:Usuario, notice: str=None):
        self.copyUsersMessagesToDelete(user)
        # Inicializate the user state
        user.anhadiendoProducto = True
        user.temporal = None
        # Send the notice
        if notice != None:
            self.sendMessage(user, notice)
        # Send the message
        text, photo, buttons, parseMode = ADD_PRODUCT_VIEW()
        self.sendMessage(user, text, buttons, parseMode, photo=photo)
        # Delete the las messages
        self.deleteCopiedMessages()

    def deleteMessage(self, message: Mensaje):
        self.delete_message(message.chatId, message.messageId)

    def sendMessage(self, user:Usuario, text:str, buttons=None, 
                    parseMode="html", saveMessage=True, photo:bytes=None) -> Mensaje:
        if buttons is None: buttons = []
        markup = generateButtons(buttons)
        if photo is None:
            message = self.send_message(user.chatId, text, parse_mode=parseMode, reply_markup=markup)
        else:
            message = self.send_photo(user.chatId, photo, text, parse_mode=parseMode, reply_markup=markup)
        message = Mensaje(message)
        if saveMessage: self.manager.saveMessage(message)
        return message

    def getUserAndMessageFromBotsMessageType(self, message, removeMessage: bool) -> Usuario:
        # Get the correct message type
        message = Mensaje(message)
        # Remove the message
        if removeMessage: 
            self.deleteMessage(message)
        user = self.manager.getUserFromMessage(message)
        return user, message

    def copyUsersMessagesToDelete(self, user: Usuario):
        messages = self.manager.deleteUsersMessages(user)
        self.__copiedMessages.extend(messages)

    def deleteCopiedMessages(self):
        for message in self.__copiedMessages:
            self.deleteMessage(message)
        self.__copiedMessages.clear()

    def showRequest(self, request:Peticion, buttons=None):
        text, photo, _, parseMode = REQUEST_VIEW(request)
        self.sendMessage(request.usuario, text, buttons, parseMode, photo=photo)

    def showAddingRequest(self, user: Usuario):
        self.copyUsersMessagesToDelete(user)
        # Show the request
        buttons = [
            [("Añadir avisos", "add_product addTags")],
            [("Guardar", "add_product save"), ("Cancelar", "cmd_start")]
        ]
        self.showRequest(user.temporal, buttons)
        # Delete the copied messgaes
        self.deleteCopiedMessages()
