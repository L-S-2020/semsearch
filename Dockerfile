FROM python:3.10

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . code
WORKDIR /code

EXPOSE 7777

ENTRYPOINT ["python", "manage.py"]
CMD ["runserver", "0.0.0.0:7777"]