from django.core.mail import EmailMultiAlternatives
from django.template import loader
from main.services import AuthorizationService
from src.celery import app


@app.task(name='update_prices')
def update_prices(**kwargs):
    users = kwargs.get('users')
    service = AuthorizationService(url='/api/v1/email-list/')
    response = service.service_response(method="post", data={"users": users})
    print(response.data, users)
    to_email: list[str] = response.data
    template_name = 'auth_app/success_registration.html'
    email_message = EmailMultiAlternatives(subject='Updated products', to=to_email)
    html_email: str = loader.render_to_string(template_name, {})
    email_message.attach_alternative(html_email, 'text/html')
    email_message.send()
