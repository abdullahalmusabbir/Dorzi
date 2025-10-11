from django.db import models
from django.contrib.auth.models import User


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='customer',null=True, blank=True)
    
    chest = models.CharField(max_length=10, blank=True, null=True)
    waist = models.CharField(max_length=10, blank=True, null=True)
    hip = models.CharField(max_length=10, blank=True, null=True)
    shoulder = models.CharField(max_length=10, blank=True, null=True)
    sleeve = models.CharField(max_length=10, blank=True, null=True)
    neck = models.CharField(max_length=10, blank=True, null=True)
    length = models.CharField(max_length=10, blank=True, null=True)
    inseam = models.CharField(max_length=10, blank=True, null=True)

    phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to="customer_profiles/", blank=True, null=True)
    

    def __str__(self):
        return self.user.username
