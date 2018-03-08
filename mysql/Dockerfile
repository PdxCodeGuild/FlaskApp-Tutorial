# base container image
FROM mysql:5.7

# Add SQL files to run on the container creation
ADD scripts/tables.sql   /docker-entrypoint-initdb.d/1-tables.sql
ADD scripts/seeddata.sql /docker-entrypoint-initdb.d/2-seeddata.sql
