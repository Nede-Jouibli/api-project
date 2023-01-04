from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from dotenv import dotenv_values
from pydantic import BaseModel, EmailStr
from typing import List
from .models import Citizen
import jwt



config_credentials = dotenv_values(".env")

conf = ConnectionConfig(
    MAIL_USERNAME = config_credentials["MAIL_USERNAME"],
    MAIL_PASSWORD = config_credentials["MAIL_PASSWORD"],
    MAIL_FROM = config_credentials["MAIL_USERNAME"],
    MAIL_PORT = 587,
    MAIL_SERVER = "smpt.gmail.com",
    MAIL_STARTTLS = False,
    MAIL_SSL_TLS = True,
    USE_CREDENTIALS = True,
    #VALIDATE_CERTS = True
)

class EmailSchema (BaseModel):
    email: List[EmailStr]

def send_email(email: EmailSchema, instance: Citizen):
    token_data = { "id" : Citizen.id,
                    "email": Citizen.email
                }
    token=jwt.encode(token_data, config_credentials["SECRET"] )            

    template = f"""
        <!DOCTYPE html>
        <html>
        <head>
        </head>
        <body>
            <div style=" display: flex; align-items: center; justify-content: center; flex-direction: column;">
                <h3> Account Verification </h3>
                <br>
                <p>Thanks for choosing EasyShopas, please 
                click on the link below to verify your account</p> 
                <a style="margin-top:1rem; padding: 1rem; border-radius: 0.5rem; font-size: 1rem; text-decoration: none; background: #0275d8; color: white;"
                 href="http://localhost:8000/verification/?token={token}">
                    Verify your email
                <a>
                <p style="margin-top:1rem;">If you did not register for EasyShopas, 
                please kindly ignore this email and nothing will happen. Thanks<p>
            </div>
        </body>
        </html>
    """
    message = MessageSchema(
        subject= "TunInvest Account Verification Email",
        recipients= email, #list
        body = template,
        subtype="html")
    
    fm = FastMail(conf)
    fm.send_message(message=message)

# from typing import List
# from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
# from pydantic import EmailStr, BaseModel
# from .config import settings
# from jinja2 import Environment, select_autoescape, PackageLoader


# env = Environment(
#     loader=PackageLoader('app', 'templates'),
#     autoescape=select_autoescape(['html', 'xml'])
# )


# class EmailSchema(BaseModel):
#     email: List[EmailStr]


# class Email:
#     def __init__(self, user: dict, url: str, email: List[EmailStr]):
#         self.name = user['name']
#         self.sender = 'Codevo <admin@admin.com>'
#         self.email = email
#         self.url = url
#         pass

#     async def sendMail(self, subject, template):
#         # Define the config
#         conf = ConnectionConfig(
#             MAIL_USERNAME=settings.EMAIL_USERNAME,
#             MAIL_PASSWORD=settings.EMAIL_PASSWORD,
#             MAIL_FROM=settings.EMAIL_FROM,
#             MAIL_PORT=settings.EMAIL_PORT,
#             MAIL_SERVER=settings.EMAIL_HOST,
#             MAIL_STARTTLS=False,
#             MAIL_SSL_TLS=False,
#             USE_CREDENTIALS=True,
#             VALIDATE_CERTS=True
#         )
#         # Generate the HTML template base on the template name
#         template = env.get_template(f'{template}.html')

#         html = template.render(
#             url=self.url,
#             first_name=self.name,
#             subject=subject
#         )

#         # Define the message options
#         message = MessageSchema(
#             subject=subject,
#             recipients=self.email,
#             body=html,
#             subtype="html"
#         )

#         # Send the email
#         fm = FastMail(conf)
#         await fm.send_message(message)

#     async def sendVerificationCode(self):
#         await self.sendMail('Your verification code (Valid for 10min)', 'verification')

