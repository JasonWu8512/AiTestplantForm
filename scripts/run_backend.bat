@echo off
cd /d %~dp0
cd ..\backend
call ..\venv\Scripts\activate.bat
pip install setuptools
pip install Django==3.2 djangorestframework==3.12.4 django-cors-headers==3.10.0 djangorestframework-simplejwt==5.0.0 drf-yasg==1.20.0 python-dateutil==2.8.2 requests==2.27.1 django-celery-results==2.2.0
python manage.py runserver 