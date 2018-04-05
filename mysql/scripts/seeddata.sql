-- -------------------------------------------- --
-- create FlaskApp DB objects
-- ./bin/mysql_connect.sh < ./scripts/seeddata.sql
--
-- INSERT handled automatically when first lauching MySQL/Docker container
--   using this file, copied to /docker-entrypoint-initdb.d/.
-- -------------------------------------------- --

USE `flaskapp`;

DELETE FROM `user`;
INSERT INTO `user` (user_role,keyname,user_email) VALUES (3,"admin","admin@flaskapp.com");
INSERT INTO `user` (user_role,keyname,user_email) VALUES (2,"edit","user2@flaskapp.com");
INSERT INTO `user` (user_role,keyname,user_email) VALUES (1,"view","user1@flaskapp.com");
INSERT INTO `user` (user_role,keyname,user_email) VALUES (0,"none","user0@flaskapp.com");
OPTIMIZE TABLE `user`;

DELETE FROM `item`;
INSERT INTO `item` (keyname,item_title,item_text) VALUES ("one","One","One here");
INSERT INTO `item` (keyname,item_title,item_text) VALUES ("two","Two","Two here");
INSERT INTO `item` (keyname,item_title,item_text) VALUES ("three","Three","Three here");
INSERT INTO `item` (keyname,item_title,item_text) VALUES ("four","Four","Four here");
INSERT INTO `item` (keyname,item_title,item_text) VALUES ("five","Five","Five here");
INSERT INTO `item` (keyname,item_title,item_text) VALUES ("six","Six","Six here");
OPTIMIZE TABLE `item`;


DELETE FROM `item_user`;
insert into `item_user` (item_id,user_id) values (1000,1001);
insert into `item_user` (item_id,user_id) values (1000,1002);
OPTIMIZE TABLE `item_user`;
