## settings

by default prod settings inside settings.py

if need to overrite use those in /__settings/

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

```bash
export DJANGO_SETTINGS_MODULE=SetracoRecrutement.settings.local
export DJANGO_SECRET_KEY="local"
python3 manage.py runserver
```

If new model added etc

```bash
python3 manage.py makemigrations
python3 manage.py migrate

python3 manage.py migrate accounts 0001_initial --fake
python3 manage.py makemigrations accounts --empty 

python3 manage.py init_group_permissions_after_migration
python3 manage.py create_test_users 

find . -not -path "./.venv/*" -path "*/migrations/*.py" ! -name "__init__.py" -delete

python3 manage.py dbshell
```

## Data integrity

### backup
```bash
python3 manage.py backup 
```

### restore
```bash
python3 manage.py migrate 
python3 manage.py restore /Users/emmanuelzakaryan/Projects/SetracoRecrutement/backups/backup_27_09_2024.zip
```



# Create super user

```bash
python3 manage.py createsuperuser --username admin
python3 manage.py changepassword admin  # azertyA1
# password: admin
```
