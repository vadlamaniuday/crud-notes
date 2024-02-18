CRUD Notes App built with Django and Django Rest Framework. It provides endpoints for user registration, authentication, and note management. 

To install and run this project, follow these steps:

1. Clone the repository:

```bash
git clone https://github.com/vadlamaniuday/crud-notes.git
```

2. Navigate to the project directory:

```bash
cd crud-notes
```

3. Create a new virtual environment (recommended):

```bash
python3 -m venv env
```

4. Activate the virtual environment (on Unix/MacOS):

```bash
source env/bin/activate
```

5. Install the required dependencies:

```bash
pip install -r requirements.txt
```

6. Set up the database (create a new database and migrate):

```bash
python manage.py migrate
```

7. Create a superuser (for the admin interface):

```bash
python manage.py createsuperuser
```

8. Run the development server:

```bash
python manage.py runserver
```

The requirements are to be downloaded from requirements.txt files


Sources : 
1. Django Docs : https://docs.djangoproject.com/en/4.2/
2. DjangoRESTFramework : https://www.django-rest-framework.org/
