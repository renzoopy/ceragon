# Ceragon

## Requirements

-   Python >= 3.8
-   Pipenv
-   PostgreSQL >= 16

## Development Environment

1. Create a database for the project:

    ```bash
    psql -U postgres -c "CREATE USER ceragon WITH ENCRYPTED PASSWORD 'superstrongpassword';"
    psql -U postgres -c "CREATE DATABASE ceragon OWNER ceragon;"
    ```

2. In the project root directory, create a `.env` file with the following content:

    ```
        DEBUG = True
        SECRET_KEY = supersecretkey
        ALLOWED_HOSTS = *
        DB_USER = ceragon
        DB_PASSWORD = superstrongpassword
        DB_NAME = ceragon
        DB_HOST = 127.0.0.1
        DB_PORT = 5432
    ```

3. Install project dependencies:

    ```bash
    pipenv install
    ```

4. Run the database migrations:

    ```bash
    pipenv run python manage.py migrate
    ```

5. Create a superuser:

    ```bash
    pipenv run python manage.py createsuperuser
    ```

6. Start the development server:

    ```bash
    pipenv run python manage.py runserver
    ```
