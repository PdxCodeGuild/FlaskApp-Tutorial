-- -------------------------------------------- --
-- create FlaskApp DB objects
-- ./bin/mysql_connect.sh < ./scripts/tables.sql
--
-- CREATE handled automatically when first lauching MySQL/Docker container
--   using this file, copied to /docker-entrypoint-initdb.d/.
-- -------------------------------------------- --

USE `flaskapp`;

-- -------------------------------------------- --
-- item
-- -------------------------------------------- --
DROP TABLE IF EXISTS `item`;
CREATE TABLE `item` (
    `id`            bigint(20)      NOT NULL AUTO_INCREMENT,
    `keyname`       varchar(63)     NOT NULL,
    `mod_create`    datetime        DEFAULT CURRENT_TIMESTAMP,

    PRIMARY KEY (`id`),
    UNIQUE KEY `item_keyname` (`keyname`)
) ENGINE=InnoDB AUTO_INCREMENT=1000 DEFAULT CHARSET=utf8;
DESCRIBE `item`;
SELECT "table `item` created" AS MSG;

