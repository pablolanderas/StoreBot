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

    def __eq__(self, value: object) -> bool:
        if type(value) != Deseado: return False
        if len(self.tags) != len(value.tags): return False
        for i in range(len(self.tags)):
            if self.tags[i] != value.tags[i]: return False
        return True

    def __str__(self) -> str:
        if self.mensaje is None: em = "✖"
        else: em = "✔"
        return f"[Deseado|Notificado:{em}|Tags:{self.tags}]"
    
    def __repr__(self) -> str:
        return str(self)