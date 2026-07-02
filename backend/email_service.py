import os
import resend
from dotenv import load_dotenv
load_dotenv()
resend.api_key=os.getenv("RESEND_API_KEY")
def send_email(receiver,subject,body):
    response=resend.Emails.send({
        "from": "Deekshitha AI <onboarding@resend.dev>",
        "to":receiver,
        "subject":subject,
        "html":body
    })
    return response