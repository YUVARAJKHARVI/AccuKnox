FROM python:3.8-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /social_network

COPY ../requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD ["gunicorn", "--bind", ":8000", "social_network.wsgi:application"]
