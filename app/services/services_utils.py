from fastapi import Depends
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema


class services_utils:
    
    conf = ConnectionConfig(
        MAIL_USERNAME = "gutierrezjaime@americana.edu.co",
        MAIL_PASSWORD = "Loscapos32635373",
        MAIL_FROM = "gutierrezjaime@americana.edu.co",
        MAIL_PORT = 587,
        MAIL_SERVER = "smtp.gmail.com",
        MAIL_STARTTLS = True,
        MAIL_SSL_TLS = False
    )

    def __init__(self):
        pass

    async def send_emails(self, 
                          subject, 
                          recipients, 
                          body):
        
        mail = FastMail(self.conf)

        message = MessageSchema(
            subject=subject,
            recipients=[recipients],  # List of recipients, as many as you can pass 
            body=body,
            subtype="plain"  # Default is plain
        )

        await mail.send_message(message, self.conf)