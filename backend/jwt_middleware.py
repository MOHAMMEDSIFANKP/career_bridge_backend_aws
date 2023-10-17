from rest_framework_simplejwt.tokens import AccessToken
from rest_framework import exceptions
from api.models import User
from rest_framework.response import Response
from rest_framework import status

class JWTAuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        authorization_header = request.META.get('HTTP_AUTHORIZATION')

        if authorization_header:
            try:
                token = authorization_header.split()[1]
                access_token = AccessToken(token)
                access_token.verify()

                # Retrieve the user ID from the token payload
                user_id = access_token['user_id']

                try:
                    # Retrieve the user object from the database by ID
                    user = User.objects.get(id=user_id)  # Replace with your user model if it's custom

                    # Check if the user is active
                    if not user.is_active:
                        return Response({'detail': 'User is not activated.'}, status=status.HTTP_401_UNAUTHORIZED)

                    request.user = user
                except User.DoesNotExist:
                    # Handle the case where the user does not exist
                    pass

            except (IndexError, exceptions.AuthenticationFailed):
                pass

        response = self.get_response(request)
        return response
