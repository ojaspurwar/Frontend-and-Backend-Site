from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
import os
import json
from pathlib import Path

from app.database import engine, get_db, Base
from app import crud, schemas, models

# Get the directory where this script is located
BASE_DIR = Path(__file__).resolve().parent

# Load config file
CONFIG_FILE = BASE_DIR / "config.json"
with open(CONFIG_FILE, "r") as f:
    config = json.load(f)

# Create all tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(title="Portfolio Website", version="1.0.0")

# Mount static files
static_dir = BASE_DIR / "static"
app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

# Setup Jinja2 templates
templates_dir = BASE_DIR / "templates"
templates = Jinja2Templates(directory=str(templates_dir))

# ==================== Routes ====================

# Home page
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(request=request, name="index.html", context={"config": config})

# About page
@app.get("/about", response_class=HTMLResponse)
async def about(request: Request):
    return templates.TemplateResponse(request=request, name="about.html", context={"config": config})

# Portfolio/Projects page
@app.get("/portfolio", response_class=HTMLResponse)
async def portfolio(request: Request, db: Session = Depends(get_db)):
    projects = crud.get_projects(db, skip=0, limit=100)
    return templates.TemplateResponse(request=request, name="portfolio.html", context={"projects": projects, "config": config})

# Contact page
@app.get("/contact", response_class=HTMLResponse)
async def contact(request: Request):
    return templates.TemplateResponse(request=request, name="contact.html", context={"config": config})

# ==================== API Routes ====================

# Projects API
@app.get("/api/projects", response_model=list[schemas.Project])
async def list_projects(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_projects(db, skip=skip, limit=limit)

@app.get("/api/projects/{project_id}", response_model=schemas.Project)
async def get_project(project_id: int, db: Session = Depends(get_db)):
    project = crud.get_project(db, project_id=project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project

@app.post("/api/projects", response_model=schemas.Project)
async def create_project(project: schemas.ProjectCreate, db: Session = Depends(get_db)):
    return crud.create_project(db=db, project=project)

@app.put("/api/projects/{project_id}", response_model=schemas.Project)
async def update_project(project_id: int, project: schemas.ProjectUpdate, db: Session = Depends(get_db)):
    db_project = crud.update_project(db=db, project_id=project_id, project=project)
    if not db_project:
        raise HTTPException(status_code=404, detail="Project not found")
    return db_project

@app.delete("/api/projects/{project_id}")
async def delete_project(project_id: int, db: Session = Depends(get_db)):
    db_project = crud.delete_project(db=db, project_id=project_id)
    if not db_project:
        raise HTTPException(status_code=404, detail="Project not found")
    return {"detail": "Project deleted"}

# Contact API
@app.post("/api/contact", response_model=schemas.Contact)
async def submit_contact(contact: schemas.ContactCreate, db: Session = Depends(get_db)):
    return crud.create_contact(db=db, contact=contact)

@app.get("/api/contacts", response_model=list[schemas.Contact])
async def list_contacts(skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    return crud.get_contacts(db, skip=skip, limit=limit)

# Health check
@app.get("/health")
async def health_check():
    return {"status": "online"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
