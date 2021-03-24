# An url shortening service

## Description

To shorten a given url I used hashids to create a unique hash for each url. It's done by hashing the id of an url object.

Everything is done in the "urlshortener" django app.

## Requirements:
* Python 3.9.2 or higher
* Python packages listed below:
  * asgiref==3.3.1
  * Django==3.1.7
  * django-ipware==3.0.2
  * hashids==1.3.1
  * pytz==2021.1
  * sqlparse==0.4.1

## To run the service use

In the main folder:

	python manage.py runserver