from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from .database import engine, Base, get_db
from .models import Ticket
from uuid import uuid4
from datetime import datetime
from .celery_app import process_ticket
import logging
from fastapi.middleware.cors import CORSMiddleware
import json

Base.metadata.create_all(bind=engine)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(Exception)
async def exception_handler(request, exc):
    logger.error(f"An error occurred: {exc}")
    return json.dumps({"status_code":500,"content":{"message": "An internal error occurred"},})
    
class TicketCreate(BaseModel):
    subject: str
    body: str
    customer_email: str

@app.post("/ticket")
async def create_ticket(ticket: TicketCreate, db: Session = Depends(get_db)):
    ticket_id = str(uuid4())
    db_ticket = Ticket(
        id=ticket_id,
        subject=ticket.subject,
        body=ticket.body,
        customer_email=ticket.customer_email,
        status="submitted",
        created_at=datetime.utcnow(),
    )
    db.add(db_ticket)
    db.commit()
    db.refresh(db_ticket)
    return {"ticket_id": ticket_id, "status": "submitted", "message": "Ticket submitted successfully and queued for processing"}

@app.get("/ticket/{ticket_id}")
async def get_ticket(ticket_id: str, db: Session = Depends(get_db)):
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if ticket is None:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return ticket

@app.get("/tickets")
async def get_tickets(category: str = None, priority: str = None, status: str = None, db: Session = Depends(get_db)):
    query = db.query(Ticket)
    if category:
        query = query.filter(Ticket.category == category)
    if priority:
        query = query.filter(Ticket.priority == priority)
    if status:
        query = query.filter(Ticket.status == status)
    tickets = query.all()
    return {"tickets": tickets}

@app.post("/process")
async def process_tickets(db: Session = Depends(get_db)):
    try:
        unprocessed_tickets = db.query(Ticket).filter(Ticket.status == "submitted").all()
        for ticket in unprocessed_tickets:
            process_ticket(ticket.id)
        return {"message": f"Processing started for {len(unprocessed_tickets)} tickets"}
    except Exception as e:
        logger.error(f"An error occurred while processing tickets: {e}")
        raise HTTPException(status_code=500, detail="An internal error occurred")

