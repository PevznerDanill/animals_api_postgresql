from django_filters import rest_framework as filters
from .models import Animal


class AnimalFilter(filters.FilterSet):
    """
        A filter for the AnimalListAPIView (model Animal).
        Allows to filter the list by the animal's name, id.
    """

    class Meta:
        model = Animal
        fields = 'name', 'id',

    name = filters.CharFilter(field_name='name', lookup_expr='startswith')
