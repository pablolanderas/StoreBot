
class Mensaje:

    messageId : int
    chatId : int
    text : str
    username : str
    
    def __init__(self, message, text=None, chatId=None, username=None, messageId=None) -> None:
        if message is not None:
            self.text = message.text
            self.chatId = message.chat.id
            if message.from_user:
                self.username = message.from_user.username
            else:
                self.username = None
            self.messageId = message.id
        else:
            self.text = text
            self.chatId = chatId
            self.username = username
            self.messageId = messageId

    def __str__(self) -> str:
        return f"Mensaje[@{self.username}:{self.messageId}]:{self.text}"
    
    def __repr__(self) -> str:
        return self.__str__()