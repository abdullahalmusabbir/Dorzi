from django.db import models
from django.contrib.auth.models import User
from pre_designed.models import Predesigned

class FavoriteDress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorite_dresses')
    dress = models.ForeignKey(Predesigned, on_delete=models.CASCADE, related_name='favorited_by')
    added_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} favorited {self.dress.name}"