from celery import Celery
from .settings import settings
from .ai import categorize_ticket, prioritize_ticket, generate_response
import datetime
import logging
from .database import SessionLocal
from .models import Ticket
import time
celery = Celery(__name__)
celery.conf.broker_url = settings.broker_url
celery.conf.result_backend = settings.result_backend

logger = logging.getLogger(__name__)

# @celery.task
def process_ticket(ticket_id:str):
    logger.info(f"Starting to process ticket {ticket_id}")
    db = SessionLocal()
    try:
        ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
        if not ticket:
            print(f"Ticket with id {ticket_id} not found.")
            return

        print(f"Processing ticket {ticket_id}...")

        category, category_confidence = categorize_ticket(ticket.subject, ticket.body)
        priority, priority_confidence = prioritize_ticket(ticket.subject, ticket.body)
        initial_response = generate_response(ticket.subject, ticket.body)

        print(f"Categorized ticket {ticket_id}: {category} with confidence {category_confidence}")
        print(f"Prioritized ticket {ticket_id}: {priority} with confidence {priority_confidence}")
        print(f"Generated response for ticket {ticket_id}: {initial_response}")

        ticket.category = category
        ticket.category_confidence = category_confidence
        ticket.priority = priority
        ticket.priority_confidence = priority_confidence
        ticket.initial_response = initial_response
        ticket.status = "processed"
        ticket.processed_at = datetime.utcnow()

        db.commit()
        print(f"Ticket {ticket_id} processed successfully.")
    except Exception as e:
        print(f"Error processing ticket {ticket_id}: {e}")
    finally:
        db.close()