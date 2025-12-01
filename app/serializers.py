from rest_framework import serializers
from .models import AllUser, Department, DoctorProfile, PatientProfile


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

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model=Department
        fields='__all__'
        
class PatientProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model=PatientProfile
        fields='__all__'
        extra_kwargs = {
            "user": {"read_only": True}
        }

class DoctorProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model=DoctorProfile
        fields='__all__'
        extra_kwargs = {
            "user": {"read_only": True}
        }
class CombinedUserProfileSerializer(serializers.Serializer):
    user = AllUserSerializer()
    profile = serializers.DictField()