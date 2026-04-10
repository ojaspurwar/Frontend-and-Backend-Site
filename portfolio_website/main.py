from fastapi import FastAPI, Depends, HTTPException, Request, Response, Form
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
import os
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pathlib import Path
import time
import psutil
import socket
import secrets
from datetime import datetime

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

# Add session middleware with cross-domain support
from starlette.middleware.sessions import SessionMiddleware
app.add_middleware(
    SessionMiddleware, 
    secret_key="your-secret-key-change-in-production",
    session_cookie="session",
    max_age=86400,  # 24 hours
    same_site="none"  # Allow cross-domain cookies
)

# Add CORS middleware to allow cross-origin requests
from starlette.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for localtunnel support
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
static_dir = BASE_DIR / "static"
app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

# Setup Jinja2 templates
templates_dir = BASE_DIR / "templates"
templates = Jinja2Templates(directory=str(templates_dir))

# ==================== Helper Functions ====================

def send_contact_email(contact: schemas.ContactCreate):
    """Send contact form submission email"""
    try:
        # Email configuration
        sender_email = "noreply@yourportfolio.com"  # Replace with your sender email
        receiver_email = config["personal"]["email"]
        smtp_server = "smtp.gmail.com"  # Replace with your SMTP server
        smtp_port = 587
        smtp_username = os.getenv("SMTP_USERNAME")  # Set these environment variables
        smtp_password = os.getenv("SMTP_PASSWORD")

        # Create message
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg['Subject'] = f"New Contact Form Submission from {contact.name}"

        body = f"""
        New contact form submission:

        Name: {contact.name}
        Email: {contact.email}
        Message:
        {contact.message}
        """
        msg.attach(MIMEText(body, 'plain'))

        # Send email (only if SMTP credentials are configured)
        if smtp_username and smtp_password:
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
            server.login(smtp_username, smtp_password)
            text = msg.as_string()
            server.sendmail(sender_email, receiver_email, text)
            server.quit()
            print(f"Email sent successfully to {receiver_email}")
        else:
            print("SMTP credentials not configured - email not sent")

    except Exception as e:
        print(f"Failed to send email: {e}")

# ==================== Admin Authentication ====================

ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "Zeq26TyB65Rt@b1"
admin_tokens = {}  # Store admin tokens for cross-domain access

def check_admin_auth(request: Request):
    """Check if user is authenticated as admin"""
    # Check session
    if request.session.get("admin_authenticated", False):
        return True
    
    # Fallback: check URL token for localtunnel support
    token = request.query_params.get("admin_token")
    if token and token in admin_tokens:
        request.session["admin_authenticated"] = True
        return True
    
    return False

def require_admin_auth(request: Request):
    """Require admin authentication"""
    if not check_admin_auth(request):
        raise HTTPException(status_code=401, detail="Admin authentication required")
    return True

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
    # Save to database
    db_contact = crud.create_contact(db=db, contact=contact)
    
    # Send email notification
    send_contact_email(contact)
    
    return db_contact

