from channels.layers import get_channel_layer
from django.conf import settings
from twilio.rest import Client

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
