from dominio.Mensaje import Mensaje

class Deseado:

    idDeseado : int
    tags: list[str]
    mensaje : Mensaje
    peticion : None

    def __init__(self, idDeseado:int, mensaje:Mensaje, tags:list[str], peticion) -> None:
        self.idDeseado = idDeseado
        self.mensaje = mensaje
        self.tags = tags
        self.peticion = peticion

    def __str__(self) -> str:
        if self.mensaje is None: em = "✖"
        else: em = "✔"
        return f"[Deseado|Notificado:{em}|Tags:{self.tags}]"
    
    def __repr__(self) -> str:
        return str(self)