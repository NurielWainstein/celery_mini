CREATE TABLE IF NOT EXISTS categories (
    name TEXT PRIMARY KEY,
    region TEXT NOT NULL,
    type TEXT NOT NULL,
    count INTEGER NOT NULL
);
