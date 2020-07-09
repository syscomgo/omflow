@echo off

set app=omflow omuser ommessage omformflow omdashboard omformmodel omservice ommission ommonitor ompolicymodel omorganization
for %%b in (%app%) do python manage.py makemigrations %%b

python manage.py migrate

