CREATE TABLE IF NOT EXISTS users (
    id TEXT PRIMARY KEY NOT NULL,
    nome TEXT NOT NULL,
    id_lfm INT NULL,
    embedding FLOAT[50] NOT NULL
);

CREATE TABLE IF NOT EXISTS news (
    id TEXT PRIMARY KEY NOT NULL,
    titulo TEXT NOT NULL,
    subtitulo TEXT,
    corpo_noticia TEXT NOT NULL,
    url TEXT NOT NULL,
    data_publicacao TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
    id_lfm INT NULL,
    embedding FLOAT[50] NOT NULL
);

CREATE TABLE IF NOT EXISTS access (
    id serial PRIMARY KEY,
    id_user TEXT NULL,
    id_news TEXT NULL,
    data_acesso TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    engagement numeric NOT NULL,
    FOREIGN KEY (id_user) REFERENCES users(id),
    FOREIGN KEY (id_news) REFERENCES news(id)
);


