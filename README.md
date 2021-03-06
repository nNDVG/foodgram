Project: Foodgram "Food Assistant"
This is an online service where users can publish recipes, subscribe to the publication of other users, add recipes they like to the favorites list, comment on recipes from other authors, and before going to the store download a pdf summary of the products required to prepare one or more selected dishes.
Tech stack

    Python
    Django
    PostgreSQL
    Gunicorn
    Nginx
    Docker
    GitHub actions

The project was completed as a diploma assignment for the Python-developer Yandex.Practicum.
Installing on a local computer

To install on a local computer, you must:

    Install Docker
    Download project files from the repository or clone it: https://github.com/nNDVG/foodgram-project.git
    In the <project_name> / foodgram / project directory, create an .env file in which to specify environment variables (for example):

    DB_NAME = postgres
    DB_USER = postgres
    DB_PASSWORD = postgres
    DB_HOST = db
    DB_PORT = 5432
    SECRET_KEY = can be generated at

    To build and run containers, go to the <project_name> / foodgram / folder and run the command:
    docker-compose up -d --build

The installation will launch three containers: the first is foodgram + gunicorn, the second is the PostgreSQL database, and the third is the NGINX web server configured at http: // localhost.

To fill the database with recipes and tags, enter the following command:
     docker-compose exec web /bin/sh builddatabase.sh

To perform only migrations, run the command:
     docker-compose exec web /bin/sh migrate.sh
To create a superuser system, run the command:
docker-compose exec web python manage.py creates superuser

An example of the service can be viewed at https://130.193.34.55/
