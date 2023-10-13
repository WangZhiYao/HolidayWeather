import logging
import smtplib
from email.mime.text import MIMEText

from config import settings
from model import Message
from push.push_api import PushApi


class EmailPush(PushApi):

    def send_push(self, message: Message) -> bool:
        logging.info('Pushing message...')
        msg = MIMEText(message.content)
        msg['Subject'] = message.title
        msg['From'] = settings.smtp.sender
        receiver = settings.smtp.sender
        if settings.smtp.receiver:
            receiver = settings.smtp.receiver
        msg['To'] = receiver
        try:
            with smtplib.SMTP_SSL(settings.smtp.host, settings.smtp.port) as smtp:
                smtp.login(settings.smtp.sender, settings.smtp.password)
                smtp.send_message(msg)
                return True
        except Exception as ex:
            logging.error(ex)
            return False
