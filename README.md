# Luma — Agentic AI Todo Application

![Agentic AI Todo Application](Images/Image%201.png)

Luma is an AI-powered task management application that combines a conversational AI assistant with task management and Google Calendar integration.

## Features

- Create tasks using natural language
- View and search existing tasks
- Update and reschedule tasks
- Delete individual tasks
- Complete overdue tasks
- Query today's tasks and pending tasks
- Automatically create Google Calendar events for scheduled tasks
- Keep task changes synchronized with Google Calendar
- Web-based dashboard for viewing tasks and calendar events
- MySQL database for persistent task storage

## Architecture

```text
User
 │
 ▼
Luma Frontend
 │
 ├── GET /tasks
 │
 └── POST /chat
        │
        ▼
   FastAPI Backend
        │
        ▼
    Agno Agent
        │
        ▼
    Groq LLM
        │
        ▼
      Tools
     /     \
    ▼       ▼
 MySQL   Google Calendar
```

## Tech Stack

### Backend
- Python
- FastAPI
- Agno
- Groq
- MySQL

### Frontend
- HTML
- CSS
- JavaScript
- FullCalendar

### Integrations
- Google Calendar API

### Authentication & Configuration
- Google OAuth 2.0
- Environment variables using `.env`

## Project Structure

```text
Agentic-AI-Todo-Application/
│
├── agent.py
├── app.py
├── calendar_service.py
├── config.py
├── database.py
├── models.py
├── tools.py
├── test_calendar.py
├── requirements.txt
├── .gitignore
│
└── frontend/
    ├── index.html
    ├── script.js
    └── style.css
```

## How It Works

The user interacts with Luma through the web interface.

For conversational requests, the frontend sends the user's message to the FastAPI `/chat` endpoint. The Agno agent uses the configured Groq model and available tools to determine which task operation is required.

Task information is stored in MySQL.

When a task contains a scheduled date and time, Luma can create a corresponding Google Calendar event. Updates and deletions can also be synchronized with the associated calendar event.

The dashboard retrieves task data through the `/tasks` endpoint and calendar events through the `/calendar/events` endpoint.

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/AashimaFathima/Agentic-AI-Todo-Application.git
cd Agentic-AI-Todo-Application
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows:

```bash
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file:

```env
GROQ_API_KEY=your_groq_api_key

DB_HOST=localhost
DB_PORT=3306
DB_USER=your_mysql_user
DB_PASSWORD=your_mysql_password
DB_NAME=your_database_name
```

Do not commit `.env` to GitHub.

### 5. Configure Google Calendar

Create Google OAuth credentials and place the downloaded credentials file in the project root as:

```text
credentials.json
```

The application generates `token.json` after completing the Google OAuth flow.

Both files are excluded from Git using `.gitignore`.

### 6. Start the backend

```bash
uvicorn app:app --reload
```

The FastAPI server will run at:

```text
http://127.0.0.1:8000
```

### 7. Open the frontend

Open:

```text
frontend/index.html
```

in your browser.

## API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| POST | `/chat` | Send a natural-language request to the AI agent |
| GET | `/tasks` | Retrieve stored tasks |
| GET | `/calendar/events` | Retrieve Google Calendar events |


## License

This project is licensed under the MIT License. See [LICENSE](LICENSE).
