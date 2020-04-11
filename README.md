# brew_auth_service
microbrewery authentication microservice

Uses Django JWT framework to generate authentication tokens which are used in API requests for other microbrewery microservices.

## Use Standalone:
1. Nagivate in /app folder
2. pip install -r requirements.txt
3. python manage.py migrate
4. python manage.py makemigrations
5. python manage.py runserver

## Execute tests
1. Nagivate in /app folder
2. python manage.py test

