from dominio.Mensaje import Mensaje
from dominio.Peticion import Peticion


class Usuario:
    username : str
    chatId : int
    chatMessages : list[Mensaje]
    peticiones : dict[int:Peticion]
    anhadiendoProducto: bool
    temporal : None

    def __init__(self, username:str, chatId:int) -> None:
        self.username = username
        self.chatId = chatId
        self.chatMessages = []
        self.peticiones = {}
        self.anhadiendoProducto = False
        self.temporal = None

    def eliminaTodoMensaje(self) -> list[Mensaje]:
        copia = self.chatMessages.copy()
        self.chatMessages.clear()
        return copia
    
    def eliminaMensaje(self, index:int) -> Mensaje:
        return self.chatMessages.pop(index)
    
    def __eq__(self, __value: object) -> bool:
        return type(__value) == Usuario and __value.chatId == self.chatId
    
    def __hash__(self) -> int:
        return self.chatId
    
    def __str__(self) -> str:
        return f"Usuario[@{self.username}:{self.chatId}]"

    def __repr__(self) -> str:
        return self.__str__()