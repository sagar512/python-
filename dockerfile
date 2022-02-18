FROM python:3.9-buster

ENV PYTHONUNBUFFERED 1

RUN apt-get update -y &&  apt-get install xvfb -y && apt-get install xfonts-100dpi xfonts-75dpi xfonts-scalable xfonts-cyrillic -y && apt-get install wkhtmltopdf -y

RUN mkdir /code

WORKDIR /code

COPY requirements.txt /code/

#RUN pip install --upgrade pip

RUN pip install -r requirements.txt

COPY . /code/

COPY ./config.ini.dev /code/config.ini

RUN python manage.py migrate

EXPOSE 8000

CMD python manage.py runserver 0.0.0.0:8000