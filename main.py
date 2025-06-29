from fastapi import FastAPI
from app.web.api.email_webhook import router as email_webhook_router

app = FastAPI(title="Email Webhook MVP", version="1.0")

# Incluir el router del webhook
app.include_router(email_webhook_router)

@app.get("/")
def root():
    return {"status": "ok", "message": "Email Webhook MVP is running"} 