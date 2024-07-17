FROM python:3.11-slim

RUN mkdir /app

COPY requirements.txt /app

RUN python -m pip install --upgrade pip

RUN pip install -r /app/requirements.txt --no-cache-dir

COPY backend/ /app

WORKDIR /app

CMD ["python", "manage.py", "runserver", "0:8000"]