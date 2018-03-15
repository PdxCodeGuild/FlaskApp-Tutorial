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
    `active`        tinyint(1)      NOT NULL DEFAULT '1',
    `item_title`    varchar(255)    DEFAULT NULL,
    `item_text`     text,
    `mod_create`    datetime        DEFAULT CURRENT_TIMESTAMP,
    `mod_update`    datetime        DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    PRIMARY KEY (`id`),
    UNIQUE KEY `item_keyname` (`keyname`),
    KEY `item_active` (`active`),
    KEY `item_title` (`item_title`),
    KEY `item_update` (`mod_update`)
) ENGINE=InnoDB AUTO_INCREMENT=1000 DEFAULT CHARSET=utf8;
DESCRIBE `item`;
SELECT "table `item` created" AS MSG;


-- -------------------------------------------- --
-- user
-- -------------------------------------------- --
DROP TABLE IF EXISTS `user`;
CREATE TABLE `user` (
    `id`            bigint(20)      NOT NULL AUTO_INCREMENT,
    `keyname`       varchar(63)     NOT NULL,
    `active`        tinyint(1)      NOT NULL DEFAULT '1',

    PRIMARY KEY (`id`),
    UNIQUE KEY `user_keyname` (`keyname`),
    KEY `user_active` (`active`)
) ENGINE=InnoDB AUTO_INCREMENT=1000 DEFAULT CHARSET=utf8;
DESCRIBE `user`;
SELECT "table `user` created" AS MSG;
