CREATE TABLE IF NOT EXISTS user (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
);
INSERT OR IGNORE INTO user (username, password) VALUES ('admin', 'admin');

CREATE TABLE IF NOT EXISTS voos (
    id INTEGER PRIMARY KEY,
    ano INTEGER NOT NULL,
    mes INTEGER NOT NULL,
    mercado TEXT NOT NULL,
    rpk FLOAT
);