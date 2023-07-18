FROM python:3.10

RUN mkdir /api && mkdir /api/static

WORKDIR /api

EXPOSE 8000

COPY . .

RUN pip install -r requirements.txt

CMD ["bash", "./run.sh"]
#CMD ["python", "manage.py", "runserver"]
