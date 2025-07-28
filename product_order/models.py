from django.db import models
from django.contrib.auth.models import User
from tailor.models import *
from pre_designed.models import *
from reviews.models import *

class Order(models.Model):
    SIZE_CHOICES = [
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
        ('XL', 'Extra Large'),
        ('XXL', 'Double Extra Large'),
    ]
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='porder') 
    tailor = models.ForeignKey(Tailor, on_delete=models.CASCADE, related_name='porder', default=None)  
    predesigned = models.ForeignKey(Predesigned, on_delete=models.CASCADE, related_name='porder')  
    quantity = models.IntegerField()  
    price = models.DecimalField(max_digits=10, decimal_places=2)  
    order_date = models.DateTimeField(auto_now_add=True) 
    delivery_date = models.DateField(null=True, blank=True)  
    address = models.TextField()  
    number = models.CharField(max_length=11, default=None)  
    size = models.CharField(max_length=4, choices=SIZE_CHOICES, default='S')  
    review = models.ForeignKey(Review, on_delete=models.SET_NULL, related_name='porder', null=True, blank=True)  
    status = models.CharField(max_length=20, default='pending')  


    def __str__(self):
        return f"Order #{self.id} - {self.buyer.username} ({self.predesigned.name})"