@app.get("/api/contacts", response_model=list[schemas.Contact])
async def list_contacts(skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    return crud.get_contacts(db, skip=skip, limit=limit)

@app.delete("/api/contacts/{contact_id}")
async def delete_contact_endpoint(contact_id: int, db: Session = Depends(get_db)):
    contact = crud.delete_contact(db, contact_id=contact_id)
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    return {"detail": "Contact deleted successfully"}

@app.delete("/api/contacts")
async def delete_all_contacts_endpoint(db: Session = Depends(get_db)):
    crud.delete_all_contacts(db)
    return {"detail": "All contacts deleted successfully"}

# ==================== Admin Routes ====================

# Admin login page
@app.get("/admin/login", response_class=HTMLResponse)
async def admin_login(request: Request):
    if check_admin_auth(request):
        return RedirectResponse(url="/admin/dashboard", status_code=302)
    return templates.TemplateResponse(request=request, name="admin_login.html", context={"config": config})

# Admin login POST
@app.post("/admin/login")
async def admin_login_post(request: Request, username: str = Form(...), password: str = Form(...)):
    if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
        request.session["admin_authenticated"] = True
        # Generate a secure token for localtunnel access
        token = secrets.token_urlsafe(32)
        admin_tokens[token] = True
        request.session["admin_token"] = token
        return RedirectResponse(url=f"/admin/dashboard?admin_token={token}", status_code=302)
    return templates.TemplateResponse(
        request=request, 
        name="admin_login.html", 
        context={"config": config, "error": "Invalid credentials"}
    )

# Admin logout
@app.post("/admin/logout")
async def admin_logout(request: Request):
    request.session.pop("admin_authenticated", None)
    return RedirectResponse(url="/admin/login", status_code=302)

# Admin dashboard
@app.get("/admin/dashboard", response_class=HTMLResponse)
async def admin_dashboard(request: Request, db: Session = Depends(get_db)):
    require_admin_auth(request)
    
    # Get server status
    server_status = get_server_status(db)
    
    # Get recent contacts (last 50) and convert to dict for template
    contacts_db = crud.get_contacts(db, skip=0, limit=50)
    contacts = []
    for contact in contacts_db:
        contacts.append({
            'id': contact.id,
            'name': contact.name,
            'email': contact.email,
            'message': contact.message,
            'created_at': contact.created_at
        })
    
    return templates.TemplateResponse(
        request=request, 
        name="admin_dashboard.html", 
        context={"config": config, "server_status": server_status, "contacts": contacts}
    )

# ==================== Helper Functions ====================

def get_server_status(db: Session):
    """Get comprehensive server status information"""
    try:
        # Database status
        db_status = "Connected"
        contact_count = db.query(models.Contact).count()
        
        # System info
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        
        # Disk usage (handle Windows vs Unix paths)
        try:
            if os.name == 'nt':  # Windows
                disk = psutil.disk_usage('C:\\')
            else:  # Unix/Linux
                disk = psutil.disk_usage('/')
        except:
            disk = type('MockDisk', (), {'percent': 0, 'used': 0, 'total': 0})()
        
        # Server IP address
        try:
            hostname = socket.gethostname()
            server_ip = socket.gethostbyname(hostname)
        except:
            server_ip = "Unable to determine"
        
        # Server uptime (simplified - would need to track start time)
        uptime = "Server running"
        
        return {
            "database": {
                "status": db_status,
                "contacts_count": contact_count
            },
            "system": {
                "cpu_usage": f"{cpu_percent}%",
                "memory_usage": f"{memory.percent}%",
                "memory_used": f"{memory.used / (1024**3):.1f} GB",
                "memory_total": f"{memory.total / (1024**3):.1f} GB",
                "disk_usage": f"{disk.percent}%",
                "disk_used": f"{disk.used / (1024**3):.1f} GB",
                "disk_total": f"{disk.total / (1024**3):.1f} GB"
            },
            "server": {
                "status": "Online",
                "ip_address": server_ip,
                "uptime": uptime,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
        }
    except Exception as e:
        return {
            "error": f"Failed to get server status: {str(e)}",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

# Health check with comprehensive status
@app.get("/health", response_class=HTMLResponse)
async def health_check(request: Request, db: Session = Depends(get_db)):
    try:
        server_status = get_server_status(db)
        return templates.TemplateResponse(
            request=request,
            name="health.html",
            context={
                "config": config,
                "health_data": {
                    "status": "online",
                    "server": server_status.get("server", {}),
                    "system": server_status.get("system", {}),
                    "database": server_status.get("database", {}),
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
            }
        )
    except Exception as e:
        return templates.TemplateResponse(
            request=request,
            name="health.html",
            context={
                "config": config,
                "health_data": {
                    "status": "error",
                    "error": str(e),
                    "timestamp": datetime.now().isoformat()
                }
            }
        )

# Health check API endpoint (JSON)
@app.get("/api/health")
async def health_check_api(db: Session = Depends(get_db)):
    try:
        server_status = get_server_status(db)
        return {
            "status": "online",
            "server": server_status.get("server", {}),
            "system": server_status.get("system", {}),
            "database": server_status.get("database", {}),
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
