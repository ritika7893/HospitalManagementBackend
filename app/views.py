
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from app.authenticate import CustomJWTAuthentication
from .models import AllUser
from .serializers import AllUserSerializer, LoginSerializer
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
