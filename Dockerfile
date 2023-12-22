FROM python:3.10
#LABEL maintainer=""

COPY --chown=www-data:www-data requirements.txt /var/app/requirements.txt
RUN pip install -U pip
RUN pip install -r /var/app/requirements.txt
COPY --chown=www-data:www-data core /var/app/
RUN chown -R www-data:www-data /var/app/
WORKDIR /var/app
#CMD python manage.py makemigrations; python manage.py migrate; python manage.py runserver 0.0.0.0:8000
EXPOSE 8000
