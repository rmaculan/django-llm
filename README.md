# LocalLLMChat

A Django application that provides a chat interface for interacting with a local large language model (LLM). The application is containerized using Docker and includes features like user authentication, chat history, and response caching.

## Features

- User authentication and session management
- Interactive chat interface
- Local LLM integration (using GPT-2 by default)
- Chat history and session management
- Response caching using Redis
- PostgreSQL database for data persistence
- Docker containerization
- Modern, responsive UI using Bootstrap

## Prerequisites

- Docker and Docker Compose
- Python 3.9 or higher (for local development)
- Git

## Quick Start

1. Clone the repository:
```bash
git clone https://github.com/rmaculan/django-llm.git
cd django-llm

email: robdesignsoftware@proton.me for .env or
create a django app and insert it to this project.
Once finished, proceed to step 2.
```

2. Create a `.env` file in the project root:
```bash
DJANGO_SECRET_KEY=your-secret-key-here
DJANGO_DEBUG=True
POSTGRES_DB=local_llm
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_HOST=db
POSTGRES_PORT=5432
REDIS_URL=redis://redis:6379/0
```

3. Build and start the containers:
```bash
docker-compose up --build
```

4. Create a superuser (in a new terminal):
```bash
docker-compose exec web python manage.py createsuperuser
```

5. Access the application:
- Main application: http://localhost:8000/chat/
- Admin interface: http://localhost:8000/admin/
- Login page: http://localhost:8000/login/

## Development Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up the database:
```bash
python manage.py migrate
```

4. Create a superuser:
```bash
python manage.py createsuperuser
```

5. Run the development server:
```bash
python manage.py runserver
```

## Project Structure

```
django-llm/
├── chat/                    # Main application
│   ├── models.py           # Database models
│   ├── views.py            # View functions
│   ├── urls.py             # URL routing
│   ├── services/           # Business logic
│   │   └── llm_service.py  # LLM integration
│   └── templates/          # HTML templates
├── local_llm_chat/         # Project settings
│   ├── settings.py         # Django settings
│   └── urls.py             # Main URL routing
├── static/                 # Static files
├── templates/              # Base templates
├── Dockerfile             # Docker configuration
├── docker-compose.yml     # Docker services
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## Customization

### Changing the LLM Model

The application uses GPT-2 by default. To use a different model:

1. Modify the `model_name` parameter in `chat/services/llm_service.py`
2. Rebuild the Docker container:
```bash
docker-compose up --build
```

### Adding New Features

1. Create new models in `chat/models.py`
2. Add views in `chat/views.py`
3. Update URL patterns in `chat/urls.py`
4. Create templates in `chat/templates/chat/`

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

See the LICENSE file for details. 
