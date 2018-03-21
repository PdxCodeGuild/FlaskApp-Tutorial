-- -------------------------------------------- --
-- create FlaskApp DB objects
-- ./bin/mysql_connect.sh < ./scripts/tables.sql
--
-- CREATE handled automatically when first lauching MySQL/Docker container
--   using this file, copied to /docker-entrypoint-initdb.d/.
-- -------------------------------------------- --

USE `flaskapp`;

-- -------------------------------------------- --
-- user
-- -------------------------------------------- --
DROP TABLE IF EXISTS `user`;
CREATE TABLE `user` (
    `id`            bigint(20)      NOT NULL AUTO_INCREMENT,
    `active`        tinyint(1)      NOT NULL DEFAULT '1',
    `keyname`       varchar(63)     NOT NULL,
    `user_email`    varchar(255)    DEFAULT NULL,
    `user_pass`     varchar(255) 	DEFAULT NULL,
    `cnt_login`     smallint(6)     DEFAULT '0',
    `mod_login`     datetime        DEFAULT NULL,
    `mod_create`    datetime        DEFAULT CURRENT_TIMESTAMP,
    `mod_update`    datetime        DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    PRIMARY KEY (`id`),
    UNIQUE KEY `user_keyname` (`keyname`),
    KEY `user_active` (`active`),
    KEY `user_email` (`user_email`),
    KEY `user_login` (`mod_login`),
    KEY `user_create` (`mod_create`)
) ENGINE=InnoDB AUTO_INCREMENT=1000 DEFAULT CHARSET=utf8;
DESCRIBE `user`;
SELECT "table `user` created" AS MSG;


-- -------------------------------------------- --
-- item
-- -------------------------------------------- --
DROP TABLE IF EXISTS `item`;
CREATE TABLE `item` (
    `id`            bigint(20)      NOT NULL AUTO_INCREMENT,
    `active`        tinyint(1)      NOT NULL DEFAULT '1',
    `keyname`       varchar(63)     NOT NULL,
    `item_title`    varchar(255)    DEFAULT NULL,
    `item_text`     text,
    `mod_create`    datetime        DEFAULT CURRENT_TIMESTAMP,
    `mod_update`    datetime        DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    `owner_id`      bigint(20)      NULL,

    PRIMARY KEY (`id`),
    UNIQUE KEY `item_keyname` (`keyname`),
    KEY `item_active` (`active`),
    KEY `item_title` (`item_title`),
    KEY `item_update` (`mod_update`),
    FOREIGN KEY (`owner_id`) REFERENCES user(`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1000 DEFAULT CHARSET=utf8;
DESCRIBE `item`;
SELECT "table `item` created" AS MSG;


