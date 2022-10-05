from django.conf import settings
from microservice_request.services import ConnectionService


class AuthorizationService(ConnectionService):
    api_key = settings.AUTHORIZATION_API_KEY
    service = settings.AUTHORIZATION_API_URL
