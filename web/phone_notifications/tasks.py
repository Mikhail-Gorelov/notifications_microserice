from typing import Union

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template import loader
from django.utils.translation import activate
import asyncio
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from twilio.rest import Client

from main.decorators import smtp_shell
from src.celery import app

channel_layer = get_channel_layer()


@app.task(name='sms_sender.tasks.send_information_sms')
def send_information_sms(
    body: str,
    to: str,
) -> bool:
    """
    :param body: sms body
    :param to: data what will be passed into email
    """
    account_sid = settings.TWILIO_ACCOUNT_SID
    auth_token = settings.TWILIO_AUTH_TOKEN
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        body=body,
        from_=settings.TWILIO_PHONE_NUMBER,
        to=to
    )
    return message.sid
