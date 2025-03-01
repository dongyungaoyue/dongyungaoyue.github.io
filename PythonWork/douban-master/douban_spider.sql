DROP TABLE IF EXISTS `comments_new`;

CREATE TABLE `comments_new` (
  `username` varchar(100) CHARACTER SET utf8mb4 DEFAULT NULL,
  `title` varchar(100) CHARACTER SET utf8mb4 DEFAULT NULL,
  `date` varchar(50) DEFAULT NULL,
  `score` varchar(50) DEFAULT NULL,
  `comment` varchar(1024) CHARACTER SET utf8mb4 DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
LOCK TABLES `comments_new` WRITE;
UNLOCK TABLES;

USE douban;
SHOW TABLES;
SELECT * FROM comments_new LIMIT 10;

