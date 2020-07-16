import os
import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart


class EmailSender:
    """This class sends email to user

        Parameters
        ---------------
        sender_name: str - your email nick(vJoe123)
        email_name: str - yours mail(gmail.com)
        sender_password:str - password for your email
        recipients_email: list - emails of recipients"""

    def __init__(self, sender_name: str, email_name: str, sender_password: str, recipients_email: list) -> None:
        self.sender_email = sender_name + '@' + email_name
        self.sender_password = sender_password
        self.recipients_email = recipients_email
        self.email = email_name
        self.outer = MIMEMultipart()
        self.outer['To'] = ', '.join(self.recipients_email)
        self.outer['From'] = self.sender_email

    def attach_file(self, file_path: str) -> None:
        """Attach your file into email.
        Parameters
        --------------
        file_path: str """

        with open(file_path, 'rb') as file:
            msg = MIMEBase('application', "octet-stream")
            msg.set_payload(file.read())

        encoders.encode_base64(msg)
        msg.add_header('Content-Disposition', 'attachment', filename=os.path.basename(file_path))
        self.outer.attach(msg)
        self.outer.as_string()

    def send(self, subject: str, msg=None, file: str = None) -> None:
        """send your message into user

        Parameters
        ---------------
        subject: str - subject your email
        msg: str (default None) - message
        file:str (default None) - path into file"""

        self.outer['Subject'] = subject

        with smtplib.SMTP(f'smtp.{self.email}', 587) as s:
            s.ehlo()
            s.starttls()
            s.ehlo()
            s.login(self.sender_email, self.sender_password)
            if file:
                self.attach_file(file)
                s.sendmail(self.sender_email, self.recipients_email, self.outer.as_string())
            else:
                s.sendmail(self.sender_email, self.recipients_email, msg)
            s.close()

