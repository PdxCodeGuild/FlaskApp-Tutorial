#/bin/sh

# root-password
#docker exec -it flaskapp_db mysql -p -u root

# python-pass
docker exec -it flaskapp_db mysql -p -u python -D flaskapp

