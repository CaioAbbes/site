# syntax=docker/dockerfile:1

FROM python:3.11


WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "domenic.wsgi:edtech"]