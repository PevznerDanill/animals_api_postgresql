from djoser.serializers import UserCreateSerializer
from app_animals.models import Shelter
from rest_framework import serializers
from .models import User


class CustomUserCreateSerializer(UserCreateSerializer):
    shelter = serializers.PrimaryKeyRelatedField(queryset=Shelter.objects.all(), required=True)

    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = 'username', 'password', 'shelter',


class UserShortSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = 'username', 'id'
