import codecs
import re
import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from .emailattachment import EmailAttachment


class EmailSender:
    def __init__(self, smtp_server: str):
        self.attempts = 0
        self.smtp_server_string = smtp_server
        self._start_server()

    def _start_server(self):
        self.smtp_server = smtplib.SMTP(self.smtp_server_string)
        self.smtp_server.ehlo()
        self.smtp_server.starttls()

    @staticmethod
    def create_email(to_field: str, subject: str, html_body: str, images=None,
                     attachments=None):
        """
        Creates a message to be sent.

        The to_field has no influence over who the email is going to, so you can use
        it to name a group (e.g. to: Everyone but Carl).
        """
        if images is None:
            images = []

        if attachments is None:
            attachments = []

        msg = MIMEMultipart('related')
        msg['To'] = to_field
        msg['Subject'] = subject
        if html_body:
            msg.attach(MIMEText(html_body, 'html'))

        for image in images:
            with open(image.file_path, 'rb') as fp:
                img = MIMEImage(fp.read())
                img.add_header('Content-ID', image.email_tag)
            msg.attach(img)

        for attachment in attachments:
            with open(attachment.file_path, 'rb') as fp:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(fp.read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', f'attachment; filename="{attachment.title}"')
            msg.attach(part)

        return msg

    @staticmethod
    def html_body_from_file(file_path: str):
        """Returns the contents of a linked HTML file."""
        return codecs.open(filename=file_path, encoding='utf8').read()

    def send(self, message, from_addr: str, to_addrs: [str]):
        """Sends the email. If there are more than 200 email addresses then it batches them. If error,
        it re-authenticates which resolves 99.9% of the errors. """
        for emails in range(0, len(to_addrs), 200):
            try:
                self.smtp_server.sendmail(from_addr=from_addr,
                                          to_addrs=to_addrs,
                                          msg=message.as_string())
            except:
                if self.attempts >= 10:
                    raise ConnectionError  # Don't want a infinite loop if it keeps failing.
                self.attempts += 1

                self._start_server()
                self.send(message=message,
                          from_addr=from_addr,
                          to_addrs=to_addrs[to_addrs.index(emails[0]):])

    @staticmethod
    def validate_email_addresses(email_addr: [str]):
        """Validates a list of email addresses."""
        email_valid = {}
        for email in email_addr:
            email_valid[email] = True if re.match(f'[^@ \t\r\n]+@[^@ \t\r\n]+\.[^@ \t\r\n]+', email) else False
        return email_valid

    def __del__(self):
        self.smtp_server.close()
