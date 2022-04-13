FROM python:3.9-buster

ENV PYTHONUNBUFFERED 1

RUN apt-get update -y &&  apt-get install xvfb -y && apt-get install xfonts-100dpi xfonts-75dpi xfonts-scalable xfonts-cyrillic -y && apt-get install wkhtmltopdf -y

RUN mkdir /code

WORKDIR /code

COPY requirements.txt /code/

RUN pip install -r requirements.txt

COPY . /code/

COPY ./config.ini.dev /code/config.ini

RUN python manage.py makemigrations logpipe

RUN python manage.py migrate

EXPOSE 8001



CMD python manage.py runserver 0.0.0.0:8001 --noreload

FROM celery import Celery
 app = Celery('vwadaptor',
             broker='redis://workerdb:6379/0',
             backend='redis://workerdb:6379/0')

 app.control.inspect().active()

CMD celery -A rtf worker -B -l info