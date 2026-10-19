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

CREATE TABLE IF NOT EXISTS subnet_division (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_user INT NOT NULL,
    subnet VARCHAR(15) NOT NULL,
    subnet_mask_classless TINYINT UNSIGNED NOT NULL,
    number_of_subnets INT UNSIGNED NOT NULL,

    CONSTRAINT fk_subnet_division_user
        FOREIGN KEY (id_user) REFERENCES user(id)
) ENGINE=InnoDB;


CREATE TABLE IF NOT EXISTS communication_btw_devices (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_user INT NOT NULL,
    ip_device_1 VARCHAR(15) NOT NULL,
    ip_device_2 VARCHAR(15) NOT NULL,
    mask_device_1 VARCHAR(15)  NOT NULL,
    mask_device_2 VARCHAR(15) NOT NULL,
    CONSTRAINT fk_communication_devices_user
    FOREIGN KEY (id_user) REFERENCES user(id)
) ENGINE=InnoDB;


create table if not exists historicFunction(

)engine=InnoDB;

create table if not exists subnetting(

)engine =InnoDB;





create table if not exists CIDRTable(
    cidr INT PRIMARY KEY,
    masque_binaire VARCHAR(35) NOT NULL,
    masque_decimal VARCHAR(15) NOT NULL
)engine=InnoDB; 

/*

VALEURS DE TEST  RAPPEL A NOUS SUPPRIMER QUAND PARTIE EVAN FINIE
INSERT INTO subnet_division
    (id_user, subnet, subnet_mask_classless, number_of_subnets)
VALUES
    (1, '192.168.1.0', 24, 4),
    (1, '192.168.10.0', 24, 8);


    INSERT INTO communication_btw_devices
    (id_user, ip_device_1, ip_device_2,
     mask_device_1, mask_device_2)
VALUES
    (1, '192.168.1.10', '192.168.1.20',
     '255.255.255.0', '255.255.255.0'),

    (1, '192.168.1.10', '192.168.2.20',
     '255.255.255.0', '255.255.255.0');
*/
/*
 REMPLIR LA TABLE CIDRTable AVEC : 
 INSERT INTO masques_cidr (cidr, masque_binaire, masque_decimal) VALUES
        (8,  '11111111.00000000.00000000.00000000', '255.0.0.0'),
        (9,  '11111111.10000000.00000000.00000000', '255.128.0.0'),
        (10, '11111111.11000000.00000000.00000000', '255.192.0.0'),
        (11, '11111111.11100000.00000000.00000000', '255.224.0.0'),
        (12, '11111111.11110000.00000000.00000000', '255.240.0.0'),
        (13, '11111111.11111000.00000000.00000000', '255.248.0.0'),
        (14, '11111111.11111100.00000000.00000000', '255.252.0.0'),
        (15, '11111111.11111110.00000000.00000000', '255.254.0.0'),
        (16, '11111111.11111111.00000000.00000000', '255.255.0.0'),
        (17, '11111111.11111111.10000000.00000000', '255.255.128.0'),
        (18, '11111111.11111111.11000000.00000000', '255.255.192.0'),
        (19, '11111111.11111111.11100000.00000000', '255.255.224.0'),
        (20, '11111111.11111111.11110000.00000000', '255.255.240.0'),
        (21, '11111111.11111111.11111000.00000000', '255.255.248.0'),
        (22, '11111111.11111111.11111100.00000000', '255.255.252.0'),
        (23, '11111111.11111111.11111110.00000000', '255.255.254.0'),
        (24, '11111111.11111111.11111111.00000000', '255.255.255.0'),
        (25, '11111111.11111111.11111111.10000000', '255.255.255.128'),
        (26, '11111111.11111111.11111111.11000000', '255.255.255.192'),
        (27, '11111111.11111111.11111111.11100000', '255.255.255.224'),
        (28, '11111111.11111111.11111111.11110000', '255.255.255.240'),
        (29, '11111111.11111111.11111111.11111000', '255.255.255.248'),
        (30, '11111111.11111111.11111111.11111100', '255.255.255.252')
*/