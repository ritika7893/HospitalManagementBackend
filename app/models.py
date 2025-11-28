
from django.db import models


class AllUser(models.Model):
    ROLE_CHOICES = [
        ('patient', 'Patient'),
        ('doctor', 'Doctor'),
        ('admin', 'Admin')
    ]

    id = models.AutoField(primary_key=True)
    fullname=models.CharField(max_length=80,default="test")
    user_id = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, unique=True)
    password = models.CharField(max_length=128)   # Use hashing in real apps
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    gender = models.CharField(max_length=20, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user_status = models.CharField(max_length=20, default='active')
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"{self.role} - {self.user_id}"

    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False


class Department(models.Model):
    name = models.CharField(unique=True, max_length=40)
    description = models.TextField()

    def __str__(self):
        return self.name
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class DoctorProfile(models.Model):
   
    user = models.OneToOneField(AllUser, on_delete=models.CASCADE, to_field='user_id')
    department=models.ForeignKey(Department,on_delete=models.CASCADE)
    consulting_fee = models.DecimalField(max_digits=10, decimal_places=2)
    qualification = models.CharField(max_length=40)
    timing = models.TimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"Doctor: {self.user.user_id}"


class PatientProfile(models.Model):
   
    user = models.OneToOneField(AllUser, on_delete=models.CASCADE, to_field='user_id')
    age = models.PositiveIntegerField()
    address = models.TextField()
    blood_group = models.CharField(max_length=20)
    medical_history_notes = models.TextField()
    emergency_contactno = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"Patient: {self.user.user_id}"
