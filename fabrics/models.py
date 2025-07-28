from django.db import models

class Fabrics(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    price_per_meter = models.DecimalField(max_digits=10, decimal_places=2)
    available_stock = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Fabrics"

class FabricImage(models.Model):
    fabric = models.ForeignKey(Fabrics, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='fabrics/')

    def __str__(self):
        return f"Image for {self.fabric.name}"