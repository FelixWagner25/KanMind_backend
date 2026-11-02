# KanMind

KanMind is a bakcend for a task management application following the Kanban style. It comprises the management of boards, tasks, comments and token-based authentication are part of this project.
This projekct was developed as part of the Developer Akademie Backend Course.

## Features

- User registration and login with token authentication,
- Email availability check,
- Task Board management with owners and member,
- Task management with creation, assignment, review assignment and comments,
- Permission management depending on owners and members.

## Local Installation

### 1. Clone the repository

```bash
git clone https://github.com/FelixWagner25/KanMind_backend.git
cd KanMind_backend
```

### 2. Create and activate a virtual environment

**Windows (CMD):**

```bash
python -m venv .venv
.\.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Apply model migrations

```bash
python manage.py migrate
```

### 6. Run the development server

```bash
python manage.py runserver
```

The API is available at `http://127.0.0.1:8000/api/`.

## License

This project is intended for educational purposes only. You are welcome to view and explore the code but redistribution and commercial use is not permitted.
