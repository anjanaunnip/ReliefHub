# ReliefHub

ReliefHub is a web-based disaster relief coordination platform that connects donors, volunteers, and relief organizations to efficiently manage and distribute resources during emergencies such as floods, earthquakes, and other natural disasters.

## Features
- Centralized disaster relief coordination platform
- Donor registration and donation management
- Volunteer participation and task allocation
- Request tracking for affected communities
- Real-time updates on resource availability
- Admin panel for managing relief operations

## Tech Stack

Frontend:
HTML
CSS
JavaScript
Bootstrap

Backend:
Python
Django

Database:
SQLite / MySQL

Tools:
VS Code
Git
GitHub

## Project Structure

ReliefHub/
│
├── ReliefHub/            # Django project configuration
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── home/                 # Main application
│   ├── migrations/
│   ├── templates/
│   ├── static/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── admin.py
│
├── manage.py
├── requirements.txt
└── .gitignore

## Installation

Clone the repository

git clone https://github.com/anjanaunnip/ReliefHub.git

Navigate to the project folder

cd ReliefHub

Create virtual environment

python -m venv venv

Activate virtual environment

Windows:
venv\Scripts\activate

Mac/Linux:
source venv/bin/activate

Install dependencies

pip install -r requirements.txt

Run database migrations

python manage.py migrate

Start the development server

python manage.py runserver

Open in browser

http://127.0.0.1:8000/

## Future Improvements
- Real-time disaster alerts
- Map-based resource tracking
- Mobile application support
- AI-based resource allocation

## Author

Anjana Unni P  
MCA Student | AI & Full Stack Developer  
LinkedIn: https://linkedin.com/in/anjanaunnip
