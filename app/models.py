from django.db import models
import random



class AllUser(models.Model):
    id = models.AutoField(primary_key=True)
    ROLE_CHOICES = [('patient', 'Patient'), ('doctor', 'Doctor'), ('admin', 'Admin')]
    user_id = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True,null=False,blank=False)
    phone = models.CharField(max_length=15, unique=True, null=False,blank=False)
    password = models.CharField(max_length=128)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    gender=models.CharField(max_length=20,blank=False,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user_status=models.CharField(max_length=20,default='active')
    is_active = models.BooleanField(default=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    def __str__(self):
        return f"{self.name} ({self.email})"
    
    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def __str__(self):
        return f"{self.role} - {self.user_id}"

