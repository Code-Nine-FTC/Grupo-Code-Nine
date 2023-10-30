CREATE DATABASE IF NOT EXISTS cianp;
USE cianp;

CREATE TABLE IF NOT EXISTS usuario(
username VARCHAR(30) NOT NULL,
email VARCHAR(100) NOT NULL PRIMARY KEY UNIQUE,
cpf CHAR(11) NOT NULL UNIQUE,
prof VARCHAR(50),
data_nasc DATE NOT NULL,
parentesco VARCHAR(50) NOT NULL,
senha CHAR(16) NOT NULL
);

CREATE TABLE IF NOT EXISTS posts(
id INT AUTO_INCREMENT PRIMARY KEY,
user_email VARCHAR(100) NOT NULL,
user_name VARCHAR (30) NOT NULL,
content VARCHAR(1500) NOT NULL,
imagens INT DEFAULT 0,
 FOREIGN KEY (user_email) REFERENCES usuario(email),
 user_name REFERENCES usuario(username)
);

CREATE TABLE IF NOT EXISTS comentarios(
id INT AUTO_INCREMENT PRIMARY KEY,
post_id INT NOT NULL,
user_email VARCHAR(100) NOT NULL,
user_name VARCHAR (30) NOT NULL,
content VARCHAR(300) NOT NULL,
FOREIGN KEY (post_id) REFERENCES posts(id),
FOREIGN KEY (user_email) REFERENCES usuario(email),
user_name REFERENCES usuario(username)
);

CREATE TABLE IF NOT EXISTS perguntas(
id int AUTO_INCREMENT PRIMARY KEY,
autor_email VARCHAR(100) NOT NULL,
user_name VARCHAR (30) NOT NULL,
texto VARCHAR(300) NOT NULL,
FOREIGN KEY (autor_email) REFERENCES usuario(email),
user_name REFERENCES usuario(username)
);

CREATE TABLE IF NOT EXISTS respostas_perguntas(
id INT AUTO_INCREMENT PRIMARY KEY,
id_perguntas INT NOT NULL,
autor_email VARCHAR(100) NOT NULL,
user_name VARCHAR (30) NOT NULL,
texto VARCHAR(300) NOT NULL,
FOREIGN KEY (id_perguntas) REFERENCES perguntas(id),
FOREIGN KEY (autor_email) REFERENCES usuario(email),
user_name REFERENCES usuario(username)
);