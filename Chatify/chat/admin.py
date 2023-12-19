from django.contrib import admin
from .models import User, Chat, ChatGroup


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "first_name", "last_name", "profile_photo")


@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "message",
        "sent_at",
        "client_timezone",
        "group",
        "sender",
        "attachment",
        "is_deleted",
    )


@admin.register(ChatGroup)
class ChatAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "created")
