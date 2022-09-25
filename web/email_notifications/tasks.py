from typing import Union
from django.core.mail import EmailMultiAlternatives
from django.template import loader
from django.utils.translation import activate
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from main.decorators import smtp_shell
from src.celery import app

channel_layer = get_channel_layer()


@app.task(name='email_sender.tasks.send_information_email')
def send_information_email(
    subject: str,
    template_name: str,
    context: dict,
    to_email: Union[list[str], str],
    letter_language: str = 'en',
) -> bool:
    """
    :param subject: email subject
    :param template_name: template path to email template
    :param context: data what will be passed into email
    :param to_email: receiver email(s)
    :param letter_language: translate letter to selected lang
    :param kwargs: from_email, bcc, cc, reply_to and file_path params
    """
    activate(letter_language)
    to_email: list = [to_email] if isinstance(to_email, str) else to_email
    email_message = EmailMultiAlternatives(subject=subject,to=to_email)
    html_email: str = loader.render_to_string(template_name, context)
    email_message.attach_alternative(html_email, 'text/html')
    # TODO: нужно отослать данные на вебсокет, пробовать печатать дату и проверять как оно работает
    data = {
        "subject": "Confirmation email",
        'template_name': 'auth_app/success_registration.html',
        "to_email": to_email,
        "context": {
            "activate_url": context.get('activate_url'),
            "full_name": context.get('full_name')
        }
    }
    async_to_sync(channel_layer.group_send)(
        "notifications",
        {
            "type": "email_notification",
            "data": data,
        }
    )
    return send_email(email_message)


@smtp_shell
def send_email(email_message) -> bool:
    email_message.send()
    return True
