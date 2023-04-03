import email
import imaplib
import json
import smtplib
import ssl
from email import encoders
from email.header import decode_header
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Any, Dict, Tuple

from django.core.files import File


def get_mail_credentials() -> Tuple[str]:
    with open("credentials.json") as credentials_file:
        mail_credentials = json.load(credentials_file)["mail"]
    username = mail_credentials["username"]
    password = mail_credentials["password"]
    return username, password


def send_mail_with_attachment(
    sender_address: str,
    sender_password: str,
    receiver_address: str,
    subject: str,
    body: str,
    attachment: File,
) -> bool:
    message = MIMEMultipart("alternative")
    message["Subject"] = subject
    message["From"] = sender_address
    message["To"] = receiver_address

    message.attach(MIMEText(body, "plain"))

    attachment_part = MIMEBase("application", "octet-stream")
    attachment_part.set_payload(attachment.file.read())

    encoders.encode_base64(attachment_part)
    attachment_part.add_header(
        "Content-Disposition",
        "attachment; filename=shopping_list.pdf",
    )
    message.attach(attachment_part)
    return _send_mail(sender_password, message)


def get_last_mail_content(username: str, password: str) -> Dict[str, Any]:
    mail_content = {}

    last_message = _get_last_received_mail(username, password)

    subject = _get_subject(last_message)
    mail_content["subject"] = subject

    for part in last_message.walk():
        if part.get_content_type() == "text/plain":
            body = part.get_payload(decode=True)
            mail_content["body"] = body.decode()
        elif part.get_content_disposition() == "attachment":
            mail_content["attachment"] = {}
            mail_content["attachment"]["filename"] = part.get_filename()
            mail_content["attachment"]["content"] = part.get_payload(
                decode=True
            )
    return mail_content


def _get_subject(message: email.message.Message) -> str:
    subject, encoding = decode_header(message["Subject"])[0]
    if encoding is not None:
        subject = subject.decode(encoding)
    return subject


def _get_last_received_mail(
    username: str, password: str
) -> email.message.Message:
    imap_server = imaplib.IMAP4_SSL("imap.gmail.com")
    imap_server.login(username, password)

    _, message = imap_server.select("INBOX")
    messages_nb = int(message[0])
    _, last_message = imap_server.fetch(str(messages_nb), "(RFC822)")
    return email.message_from_bytes(last_message[0][1])


def _send_mail(sender_password: str, message: MIMEMultipart) -> bool:
    sender_address = message["From"]
    receiver_address = message["To"]
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        try:
            server.login(sender_address, sender_password)
            server.sendmail(
                sender_address, receiver_address, message.as_string()
            )
        except smtplib.SMTPException as e:
            print(e)
            return False
    return True
