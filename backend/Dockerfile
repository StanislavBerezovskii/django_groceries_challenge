FROM python:3.11-slim

RUN python -m pip install --upgrade pip

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt --no-cache-dir

COPY backend/ /app

CMD ["gunicorn", "backend.wsgi:application", "--bind", "0:8000"]