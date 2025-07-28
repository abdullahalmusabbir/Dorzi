from django.db import models

class Embroidery(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='embroidery/', blank=True, null=True)
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.name