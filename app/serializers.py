from rest_framework import serializers
from .models import AllUser
class AllUserSerializer(serializers.ModelSerializer):
    class Meta:
        model=AllUser
        fields='__all__'
class LoginSerializer(serializers.Serializer):
    email_or_phone = serializers.CharField(required=True)
    password = serializers.CharField(required=True)