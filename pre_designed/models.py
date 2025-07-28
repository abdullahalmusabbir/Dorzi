from django.db import models
from tailor.models import Category, Tailor
from django.contrib.auth.models import User

class Predesigned(models.Model):
    name = models.CharField(max_length=225)
    description = models.TextField()
    availability = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    tailor = models.ForeignKey(Tailor, on_delete=models.CASCADE, related_name='predesigned_Tailor')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    orders = models.IntegerField(default=0)
    popularity = models.IntegerField(default=0)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name

class ProductImage(models.Model):
    product = models.ForeignKey(Predesigned, on_delete=models.CASCADE, related_name="product_images")  
    image = models.ImageField(upload_to='photos/')

    def __str__(self):
        return f"Image for {self.product.name}"

