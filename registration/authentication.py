from django.conf import settings
from rest_framework import exceptions
from rest_framework import authentication


class KeyAuth(authentication.BaseAuthentication):
    """
    Custom authentication class according to Header Token
    """
    api_keys = (settings.CLIENT_API_KEY,
                )

    def authenticate(self, request):

        try:
            incoming_api_key = request.META['HTTP_APIKEY']
        except (AttributeError, KeyError):  # Missing Authorization Header
            raise exceptions.AuthenticationFailed('Unauthorised')
        else:
            if incoming_api_key not in self.api_keys:
                raise exceptions.AuthenticationFailed()
            else:
                return None, incoming_api_key
