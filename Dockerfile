FROM python:3.9-buster

ENV PYTHONUNBUFFERED 1

RUN apt-get update -y &&  apt-get install xvfb -y && apt-get install xfonts-100dpi xfonts-75dpi xfonts-scalable xfonts-cyrillic -y && apt-get install wkhtmltopdf -y

RUN mkdir /code

WORKDIR /code

COPY ./rtf/requirements.txt /code

RUN pip install -r requirements.txt

COPY . /code/

COPY ./rtf/config.ini.dev /code/config.ini

RUN python rtf/manage.py makemigrations

RUN python rtf/manage.py migrate

EXPOSE 8002

CMD python manage.py runserver 0.0.0.0:8002
