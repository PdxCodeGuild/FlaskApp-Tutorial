-- -------------------------------------------- --
-- create FlaskApp DB objects
-- ./bin/mysql_connect.sh < ./scripts/seeddata.sql
--
-- INSERT handled automatically when first lauching MySQL/Docker container
--   using this file, copied to /docker-entrypoint-initdb.d/.
-- -------------------------------------------- --

USE `flaskapp`;

DELETE FROM `item`;
INSERT INTO `item` (keyname) VALUES ("one");
INSERT INTO `item` (keyname) VALUES ("two");
INSERT INTO `item` (keyname) VALUES ("three");
OPTIMIZE TABLE `item`;
