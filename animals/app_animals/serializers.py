from rest_framework import serializers
from .models import Shelter, Animal


class CurrentShelterDefault(serializers.CurrentUserDefault):
    """
    Creates a current serializer value for User.shelter field.
    """

    def __call__(self, serializer_field):
        return serializer_field.context['request'].user.shelter


class ShelterShortSerializer(serializers.ModelSerializer):
    """
    A serializer for the short information about the shelter.
    Used in AnimalListSerializer and ShelterListAPIView.
    """

    class Meta:
        model = Shelter
        fields = 'id', 'title'


class AnimalListSerializer(serializers.ModelSerializer):
    """
    A serializer for the representation of an object in a list of Animal instances.
    Used in AnimalListAPIView.
    """

    class Meta:
        model = Animal
        fields = 'id', 'name', 'shelter',

    shelter = ShelterShortSerializer()


class AnimalCreateSerializer(serializers.ModelSerializer):
    """
    A serializer for the creation of a new Animal instance.
    """

    class Meta:
        model = Animal
        fields = 'id', 'joined_shelter', 'name', 'age', 'height', 'weight', 'owner', 'shelter', 'distinctive_features'
        extra_kwargs = {
            'id': {'read_only': True},
            'owner': {'read_only': True},
            'shelter': {'read_only': True}
        }


class AnimalDetailSerializer(serializers.ModelSerializer):
    """
    A serializer for the detail representation of the retrieved Animal instance.
    """

    class Meta:
        model = Animal
        fields = 'id', 'joined_shelter', 'name', 'age', 'height', 'weight', 'owner', 'shelter', 'distinctive_features'
        extra_kwargs = {
            'owner': {'read_only': True},
            'shelter': {'read_only': True},
            'id': {'read_only': True},
        }



