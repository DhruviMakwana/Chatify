from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField


class User(AbstractUser):
    profile_photo = models.ImageField(upload_to="profile_photo/")
    mobile_number = PhoneNumberField(unique=True)
    is_online = models.BooleanField(default=False, blank=True, null=True)
    block_user = models.ManyToManyField(
        "self", blank=True, default="", related_name="blockUser"
    )

    def __str__(self):
        return self.username


class ChatGroup(models.Model):
    name = models.CharField(max_length=30)
    created = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Chat(models.Model):
    message = models.CharField(max_length=5000, blank=True, null=True)
    sent_at = models.DateTimeField()
    client_timezone = models.CharField(max_length=50)
    group = models.ForeignKey(ChatGroup, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="messages")
    attachment = models.FileField(null=True, blank=True)
    is_deleted = models.BooleanField(default=False, blank=True)

    def __str__(self):
        return f"{self.sender.username}"
