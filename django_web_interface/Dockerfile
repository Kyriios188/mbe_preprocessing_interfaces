FROM python:3.10-buster

EXPOSE 8000
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY . /code
RUN pip install -r /code/requirements.txt

ENTRYPOINT ["python", "manage.py", "runserver", "0.0.0.0:8000"]
