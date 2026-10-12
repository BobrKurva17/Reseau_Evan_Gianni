drop database Ippy_DB;
create database if not exists Ippy_DB;
use Ippy_DB;

create table if not exists user(
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) NOT NULL,
    roles VARCHAR(255) NOT NULL,
    pswd VARCHAR(255) NOT NULL,
    isActive BOOLEAN default true,
    codeSecret VARCHAR(255)
)engine=InnoDB;

create table if not exists alert(
    id INT AUTO_INCREMENT PRIMARY KEY,
    nbAlert INT default 0,
    idUser1 INT,
    idUser2 INT,
    FOREIGN KEY (idUser1) REFERENCES user(id),
    FOREIGN KEY (idUser2) REFERENCES user(id)
)engine=InnoDB;

create table if not exists historicUser(

)engine=InnoDB;

create table if not exists historicFunction(

)engine=InnoDB;

create table if not exists subnetting(

)engine =InnoDB;