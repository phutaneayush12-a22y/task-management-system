# Task Management System

A full-stack task management application built with **Flask**, **PostgreSQL**, **WebSockets**, and **Pandas/NumPy** analytics.

## Features

- 🔐 User Authentication (Register/Login/Logout)
- ✅ Task CRUD Operations (Create, Read, Update, Delete)
- 📊 Analytics Dashboard with Pandas & NumPy
- 🔔 Real-time WebSocket Notifications
- 🎨 Responsive HTML/CSS Frontend
- 🗄️ PostgreSQL Database with SQLAlchemy ORM

## Tech Stack

- **Backend**: Python Flask
- **Database**: PostgreSQL
- **ORM**: SQLAlchemy
- **Real-time**: Flask-SocketIO
- **Analytics**: Pandas, NumPy
- **Frontend**: HTML, CSS, JavaScript

## Installation

### Prerequisites
- Python 3.8+
- PostgreSQL 16+

### Setup Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/phutaneayush12-a22y/task-management-system.git
   cd task-management-system

       Create virtual environment
    bash

    python -m venv venv
    venv\Scripts\activate  # Windows

    Install dependencies
    bash

    pip install -r requirements.txt

    Configure PostgreSQL
    sql

    CREATE DATABASE task_management;

    Create .env file
    env

    DATABASE_URL=postgresql://postgres:your_password@localhost:5432/task_management
    SECRET_KEY=your-secret-key
    JWT_SECRET_KEY=your-jwt-secret-key

    Run the application
    bash

    python app.py

    Open browser at http://localhost:5000

API Endpoints
Method	Endpoint	Description
POST	/api/auth/register	Register user
POST	/api/auth/login	Login user
POST	/api/auth/logout	Logout user
GET	/api/tasks/	Get all tasks
POST	/api/tasks/	Create task
PUT	/api/tasks/<id>	Update task
DELETE	/api/tasks/<id>	Delete task
GET	/api/analytics/dashboard	Get analytics
WebSocket Events
Event	Direction	Description
connect	Client → Server	Establish WebSocket connection
task_updated	Server → Client	Live task updates
Project Structure
text

task-management-system/
├── app.py                 # Main application
├── config.py              # Configuration
├── database.py            # Database instance
├── socketio_instance.py   # WebSocket instance
├── models/                # Database models
├── routes/                # API routes
├── static/                # Frontend files
├── templates/             # HTML templates
└── requirements.txt       # Dependencies

Demo Video

https://drive.google.com/drive/u/0/folders/1N627o6n4bTV8Lo77ObwDPoc1UOHOhldU
Author

Ayush Phutane
License

This project was created for a Python Development Internship Assignment.

