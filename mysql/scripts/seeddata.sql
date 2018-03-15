-- -------------------------------------------- --
-- create FlaskApp DB objects
-- ./bin/mysql_connect.sh < ./scripts/seeddata.sql
--
-- INSERT handled automatically when first lauching MySQL/Docker container
--   using this file, copied to /docker-entrypoint-initdb.d/.
-- -------------------------------------------- --

USE `flaskapp`;

DELETE FROM `user`;
INSERT INTO `user` (keyname) VALUES ("admin");
OPTIMIZE TABLE `user`;

DELETE FROM `item`;
INSERT INTO `item` (keyname,item_title,item_text) VALUES ("one","One","One here");
INSERT INTO `item` (keyname,item_title,item_text) VALUES ("two","Two","Two here");
INSERT INTO `item` (keyname,item_title,item_text) VALUES ("three","Three","Three here");
INSERT INTO `item` (keyname,item_title,item_text) VALUES ("four","Four","Four here");
INSERT INTO `item` (keyname,item_title,item_text) VALUES ("five","Five","Five here");
INSERT INTO `item` (keyname,item_title,item_text) VALUES ("six","Six","Six here");
OPTIMIZE TABLE `item`;
