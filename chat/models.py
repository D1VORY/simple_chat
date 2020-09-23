from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Message(models.Model):
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="messages")

    class Meta:
        verbose_name = "Message"
        verbose_name_plural = "Messages"

    def __str__(self):
        return self.text[:30]

    def __repr__(self):
        return self.__str__()
