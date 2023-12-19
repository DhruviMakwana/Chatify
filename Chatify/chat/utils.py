from rest_framework import serializers
from utils.messages import INVALID_PHONE_NUMBER, PHONE_NUMBER_VALUE
from django.contrib.auth import get_user_model


def validate_contact_number(mobile_number):
    if mobile_number is None:
        raise serializers.ValidationError({"phone_number": PHONE_NUMBER_VALUE})
    if 10 < len(mobile_number) <= 13:
        if mobile_number[:2] == "91":
            mobile_number = "+" + mobile_number
        elif mobile_number[:3] != "+91":
            raise serializers.ValidationError({"phone_number": INVALID_PHONE_NUMBER})
    elif len(mobile_number) == 10:
        if mobile_number[:3] == "+91":
            raise serializers.ValidationError({"phone_number": INVALID_PHONE_NUMBER})
        else:
            mobile_number = "+91" + mobile_number
    else:
        raise serializers.ValidationError({"phone_number": INVALID_PHONE_NUMBER})
    return mobile_number


def set_status(user_id, status):
    User = get_user_model()
    user = User.objects.get(id=user_id)
    user.is_online = status == "online"
    user.save()
    return user.id
