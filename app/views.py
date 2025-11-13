from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from django.contrib.auth.hashers import make_password
from .serializers import PatientSerializer, DoctorSerializer, AdminSerializer
from .models import AllLog, Patient, Doctor, Admin
import random

class AllRegistrationAPIView(APIView):
    def post(self, request):
        role = request.data.get('role')
        if not role:
            return Response({"success": False, "message": "Role is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            with transaction.atomic():
                # Choose serializer based on role
                if role == 'patient':
                    serializer = PatientSerializer(data=request.data)
                elif role == 'doctor':
                    serializer = DoctorSerializer(data=request.data)
                elif role == 'admin':
                    serializer = AdminSerializer(data=request.data)
                else:
                    return Response({"success": False, "message": "Invalid role"}, status=status.HTTP_400_BAD_REQUEST)

                # Validate serializer
                if not serializer.is_valid():
                    return Response({"success": False, "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

                data = serializer.validated_data
                password = data.pop('password')

                # 1️⃣ Create role-specific object first (ID generated in model save)
                if role == 'patient':
                    obj = Patient.objects.create(**data, password=make_password(password))
                    unique_id = obj.patient_id
                elif role == 'doctor':
                    obj = Doctor.objects.create(**data, password=make_password(password))
                    unique_id = obj.doctor_id
                else:  # admin
                    obj = Admin.objects.create(**data, password=make_password(password))
                    unique_id = obj.admin_id

                # 2️⃣ Create AllLog entry using the generated ID
                AllLog.objects.create(
                    unique_id=unique_id,
                    email=obj.email,
                    phone=getattr(obj, 'phone', None),
                    password=getattr(obj, 'password'),
                    role=role
                )

                return Response({
                    "success": True,
                    "message": f"{role.capitalize()} registered successfully",
                    "unique_id": unique_id
                }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({
                "success": False,
                "message": "Registration failed",
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)