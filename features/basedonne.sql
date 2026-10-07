create database if not exists Ippy_DB;
use Ippy_DB;

create table if not exists user(
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) NOT NULL,
    roles VARCHAR(255) NOT NULL,
    pswd VARCHAR(255) NOT NULL,
    isActive boolean default true,
    codeSecret int
)engine=InnoDB;

create table if not exists historicUser(

)engine=InnoDB;

create table if not exists historicFunction(

)engine=InnoDB;

create table if not exists subnetting(

)engine =InnoDB;