-- Items
CREATE TABLE IF NOT EXISTS items_data (
    ID SERIAL PRIMARY KEY,
    Name VARCHAR NOT NULL,
    Description VARCHAR
);