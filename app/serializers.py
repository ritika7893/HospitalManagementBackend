from rest_framework import serializers
from .models import Patient, Doctor, Admin

class PatientSerializer(serializers.ModelSerializer):
    

    class Meta:
        model = Patient
        fields = '__all__'
        read_only_fields = ['id', 'patient_id']

class DoctorSerializer(serializers.ModelSerializer):
   

    class Meta:
        model = Doctor
        fields = '__all__'
        read_only_fields = ['id', 'doctor_id']

class AdminSerializer(serializers.ModelSerializer):
    

    class Meta:
        model = Admin
        fields = '__all__'
        read_only_fields = ['id', 'admin_id']