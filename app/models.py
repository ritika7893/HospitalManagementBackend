from django.db import models
import random

def generate_id(prefix):
    return f"{prefix}/{random.randint(10000, 99999)}"

class AllLog(models.Model):
    id = models.AutoField(primary_key=True)
    ROLE_CHOICES = [('patient', 'Patient'), ('doctor', 'Doctor'), ('admin', 'Admin')]
    unique_id = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, unique=True, null=True, blank=True)
    password = models.CharField(max_length=128)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.role} - {self.unique_id}"


class Patient(models.Model):
    id = models.AutoField(primary_key=True)
    patient_id = models.CharField(max_length=50, unique=True, blank=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, unique=True, null=True, blank=True)
 
    role = models.CharField(max_length=10, default='patient')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(AllLog, on_delete=models.SET_NULL, to_field='unique_id', related_name='patient_created_by', null=True, blank=True)
    updated_by = models.ForeignKey(AllLog, on_delete=models.SET_NULL, to_field='unique_id', related_name='patient_updated_by', null=True, blank=True)
    created_for = models.ForeignKey(AllLog, on_delete=models.SET_NULL, to_field='unique_id', related_name='patient_created_for', null=True, blank=True)
    created_byname = models.CharField(max_length=100, null=True, blank=True)
    updated_byname = models.CharField(max_length=100, null=True, blank=True)
    def save(self, *args, **kwargs):
        if not self.unique_id:
            self.unique_id = generate_id("PAN")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.role} - {self.unique_id}"


class Doctor(models.Model):
    id = models.AutoField(primary_key=True)
    doctor_id = models.CharField(max_length=50, unique=True, blank=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, unique=True, null=True, blank=True)
    
    role = models.CharField(max_length=10, default='doctor')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(AllLog, on_delete=models.SET_NULL, to_field='unique_id', related_name='doctor_created_by', null=True, blank=True)
    updated_by = models.ForeignKey(AllLog, on_delete=models.SET_NULL, to_field='unique_id', related_name='doctor_updated_by', null=True, blank=True)
    created_byname = models.CharField(max_length=100, null=True, blank=True)
    updated_byname = models.CharField(max_length=100, null=True, blank=True)
    def save(self, *args, **kwargs):
        if not self.doctor_id:
            self.doctor_id = generate_id("DOC")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.role} - {self.doctor_id}"


class Admin(models.Model):
    id = models.AutoField(primary_key=True)
    admin_id = models.CharField(max_length=50, unique=True, blank=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, unique=True, null=True, blank=True)
   
    role = models.CharField(max_length=10, default='admin')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(AllLog, on_delete=models.SET_NULL, to_field='unique_id', related_name='admin_created_by', null=True, blank=True)
    updated_by = models.ForeignKey(AllLog, on_delete=models.SET_NULL, to_field='unique_id', related_name='admin_updated_by', null=True, blank=True)
    created_byname = models.CharField(max_length=100, null=True, blank=True)
    updated_byname = models.CharField(max_length=100, null=True, blank=True)
    def save(self, *args, **kwargs):
        if not self.admin_id:
            self.admin_id = generate_id("ADM")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.role} - {self.admin_id}"