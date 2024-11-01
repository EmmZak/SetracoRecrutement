# Developpement

## Logs, Backups, Media files

In dev mode, all those dirs are inside root dir

## Database

on model change
```bash
python3 manage.py makemigrations --settings SetracoRecrutement.settings.local 
```
migrate
```bash
python3 manage.py migrate --settings SetracoRecrutement.settings.local
```
### Create super user

```bash
python3 manage.py createsuperuser --username admin
python3 manage.py changepassword admin  # azertyA1
# password: admin
```


## Run locally
```bash
python3 manage.py runserver --settings SetracoRecrutement.settings.local
```
# Production

## Setup
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt 
```
## Logs, Backups, Media files

create dirs
```bash
mkdir logs
mkdir media
mkdir backups
```
change permissions

## Database
```bash
python manage.py migrate  --settings SetracoRecrutement.settings.prod 
```
## Static content
```bash
python manage.py collectstatic --settings SetracoRecrutement.settings.prod 
```

## Django specific env vars
```bash
export DJANGO_SECRET_KEY=...
export DJANGO_SETTINGS_MODULE=SetracoRecrutement.settings.prod
```

## Run with Gunicorn
```bash
gunicorn --workers 4 --timeout 60 --bind 0.0.0.0:8000 SetracoRecrutement.wsgi > gunicorn.log 2>&1 & 
```

helpers
```bash
sudo lsof -i -P -n | grep LISTEN
ps ax|grep gunicorn 
pkill gunicorn
```

## Nginx
sudo nano /etc/nginx/sites-available/cvtheque 
    cat /etc/nginx/sites-available/cvtheque
sudo service nginx restart

logs 
    cat /var/log/nginx/error.log

refs

Follow on vps  https://github.com/TheProtonGuy/server-configs 
	YouTube https://www.youtube.com/watch?v=RsrJzKPigc4 

## Crontab

### backup cmds
```bash
/home/ubuntu/SetracoRecrutement/venv/bin/python /home/ubuntu/SetracoRecrutement/manage.py dbbackup --settings SetracoRecrutement.settings.prod 
/home/ubuntu/SetracoRecrutement/venv/bin/python /home/ubuntu/SetracoRecrutement/manage.py mediabackup --settings SetracoRecrutement.settings.prod 
```

### crontab cmds
```bash
0 0 * * * /home/ubuntu/SetracoRecrutement/venv/bin/python /home/ubuntu/SetracoRecrutement/manage.py dbbackup --settings SetracoRecrutement.settings.prod >> /home/ubuntu/logs/backup.log 2>&1
0 0 * * * /home/ubuntu/SetracoRecrutement/venv/bin/python /home/ubuntu/SetracoRecrutement/manage.py mediabackup --settings SetracoRecrutement.settings.prod >> /home/ubuntu/logs/backup.log 2>&1
```

# Lib Versions

## v1 

```bash
python3 -v # 3.11
python3 -m django --version # 4.2.6

vue # 3.4
vuetify # 3.7
```


# Run


If new model added etc

```bash
python3 manage.py makemigrations
python3 manage.py migrate

python3 manage.py migrate accounts 0001_initial --fake
python3 manage.py makemigrations accounts --empty 

python3 manage.py init_group_permissions_after_migration
python3 manage.py create_test_users 

```





