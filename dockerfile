FROM python:3.9-buster

ENV PYTHONUNBUFFERED 1

RUN apt-get update -y &&  apt-get install xvfb -y && apt-get install xfonts-100dpi xfonts-75dpi xfonts-scalable xfonts-cyrillic -y && apt-get install wkhtmltopdf -y

RUN mkdir /code

WORKDIR /code

COPY requirements.txt /code/

RUN pip install -r requirements.txt

#RUN python manage.py makemigrations logpipe

RUN python manage.py migrate

COPY . /code/

COPY ./config.ini.dev /code/config.ini

EXPOSE 8001

CMD python manage.py runserver 0.0.0.0:8001 --noreload

