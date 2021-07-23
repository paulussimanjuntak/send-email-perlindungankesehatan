from fastapi import FastAPI, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from config import SendEmailSchema, settings
from libs.MailSmtp import send_email

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post('/send-email',
    responses={
        200: {
            "description": "Successful Response",
            "content": {"application/json":{"example": {"detail":"Pesan telah terkirim."}}}
        }
    }
)
async def send_email_consult(data: SendEmailSchema, background_tasks: BackgroundTasks):
    background_tasks.add_task(send_email,
        [settings.email_receiver],
        'Permintaan Konsultasi dari {}'.format(data.name),
        'dont-reply',
        'SendEmail.html',
        **data.dict()
    )
    return {"message": "Pesan telah terkirim."}
