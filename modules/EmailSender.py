import smtplib, ssl
import re
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class EmailService:

    def __init__(
                    self, 
                    html,
                    ssl_server,
                    port
                ):
        self.port = port
        self.ssl_server = ssl_server
        self.html = html

    def change_variables(self, variable,value):
        self.html = self.html.replace(r"{{"+re.escape(variable)+r"}}",value)
    

    def send_email( self, sender_email, receiver_email, password, subject ):
        message = MIMEMultipart("alternative")
        message["Subject"] = subject
        message["From"] = sender_email
        message["To"] = receiver_email
        message.attach(MIMEText(self.html, "html"))
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(self.ssl_server, self.port, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(
                sender_email, receiver_email, message.as_string()
            )