from rest_framework import serializers
from .models import Shelter, Animal
from app_users.serializers import UserShortSerializer
from datetime import date


class CurrentShelterDefault(serializers.CurrentUserDefault):

    def __call__(self, serializer_field):
        return serializer_field.context['request'].user.shelter


class ShelterShortSerializer(serializers.ModelSerializer):

    class Meta:
        model = Shelter
        fields = 'id', 'title'


class AnimalListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Animal
        fields = 'id', 'name', 'shelter',

    shelter = ShelterShortSerializer()


class AnimalCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Animal
        fields = 'id', 'joined_shelter', 'name', 'age', 'height', 'weight', 'owner', 'shelter', 'distinctive_features'
        extra_kwargs = {
            'id': {'read_only': True},
            'owner': {'read_only': True},
            'shelter': {'read_only': True}
        }

    # owner = serializers.PrimaryKeyRelatedField(read_only=True)
    # shelter = serializers.PrimaryKeyRelatedField(read_only=True)



class AnimalDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Animal
        fields = 'id', 'joined_shelter', 'name', 'age', 'height', 'weight', 'owner', 'shelter', 'distinctive_features'
        extra_kwargs = {
            'owner': {'read_only': True},
            'shelter': {'read_only': True},
            'id': {'read_only': True},
        }



