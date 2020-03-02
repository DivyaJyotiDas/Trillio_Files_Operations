**Project Title**

This Repository is related to Backup Opeartions of Partitions.

**Getting Started**

python manage.py makemigrations --settings=Trillio_Files_Operations
python manage.py migrate --settings=Trillio_Files_Operations

python manage.py runserver <ip>:<port> --settings=Trillio_Files_Operations


**Prerequisites**

pip install -r requirements/base.txt

**Installing**

_requirements_ directory contains all the files necessary for install.

_models_ directory contains all the DB related schema.

_settings_ directory contains all the settings that were used for tests/dev/prod environment.


**Running the tests**

pytest --cov=. --disable-warnings

**_Docs_**

http://<x.x.x.x>:<8080>/docs


**Deployment**

In Progress

**Contributing**

1. Divya Das<Divya.Das@afourtech.com>




