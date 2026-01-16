from rest_framework.permissions import BasePermission
from rest_framework.permissions import IsAuthenticated
from .authenticate import CustomJWTAuthentication
class IsAdminUser(BasePermission):
    def has_permission(self, request, view):
        user=request.user
        if user and user.is_authenticated and user.role=='admin':
            return True
        return False
class IsDoctorUser(BasePermission):
    def has_premission(self,request,view):
        user=request.user
        if user and user.is_authenticated and user.role=='doctor':
            return True
        return False

class IsPatientUser(BasePermission):
    def has_permission(self,request,view):
        user=request.user
        if user and user.is_authenticated and user.role=="patient":
            return True
        return False