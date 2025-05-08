$ docker run --rm -d --name mysqlcont -p 3306:3306 \
-v mysql_data /var/lib/mysql \
-e MYSQL_ROOT_PASSWORD=Vamsi@12345 \
-e MYSQL_DATABASE=myflixdb \
-e MYSQL_PASSWORD=Vamsi@12345 \
mysql:latest
