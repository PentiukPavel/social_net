import smtplib
import ssl
from email.message import EmailMessage

from core.choices import EmailSubject
from core.config import settings


def send_email(
    subject: str,
    mail_to: str,
    template: str,
    context: dict = None,
    mail_from: str = settings.SMTP_USER,
) -> None:
    email = EmailMessage()
    email["Subject"] = subject
    email["From"] = mail_from
    email["To"] = mail_to
    with open(template) as body:
        text = body.read()
        if context:
            for k, v in context.items():
                text.format(context)
        email.set_content(text, subtype="html")

    context = ssl.create_default_context()
    with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
        server.starttls(context=context)
        server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
        server.send_message(email)


def send_invitation_by_email(mail_to: str, name: str, email: str):
    context = {
        "mame": name,
        "email": email,
    }
    send_email(
        subject=EmailSubject.INVITATION.value,
        mail_to=mail_to,
        template="templates/invitation.html",
        context=context,
    )
