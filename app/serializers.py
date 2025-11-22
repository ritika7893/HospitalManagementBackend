from rest_framework import serializers
from .models import AllUser, DoctorProfile, PatientProfile


class AllUserSerializer(serializers.ModelSerializer):
    class Meta:
        model=AllUser
        fields='__all__'

class LoginSerializer(serializers.Serializer):
    email_or_phone = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

class ForgetPasswordSerializer(serializers.Serializer):
    email_or_phone = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

class PatientProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model=PatientProfile
        fields='__all__'

class DoctorProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model=DoctorProfile
        fields='__all__'