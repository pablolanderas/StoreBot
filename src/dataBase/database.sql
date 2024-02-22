CREATE TABLE Productos (
    productId INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    url VARCHAR NOT NULL
);

CREATE TABLE Usuarios (
    chatId INTEGER NOT NULL PRIMARY KEY,
    username VARCHAR NOT NULL
);

CREATE TABLE TagName (
    tagId INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    nombre VARCHAR NOT NULL
);

CREATE TABLE Mensajes (
    messageId INTEGER NOT NULL PRIMARY KEY,
    chatId INTEGER NOT NULL,
    FOREIGN KEY (chatId) REFERENCES Usuarios(chatId)
);

CREATE TABLE Peticiones (
    requestId INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    usuarioId INTEGER NOT NULL,
    productId INTEGER NOT NULL,
    ultPrecio REAL NOT NULL CHECK (ultPrecio >= 0),
    FOREIGN KEY (usuarioId) REFERENCES Usuarios(chatId),
    FOREIGN KEY (productId) REFERENCES Productos(productId)
);

CREATE TABLE Deseado (
    deseadoId INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    requestId INTEGER NOT NULL,
    messageId INTEGER,
    tipoPrecio INTEGER NOT NULL CHECK (tipoPrecio in (0, 1)),
    FOREIGN KEY (requestId) REFERENCES Peticiones(requestId)
);

CREATE TABLE Tag (
    deseadoId INTEGER NOT NULL,
    posicion INTEGER NOT NULL,
    tagName INTEGER NOT NULL,
    PRIMARY KEY (deseadoId, posicion),
    FOREIGN KEY (deseadoId) REFERENCES Deseado(deseadoId),
    FOREIGN KEY (tagName) REFERENCES TagName(tagId)
);