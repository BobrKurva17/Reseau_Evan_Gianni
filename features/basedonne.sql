create table if not exist user(
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) NOT NULL,
    pswd VARCHAR(255) NOT NULL,
    codeSecret int
)engine=InnoDB;