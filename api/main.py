from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from api.database import get_db
from api import models, schemas

# Initialize the API
app = FastAPI(
    title="The Acutis API",
    description="The Open-Source Catholic Database inspired by Blessed Carlo Acutis.",
    version="1.0.0"
)

@app.get("/")
def root():
    return {
        "message": "Welcome to The Acutis API.",
        "docs_url": "/docs",
        "status": "Online"
    }

# SAINTS ENDPOINTS
@app.get("/api/v1/saints", response_model=List[schemas.SaintResponse])
def get_all_saints(db: Session = Depends(get_db)):
    """
    Retrieve a list of all saints in the database.
    """
    saints = db.query(models.Saint).all()
    return saints

# POPES ENDPOINTS
@app.get("/api/v1/popes", response_model=List[schemas.PopeResponse])
def get_all_popes(db: Session = Depends(get_db)):
    """
    Retrieve a list of all popes in the database.
    """
    popes = db.query(models.Pope).order_by(models.Pope.succession_number).all()
    return popes