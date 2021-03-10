# Description
## Project: Foodgram "Food Assistant"
## The project was completed as a diploma assignment for the Python-developer Yandex.Practicum.
This is an online service where users can publish recipes, subscribe to the publication of other users, add recipes 
they like to the favorites list, comment on recipes from other authors, and before going to the store download a 
txt summary of the products required to prepare one or more selected dishes.
The installation will launch three containers: the first is foodgram + gunicorn, the second is the PostgreSQL database, 
and the third is the NGINX web server configured at http: // localhost.
An example of the service can be viewed at http://130.193.34.188/

# Run
## To install on a local computer, you must:
* Install Docker and Docker-Compose (only for linux)
* Download project files from the repository or clone it: https://github.com/nNDVG/foodgram-project.git
#### Enter the following command:
    docker exec -it foodgram_web_1 bash
    apt update
    apt install nano 
####You need to create an .env file in which to specify environment variables (for example): 
  - DB_NAME = postgres
  - DB_USER = postgres
  - DB_PASSWORD = postgres
  - DB_HOST = db
  - DB_PORT = 5432
####To do this, enter the following command and enter the appropriate data (the ones above):
    nano .env 
####In the <project_name>/foodgram/ project directory, enter the command:
    docker-compose up -d

## Command block for migrating and loading fixtures. 
#### To fill the database with recipes and tags, enter the following command:
     docker-compose exec foodgram_web_1 /bin/sh builddatabase.sh

#### To perform only migrations, run the command:
     docker-compose exec foodgram_web_1 /bin/sh migrate.sh
  
#### To create a superuser system, run the command:
     docker-compose exec foodgram_web_1 python manage.py creates superuser
  
# Tests
(Real tests are not available at the moment.)  
* Enter the command:
    docker-compose exec foodgram_web_1 flake8 --max-line-length=119 --exclude=tests,migrations,venv .


# Author
 - https://github.com/nNDVG/
 - https://hub.docker.com/u/ndvg/

# Tech stack:
* Python
* Django
* Django REST
* PostgreSQL
* Gunicorn
* Nginx
* Docker
* SendGrid  
* GitHub actions
* HTML / CSS / Javascript was developed by the web faculty of Yandex.Praktikum (thanks for that). 
