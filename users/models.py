from django.contrib.auth.models import AbstractUser,User
from django.db import models
from django.utils import timezone

# class User(AbstractUser):
#     email = models.EmailField(unique=True)
#     REQUIRED_FIELDS = ['username']
#     USERNAME_FIELD = 'email'

class FriendRequest(models.Model):
    sender = models.ForeignKey(User, related_name='sent_requests', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_requests', on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=(('pending', 'Pending'), ('accepted', 'Accepted'), ('rejected', 'Rejected')), default='pending')
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('sender', 'receiver')
