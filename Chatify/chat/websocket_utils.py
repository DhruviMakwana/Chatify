from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


def send_chat_message(user_id, logout, block_to, blocked_by, is_blocked):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "visiblity-group",
        {
            "type": "chat.message",
            "id": user_id,
            "logout": logout,
            "blocked_user": block_to,
            "blocked_by": blocked_by,
            "is_blocked": is_blocked,
        },
    )


def get_group_name(current_user, receiver_user):
    if current_user > receiver_user:
        return f"chat_{current_user}_{receiver_user}"
    else:
        return f"chat_{receiver_user}_{current_user}"
