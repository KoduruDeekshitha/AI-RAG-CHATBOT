import smtplib
from email.message import EmailMessage
EMAIL="kodurudeekshitha2004@gmail.com"
APP_PASSWORD="zcvo rcfy ykza ayql"
def send_email(receiver,subject,body):
    msg=EmailMessage()
    msg["Subject"]=subject
    msg["From"]=EMAIL
    msg["To"]=receiver
    msg.set_content(body)
    with smtplib.SMTP_SSL("smtp.gmail.com",465)as smtp:
        smtp.login(EMAIL,APP_PASSWORD)
        smtp.send_message(msg)
    return "Email sent succrssfully."