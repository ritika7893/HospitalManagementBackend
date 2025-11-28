
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from app.authenticate import CustomJWTAuthentication
from .models import AllUser, Department, DoctorProfile, PatientProfile
from .serializers import AllUserSerializer, DepartmentSerializer, DoctorProfileSerializer, ForgetPasswordSerializer, LoginSerializer, PatientProfileSerializer
from .utils import generate_id
from rest_framework.permissions import IsAuthenticated   # your function
from django.contrib.auth.hashers import make_password,check_password
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
class AllRegistrationAPIView(APIView):

    def post(self, request):
        role = request.data.get("role")
        password=request.data.get("password")
        if not role:
            return Response({"error": "role is required"}, status=400)

        # prefix based on role
        prefix_map = {
            "patient": "PAN",
            "doctor": "DOC",
            "admin": "ADM"
        }

        if role not in prefix_map:
            return Response({"error": "Invalid role"}, status=400)

        prefix = prefix_map[role]
        user_id = generate_id(prefix)
        data = request.data.copy()
        data["user_id"] = user_id
        data["password"] = make_password(data["password"])

        serializer = AllUserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message":"user created successfull"}, status=201)
        return Response(serializer.errors, status=400)
class LoginAPIView(APIView):
    
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email_or_phone = serializer.validated_data["email_or_phone"]
        password = serializer.validated_data["password"]

        # Find user by email OR phone
        user = AllUser.objects.filter(email=email_or_phone).first()

        if not user:
            user = AllUser.objects.filter(phone=email_or_phone).first()

        if not user:
            return Response({"error": "Invalid login details"}, status=401)

        # Check password for both email and phone cases
        if not check_password(password, user.password):
            return Response({"error": "Invalid password"}, status=401)

        # Generate token
        refresh = RefreshToken.for_user(user)
        refresh['user_id'] = user.user_id
        refresh['email'] = user.email
        refresh['role'] = user.role

        access = refresh.access_token

        return Response(
            {
                "message": "Login successful",
                "access": str(access),
                "refresh": str(refresh),
                "user": {
                    "user_id": user.user_id,
                    "email": user.email,
                    "role": user.role,
                    "phone": user.phone,
                    "gender": user.gender
                }
            },
            status=status.HTTP_200_OK
        )
class UserDetailAPIView(APIView):
    
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        # Because your CustomJWTAuthentication already returns AllUser
        user = request.user  

        if user is None:
            return Response({"error": "Invalid token"}, status=401)

        serializer = AllUserSerializer(user)
        return Response({"user": serializer.data}, status=200)
class RefreshTokenAPIView(APIView):
    def post(self, request):
        refresh_token = request.data.get("refresh")

        if not refresh_token:
            return Response({"error": "Refresh token is required"}, status=400)

        try:
            refresh = RefreshToken(refresh_token)

            # Read existing claims
            user_id = refresh.get("user_id")
            email = refresh.get("email")
            role = refresh.get("role")

            # Generate new access token
            access = refresh.access_token

            # Re-add custom claims into new access token
            access["user_id"] = user_id
            access["email"] = email
            access["role"] = role

            return Response({
                "access": str(access)
            }, status=200)

        except TokenError:
            return Response({"error": "Invalid or expired refresh token"}, status=401)

class ChangePasswordAPIView(APIView):

    def post(self, request):
        serializer = ForgetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email_or_phone = serializer.validated_data["email_or_phone"]
        new_password = serializer.validated_data["new_password"]

        # Find user by email or phone
        user = AllUser.objects.filter(email=email_or_phone).first() \
            or AllUser.objects.filter(phone=email_or_phone).first()

        if not user:
            return Response({"error": "User not found"}, status=404)

        # Set new password
        user.password = make_password(new_password)
        user.save()

        return Response(
            {"message": "Password reset successful"},
            status=200
        )
class CreateProfileAPIView(APIView):
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):

        user = request.user   # Comes from token

        # --- Check Role ---
        if user.role not in ["doctor", "patient"]:
            return Response(
                {"error": "Only doctor or patient can create a profile"},
                status=403
            )

        # --- Doctor Profile ---
        if user.role == "doctor":
            
            if DoctorProfile.objects.filter(user=user.user_id).exists():
                return Response({"error": "Doctor profile already exists"}, status=400)

            serializer = DoctorProfileSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(user=user)   # Assign logged-in user
                return Response(
                    {"message": "Doctor profile created", "profile": serializer.data},
                    status=201
                )
            return Response(serializer.errors, status=400)

        # --- Patient Profile ---
        if user.role == "patient":

            if PatientProfile.objects.filter(user=user.user_id).exists():
                return Response({"error": "Patient profile already exists"}, status=400)

            serializer = PatientProfileSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(user=user)
                return Response(
                    {"message": "Patient profile created", "profile": serializer.data},
                    status=201
                )
            return Response(serializer.errors, status=400)
class DepartmentListAPIView(APIView):
    def post(self,request):
        serializer=DepartmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message":"Department created successfully"},status=201)
        return Response(serializer.errors,status=400)
    def get(self,request):
        departments=Department.objects.all()
        serializer=DepartmentSerializer(departments,many=True)
        return Response({"departments":serializer.data},status=200)
    def delete(self,request):
        id=request.data.get("id")
        try:    
            department=Department.objects.get(id=id)
            department.delete()
            return Response({"message":"Department deleted successfully"},status=200)   
        except Department.DoesNotExist:
            return Response({"error":"Department not found"},status=404)
    def put(self,request):
        id=request.data.get("id")
        try:
            department=Department.objects.get(id=id)
        except Department.DoesNotExist:
            return Response({"error":"Department not found"},status=404)
        serializer=DepartmentSerializer(department,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message":"Department updated successfully"},status=200)
        return Response(serializer.errors,status=400)