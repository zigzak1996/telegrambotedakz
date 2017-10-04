BEGIN TRANSACTION;
CREATE TABLE `subkitchen` (
	`id`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	`name`	TEXT NOT NULL,
	`kitchen_id`	INTEGER NOT NULL
);
INSERT INTO `subkitchen` VALUES (1,'Сеты',1),
 (2,'Роллы',1),
 (3,'Гуканы',1),
 (4,'Супы',1);
CREATE TABLE `kitchen` (
	`id`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	`name`	TEXT NOT NULL
);
INSERT INTO `kitchen` VALUES (1,'Японская кухня'),
 (2,'Европейская кухня '),
 (3,'Пицца '),
 (4,'Донер');
CREATE TABLE "eda" (
	`id`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	`name`	TEXT NOT NULL,
	`subkitchen_id`	INTEGER NOT NULL,
	`price`	INTEGER NOT NULL,
	`description`	TEXT NOT NULL,
	`image`	TEXT NOT NULL
);
INSERT INTO `eda` VALUES (1,'1 сет',1,2000,'не дорого','1.jpg'),
 (2,'2 сет',1,3000,'средне','2.jpg'),
 (3,'3 сет',1,4000,'дорого','3.jpg');
COMMIT;
