1. This Repository is related to Backup Opeartions of Partitions.

RUNNING:-
1. pip install -r requirements/base.txt
2. python manage.py makemigrations --settings=Trillio_Files_Operations
3. python manage.py migrate --settings=Trillio_Files_Operations

SERVER UP:-
1. python manage.py runserver <ip>:<port> --settings=Trillio_Files_Operations

RUNNING PYTEST:-
1. pytest 

SWAGGER:-
1. http://<ip>:<port>/docs

