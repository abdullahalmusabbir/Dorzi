from django.db import models
from django.contrib.auth.models import User

class Complain(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='complains')
    subject = models.CharField(max_length=255)
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)
    is_resolved = models.BooleanField(default=False)
    response = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Complain by {self.user.username}: {self.subject}"