# Django Social Networking API

This is a Django-based social networking application API with the following functionalities:

- User login/signup
- Search users by email or name
- Send/accept/reject friend requests
- List friends
- List pending friend requests
- Throttling friend requests to 3 per minute

## Features

- User authentication with email and password
- User search functionality with pagination
- Friend request management
- Dockerized for easy deployment

## Prerequisites

- Docker and Docker Compose installed on your machine
- Git installed on your machine

## Getting Started

### 1. Steps

```sh
git clone https://github.com/YUVARAJKHARVI/AccuKnox.git
cd AccuKnox

python3 -m venv social_network-env
source social_network-env/bin/activate 

cd social_network

pip install -r requirements.txt

# Build the Docker containers
docker-compose build

# Run the Docker containers
docker-compose up

docker-compose run web python manage.py migrate (exists db.sqlite3 already migrated)

docker-compose run web python manage.py createsuperuser

docker-compose run web python manage.py runserver

**Web Pages**
Signup: http://127.0.0.1:8000/
Login: http://127.0.0.1:8000/login/

**API Endpoints**
Search Users: /api/search/
Send Friend Request: /api/friend-request/
Accept Friend Request: /api/friend-request/<id>/
List Friends: /api/friends/
List Pending Friend Requests: /api/pending-requests/

Postman Collection : https://elements.getpostman.com/redirect?entityId=19239984-e4d89a81-349f-4a57-b0f4-4b0f5fa62018&entityType=collection
