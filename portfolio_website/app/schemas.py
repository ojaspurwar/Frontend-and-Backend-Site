from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class ProjectBase(BaseModel):
    title: str
    description: str
    image_url: Optional[str] = None
    project_url: Optional[str] = None
    github_url: Optional[str] = None
    technologies: Optional[str] = None

class ProjectCreate(ProjectBase):
    pass

class ProjectUpdate(ProjectBase):
    pass

class Project(ProjectBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class ContactCreate(BaseModel):
    name: str
    email: EmailStr
    message: str

class Contact(ContactCreate):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
