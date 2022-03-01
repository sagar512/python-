from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication
from django.contrib.auth import authenticate, get_user_model
from account.models import Users, Role
from django.conf import settings
import jwt


class UserTokenAuthentication(BaseAuthentication):

    def authenticate(self, request):
        # get jwt token from authorization
        authorization_token = request.headers.get("authorization", "")
        if not authorization_token:
            raise exceptions.AuthenticationFailed('No token provided.')

        try:
            decoded = jwt.decode(authorization_token,
                settings.JWT_SECURITY_TOKEN, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed('Token expired.')
        except:
            raise exceptions.AuthenticationFailed('Invalid token.')

        try:
            user = Users.objects.get(master_id=decoded.get('id'))
        except:
            raise exceptions.AuthenticationFailed('Invalid user.')

        if user.is_deleted:
            raise exceptions.AuthenticationFailed('User inactive or deleted.')

        return (user, None)

class AdminUserTokenAuthentication(BaseAuthentication):

    def authenticate(self, request):
        # get jwt token from authorization
        authorization_token = request.headers.get("authorization", "")
        if not authorization_token:
            raise exceptions.AuthenticationFailed('No token provided.')

        try:
            decoded = jwt.decode(authorization_token,
                settings.JWT_SECURITY_TOKEN, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed('Token expired.')
        except:
            raise exceptions.AuthenticationFailed('Invalid token.')

        try:
            user = Users.objects.get(master_id=decoded.get('id'),
                role=Role.objects.filter(title__iexact='admin').first())
        except:
            raise exceptions.AuthenticationFailed({'message': 'Invalid user.'})

        if user.is_deleted:
            raise exceptions.AuthenticationFailed({'message': 'User inactive or deleted.'})

        return (user, None)