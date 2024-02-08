FROM python:3.10-alpine

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt --no-cache-dir

COPY . .

RUN python manage.py makemigrations

RUN python manage.py migrate

# Test-data import
RUN python manage.py testimport

CMD ["python", "manage.py", "runserver", "0:8000"]