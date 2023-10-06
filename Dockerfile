FROM python:3.8

ENV DockerHOME=/home/app/webapp

RUN mkdir -p ${DockerHOME}

WORKDIR ${DockerHOME}

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip 

COPY requirement.txt  ${DockerHOME}

RUN pip install -r requirement.txt 

COPY . ${DockerHOME}

EXPOSE 8000

CMD python manage.py runserver
