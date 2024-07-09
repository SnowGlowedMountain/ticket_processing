import openai
from anthropic import Anthropic
from .settings import settings
openai.api_key = settings.openai
Anthropic = Anthropic(
    # This is the default and can be omitted
    api_key=settings.anthropic,
)

model = 'gpt-3.5-turbo-instruct'
max_tokens = 200
def categorize_ticket(subject, body):
    # Use OpenAI to categorize the ticket
    response = openai.completions.create(
        model = model,
        prompt=f"Categorize the following ticket:\n\nSubject: {subject}\n\nBody: {body}\n\nCategory:",
        max_tokens = max_tokens
    )
    category = response.choices[0].text.strip()
    category_confidence = 0.95  # Mock confidence for simplicity
    return category, category_confidence

def prioritize_ticket(subject, body):
    # Use OpenAI to prioritize the ticket
    response = openai.completions.create(
        model = model,
        prompt=f"Prioritize the following ticket:\n\nSubject: {subject}\n\nBody: {body}\n\nPriority:",
        max_tokens = max_tokens
    )
    priority = response.choices[0].text.strip()
    priority_confidence = 0.88  # Mock confidence for simplicity
    return priority, priority_confidence

def generate_response(subject, body):
    # Use Anthropic to generate an initial response
    response = Anthropic.messages.create(
        max_tokens=150,
        messages=[
            {
                "role": "user",
                "content": f"Categorize the following ticket:\n\nSubject: {subject}\n\nBody: {body}\n\nCategory:",
            }
        ],
        model="claude-3-opus-20240229",
    )
    return response.choices[0].text.strip()
