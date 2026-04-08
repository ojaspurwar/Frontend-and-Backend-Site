# FastAPI Portfolio Website

A modern, full-featured personal portfolio website built with FastAPI, SQLAlchemy, and Jinja2 templates.

## Features

✅ **Multi-page Portfolio** - Home, About, Portfolio, Contact pages
✅ **Project Management** - Add, edit, delete, and display your projects
✅ **Contact Form** - Collect visitor messages with email validation
✅ **RESTful API** - Full CRUD operations for projects and contacts
✅ **Database** - SQLite by default (easily switch to PostgreSQL)
✅ **Responsive Design** - Mobile-friendly UI
✅ **Modern Tech Stack** - FastAPI, SQLAlchemy, Jinja2, HTML5, CSS3

## Project Structure

```
portfolio_website/
├── app/
│   ├── __init__.py          # Package init
│   ├── database.py          # Database configuration
│   ├── models.py            # SQLAlchemy data models
│   ├── schemas.py           # Pydantic request/response schemas
│   └── crud.py              # Database operations
├── templates/
│   ├── base.html            # Base template with navigation
│   ├── index.html           # Home page
│   ├── about.html           # About page
│   ├── portfolio.html       # Portfolio/Projects page
│   └── contact.html         # Contact page
├── static/
│   ├── css/
│   │   └── style.css        # Styling
│   └── js/
│       └── script.js        # JavaScript enhancements
├── main.py                  # FastAPI application entry point
├── requirements.txt         # Python dependencies
├── .env                     # Environment variables
└── README.md                # This file
```

## Installation

### 1. Clone or Navigate to Project

```bash
cd portfolio_website
```

### 2. Create Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Initialize Database

The database will be automatically created when you run the application. It creates a `portfolio.db` SQLite file.

## Running the Application

Start the development server:

```bash
python main.py
```

Or using uvicorn directly:

```bash
uvicorn main:app --reload
```

The application will be available at:
- **Website**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Alternative API Docs**: http://localhost:8000/redoc

## API Endpoints

### Projects
- `GET /api/projects` - List all projects
- `GET /api/projects/{id}` - Get specific project
- `POST /api/projects` - Create new project
- `PUT /api/projects/{id}` - Update project
- `DELETE /api/projects/{id}` - Delete project

### Contact Messages
- `POST /api/contact` - Submit contact form
- `GET /api/contacts` - List all contact messages

### Other
- `GET /health` - Health check endpoint

## Adding Sample Projects

You can add projects via the REST API. Example using curl:

```bash
curl -X POST "http://localhost:8000/api/projects" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "E-Commerce Platform",
    "description": "A full-stack e-commerce platform with payment integration",
    "image_url": "https://example.com/image.jpg",
    "project_url": "https://example.com",
    "github_url": "https://github.com/user/project",
    "technologies": "Python, FastAPI, React, PostgreSQL"
  }'
```

## Customization

### Update Site Content
Edit these files to customize your portfolio:
- **Navigation**: `templates/base.html`
- **Home Page**: `templates/index.html`
- **About Page**: `templates/about.html`
- **Contact Info**: `templates/contact.html`
- **Styling**: `static/css/style.css`

### Update Personal Information
Edit contact information in `templates/contact.html`:
- Email
- Phone
- Location

### Colors & Branding
Edit CSS variables in `static/css/style.css`:
```css
:root {
    --primary-color: #3498db;
    --secondary-color: #2c3e50;
    /* ... */
}
```

## Database

Default database: SQLite (`portfolio.db`)

To use PostgreSQL instead, update `.env`:
```
DATABASE_URL=postgresql://user:password@localhost/portfolio_db
```

And install psycopg2:
```bash
pip install psycopg2-binary
```

## Deployment

### Local Development
```bash
python main.py
```

### Production with Uvicorn
```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

### Using Gunicorn (Recommended for Production)
```bash
pip install gunicorn
gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app
```

### Docker Deployment

Create a `Dockerfile`:
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Build and run:
```bash
docker build -t portfolio-website .
docker run -p 8000:8000 portfolio-website
```

## Technologies Used

- **Backend Framework**: FastAPI
- **ORM**: SQLAlchemy
- **Validation**: Pydantic
- **Templates**: Jinja2
- **Database**: SQLite (default) / PostgreSQL
- **Frontend**: HTML5, CSS3, JavaScript
- **Server**: Uvicorn
- **API Documentation**: Swagger UI, ReDoc

## Features to Add

Ideas for extending this project:
- [ ] Blog/Articles page with markdown support
- [ ] Admin dashboard for project management
- [ ] Authentication & user accounts
- [ ] Search functionality
- [ ] Categories/Tags for projects
- [ ] Image upload functionality
- [ ] Email notifications for contact submissions
- [ ] Analytics integration
- [ ] RSS feed
- [ ] Dark mode toggle

## Troubleshooting

**Port already in use:**
```bash
uvicorn main:app --port 8001
```

**Database issues:**
Delete `portfolio.db` and restart the application to recreate the database.

**Import errors:**
Make sure virtual environment is activated and dependencies are installed:
```bash
pip install -r requirements.txt
```

## License

This project is open source and available under the MIT License.

## Contact & Support

For questions or issues, please refer to the [FastAPI documentation](https://fastapi.tiangolo.com/) or [SQLAlchemy documentation](https://docs.sqlalchemy.org/).

---

Happy coding! 🚀
