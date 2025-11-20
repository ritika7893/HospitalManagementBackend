from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import AllUser

class CustomJWTAuthentication(JWTAuthentication):

    def get_user(self, validated_token):
        # Extract YOUR custom claim
        user_id = validated_token.get("user_id")

        try:
            return AllUser.objects.get(user_id=user_id)
        except AllUser.DoesNotExist:
            return None