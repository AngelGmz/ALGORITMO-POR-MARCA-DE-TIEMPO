from asyncio.windows_events import NULL


class Mensaje():
    id_nodo = NULL
    msg = NULL
    def __init__(self, id_nodo, msg):
        self.id_nodo = id_nodo
        self.msg = msg
