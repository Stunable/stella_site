osx_ip = $(shell /sbin/ifconfig en1| grep 'inet ' | cut -d" " -f2)

all:
	@echo "Nothing here"
start:
	(python manage.py runserver ${osx_ip}:7777)
sync:
	(python manage.py syncdb)
migrate:
	(python manage.py migrate)
reset-proj:
	(git pull)
	(mysql -uroot -e "drop database stella")
	(mysql -uroot -e "create database stella")
	(python manage.py syncdb)
	(sudo initctl stop stella)
	(sudo initctl start stella)
	(sudo /etc/init.d/nginx restart)
reset-proj-local:
	(git pull)
	(mysql -uroot -e "drop database stella")
	(mysql -uroot -e "create database stella")
	(python manage.py syncdb)
