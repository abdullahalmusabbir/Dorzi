from django.db import models
from tailor.models import *
from pre_designed.models import *
from django.contrib.auth.models import User

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')  
    tailor = models.ForeignKey(Tailor, on_delete=models.CASCADE, related_name='tailor_reviews')  
    predesigned = models.ForeignKey(Predesigned, on_delete=models.CASCADE, related_name='predesigned_reviews')  
    rating = models.IntegerField()  
    comment = models.CharField(max_length=1024,default=None)  
    timestamp = models.DateTimeField(auto_now_add=True)  

    class Meta:
        unique_together = ('user', 'predesigned')  

    def save(self, *args, **kwargs):
        if self.rating < 1 or self.rating > 5:
            raise ValueError("Rating must be between 1 and 5.")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Review by {self.user.username} on {self.predesigned.name} - {self.rating}/5"
