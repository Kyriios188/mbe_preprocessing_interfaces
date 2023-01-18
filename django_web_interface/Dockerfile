FROM python:3.10-buster

EXPOSE 8000
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY . /code
RUN pip install -r /code/requirements.txt


RUN apt-get update
RUN apt-get install netcat -y
RUN apt-get install mariadb-client -y

COPY ./docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh
ENTRYPOINT ["/docker-entrypoint.sh"]
