


def delUsed(options: dict, tags: list[list[str]]) -> list[list[str]]:
    def recursivo(obj:dict):
        for k, v in list(obj.items()):
            if type(v) == dict:
                recursivo(v)
            if not v: del obj[k]

    for tag in tags:
        c = options
        for k in tag[:-1]:
            c = c[k]
        del c[tag[-1]]
        
    recursivo(options)
    return options


if __name__ == "__main__":
    marino, negro, gris = ("Marino", "Negro", "Gris antracita")
    a, b, c, d = ("a", "b", "c", "d")
    options = {marino: {a:True, b:True}, negro: {c:True}, gris:{d:{d:True}}}
    tags = [(marino, a), (marino, b), (gris, d, d), (negro, c)]
    from pprint import pprint
    pprint(delUsed(options, tags))