from django.db import models
from tailor.models import Tailor
from pre_designed.models import PreDesigned
from customer.models import Customer

class Reviews(models.Model):
    customer = models.ForeignKey(
        Customer, 
        on_delete=models.CASCADE, 
        related_name='reviews'
    )  # Reviewer (Buyer)

    tailor = models.ForeignKey(
        Tailor, 
        on_delete=models.CASCADE, 
        related_name='tailor_reviews'
    )  

    product = models.ForeignKey(
        PreDesigned, 
        on_delete=models.CASCADE, 
        related_name='dress_reviews',
        null=True, 
        blank=True
    )

    rating = models.IntegerField()  
    comment = models.TextField(blank=True, null=True)  
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('customer', 'product')  

    def save(self, *args, **kwargs):
        if self.rating < 1 or self.rating > 5:
            raise ValueError("Rating must be between 1 and 5.")
        super().save(*args, **kwargs)

    def __str__(self):
        if self.product:
            return f"Review by {self.customer.username} on {self.product.title} - {self.rating}/5"
        return f"Review by {self.customer.username} on {self.tailor.user.username} - {self.rating}/5"
    def get_rating_display(self):
        return f"{self.rating} out of 5 stars"
