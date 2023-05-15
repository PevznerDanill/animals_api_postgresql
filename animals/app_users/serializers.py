from djoser.serializers import UserCreateSerializer
from app_animals.models import Shelter
from rest_framework import serializers
from .models import User


class CustomUserCreateSerializer(UserCreateSerializer):
    """
    Overrides the UserCreateSerializer. Adds shelter field as required.
    """
    shelter = serializers.PrimaryKeyRelatedField(queryset=Shelter.objects.all(), required=True)

    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = 'username', 'password', 'shelter', "id"
        extra_kwargs = {
            'id': {'read_only': True}
        }


class UserShortSerializer(serializers.ModelSerializer):
    """
    A short representation of a User instance.
    """

    class Meta:
        model = User
        fields = 'username', 'id'
