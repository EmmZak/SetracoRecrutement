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
django-admin startapp profileFile
django-admin startapp skills
django-admin startapp profiles
```

# Run

If new model added etc

```bash
python3 manage.py makemigrations
python3 manage.py migrate
```

```bash
python3 manage.py runserver
```

# Create super user

```bash
python3 manage.py createsuperuser --username admin --email admin@admin.com
# password: admin
```
