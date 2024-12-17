
# Django Project - Curricular Analyst

This is a Django-based project for managing and analyzing curricular data. It includes functionality for managing courses, objectives, requirements, and relationships between them.

## Prerequisites

Before running the project, make sure you have the following installed:

- Python 3.x
- Django
- django-environ (for managing environment variables)

To install the necessary dependencies, run:

```bash
pip install django django-environ
```

## Setup

1. **Clone the repository**:

   If you haven't already, clone the repository:

   ```bash
   git clone <repository_url>
   ```

2. **Create the `.env` file**:

   In the root directory of the project, create a `.env` file to store your environment variables. Here is an example of how your `.env` file should look:

   ```ini
   DB_NAME=database_name
   DATABASE_NAME=database_name
   DB_USER=user
   DB_PASSWORD=your_password
   DB_HOST=localhost
   DB_PORT=5432
   SECRET_KEY=your_secret_key
   DEBUG=True
   ALLOWED_HOSTS=127.0.0.1,localhost
   ```

   Replace the `SECRET_KEY` with a strong secret key for your application. You can generate one using:

   ```python
   from django.core.management.utils import get_random_secret_key
   print(get_random_secret_key())
   ```

3. **Run Database Migrations**:

   After setting up your `.env` file, run the following commands to set up the database:

   ```bash
   python manage.py makemigrations course_management
   python manage.py migrate
   ```

4. **Create a Superuser**:

   To be able to access the Django admin interface, create a superuser by running:

   ```bash
   python manage.py createsuperuser
   ```

   You will be prompted to enter a username, email, and password for the superuser.

5. **Run the Development Server**:

   Finally, start the Django development server:

   ```bash
   python manage.py runserver
   ```

   Your application will be accessible at `http://127.0.0.1:8000`.

## Usage

Once the server is running, you can access the predefined queries and manage the course data via the Django admin interface.

### Admin Panel

You can log into the Django admin panel at:

```
http://127.0.0.1:8000/admin
```

Use the superuser credentials you created earlier.

## Notes

- Make sure your `.env` file is not uploaded to any version control system like Git. Add `.env` to your `.gitignore` to keep it private.
- If you need to install additional dependencies, you can add them to `requirements.txt` by running:

  ```bash
  pip freeze > requirements.txt
  ```
