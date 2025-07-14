# Ceragon

## Requirements

-   Python >= 3.8
-   Pipenv
-   PostgreSQL >= 16
-   Docker & Docker Compose

## Docker Deployment

1.  **Create Environment File**

    In the project root directory, create a `.env` file. **Crucially, set `DB_HOST` to `db`**, which is the service name defined in `docker-compose.yml`.

    ```
    DEBUG=True
    SECRET_KEY=supersecretkey
    ALLOWED_HOSTS=*
    DB_USER=ceragon
    DB_PASSWORD=superstrongpassword
    DB_NAME=ceragon
    DB_HOST=db
    DB_PORT=5432
    ```

2.  **Make Scripts Executable**

    Ensure the deployment and entrypoint scripts are executable:

    ```bash
    chmod +x deploy.sh
    chmod +x entrypoint.sh
    ```

3.  **Run the Deployment Script**

    This script will build the Docker images and start the application and database containers.

    ```bash
    deploy.sh
    ```

    The application will be available at `http://localhost:8000`. The database will be running on `localhost:5432`.

    This will automatically create a superuser with the following credentials:

    -   **Username**: `admin`
    -   **Password**: `Challenge.1`

### Common Docker Commands

-   **View logs:** `docker-compose logs -f`
-   **Stop services:** `docker-compose down`
-   **Stop and remove volumes (deletes DB data):** `docker-compose down -v`
-   **Run a one-off command (e.g., shell):** `docker-compose exec web python manage.py shell`

---

## Development Environment

1.  **Create Database**

    ```bash
    psql -U postgres -c "CREATE USER ceragon WITH ENCRYPTED PASSWORD 'superstrongpassword' CREATEDB;"
    psql -U postgres -c "CREATE DATABASE ceragon OWNER ceragon;"
    ```

2.  **Create Environment File**

    In the project root, create a `.env` file. Use `127.0.0.1` or `localhost` for `DB_HOST`.

    ```
    DEBUG=True
    SECRET_KEY=supersecretkey
    ALLOWED_HOSTS=*
    DB_USER=ceragon
    DB_PASSWORD=superstrongpassword
    DB_NAME=ceragon
    DB_HOST=127.0.0.1
    DB_PORT=5432
    ```

3.  **Install Dependencies**

    ```bash
    pipenv install
    ```

4.  **Apply Migrations and Initialize**

    ```bash
    pipenv run python manage.py migrate
    pipenv run python manage.py initialize
    ```

    This will automatically create a superuser with the following credentials:

    -   **Username**: `admin`
    -   **Password**: `Challenge.1`

5.  **Start Development Server**

    ```bash
    pipenv run python manage.py runserver
    ```
