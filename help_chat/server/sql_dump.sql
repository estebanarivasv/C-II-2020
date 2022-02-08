create table operators
(
    id         int auto_increment
        primary key,
    username   varchar(50) null,
    password   varchar(50) null,
    name       varchar(50) null,
    department varchar(50) null
);

INSERT INTO authorized_operators.operators (id, username, password, name, department) VALUES (1, 'monica.sanchez', '123456', 'Mónica Sanchez', 'technical');
INSERT INTO authorized_operators.operators (id, username, password, name, department) VALUES (2, 'eduardo.gomez', '123456', 'Eduardo Gómez', 'administrative');
INSERT INTO authorized_operators.operators (id, username, password, name, department) VALUES (3, 'estela.moreno', '123456', 'Estela Moreno', 'sales');
