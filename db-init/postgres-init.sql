CREATE DATABASE products_db;
\c products_db;
CREATE TABLE products (id SERIAL PRIMARY KEY, name VARCHAR(50));
INSERT INTO products (name) VALUES ('Book'), ('Laptop');

