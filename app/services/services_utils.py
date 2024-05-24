from fastapi import Depends
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema
import os
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

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

    def login_to_google_drive(self):
        current_dir = os.path.dirname(os.path.realpath(__file__))
        client_secrets_path = os.path.abspath(os.path.join(current_dir, '../../client_secret.json'))
        credentials_path = os.path.abspath(os.path.join(current_dir, '../../credentials.json'))

        gauth = GoogleAuth()
        gauth.LoadClientConfigFile(client_secrets_path)

        # Try to load saved credentials from the file.
        if os.path.exists(credentials_path):
            try:
                gauth.LoadCredentialsFile(credentials_path)
            except:
                print("Failed to refresh the token")
                return None

        # If no valid credentials were loaded, authenticate.
        if gauth.credentials is None:
            gauth.LocalWebserverAuth()

        # Save the current credentials to a file for future use.
        gauth.SaveCredentialsFile(credentials_path)

        return GoogleDrive(gauth)