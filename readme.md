## files

store all files woth profile, 

update => 

1 list for files view, and another section for the input for what i upload, 

every upload => append

# Versions

```bash
python3 -v # 3.11
python3 -m django --version # 4.2.6

vue # 3.4
vuetify # 3.7
```

# Init

```bash
django-admin startproject SetracoRecrutement
python3 manage.py migrate
```

# Create app

```bash
django-admin startapp skills
django-admin startapp profiles
django-admin startapp accounts
django-admin startapp config
```

# Run

If new model added etc

```bash
python3 manage.py makemigrations
python3 manage.py migrate

python3 manage.py migrate accounts 0001_initial --fake
python3 manage.py makemigrations accounts --empty 

find . -not -path "./.venv/*" -path "*/migrations/*.py" ! -name "__init__.py" -delete

python3 manage.py dbshell
```

```bash
python3 manage.py runserver
```

# Create super user

```bash
python3 manage.py createsuperuser --username admin
# password: admin
```
