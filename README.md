# SW API GraphQL

## Requirements
* [Python](https://www.python.org/) (realizado en python 3.8)
* [Django](https://github.com/django/django)
* [Django Filter](https://github.com/carltongibson/django-filter)
* [Django model utils](https://github.com/jazzband/django-model-utils)
* [Graphene](https://github.com/graphql-python/graphene-django)
* [.EVN](https://github.com/theskumar/python-dotenv)

## Setup

Clone the project
```
git clone https://github.com//swapi.git
```

Move into de repo and install dependencies
```
pip install -r requirements.txt
```

Create a .env file with a secret key or [get one](https://djecrety.ir/) manually and set it in the settings.py
```
python -c 'from django.core.management.utils import get_random_secret_key; print("SECRET_KEY={}".format(get_random_secret_key()))' > swapi/.env
```


Run migrations and load fixtures
```
python manage.py migrate
python manage.py load_fixtures
```
Now the project is all set.

### Running the server
```
python manage.py runserver
```

### Runing the tests
```
python manage.py test
```

### Pruebas en servidor web

Esta es la ruta para acceder al servidor web desplegado
```
https://build-graphql.uw.r.appspot.com
```

La coleccion de servicios esta en la carpeta extra, es recomendable hacer las peticiones desde postman o parecidos

La parte uno del test se encuentra en la carpeta 'Parte1'
No se implemento Pytest y el dockerfile tuvo problemas con los paquetes, el resto de puntos fueron desarrollados