# Student Grading App

### use `docker compose up -d` to start the app in detached mode.

#### usage -

> `docker compose run --rm web sh -c "python manage.py createsuperuser"` to create a superuser and access the admin site.

> `docker compose run --rm web sh -c "python manage.py populate_db"` to populate the database with dummy data (optional).

> `docker compose run --rm web sh -c "python manage.py test"` to run tests.

#### Not configured for production.
