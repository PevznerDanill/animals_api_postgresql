from django.http import HttpRequest
from rest_framework.generics import (
    ListAPIView,
    CreateAPIView,
    RetrieveUpdateDestroyAPIView
)
from .serializers import (
    AnimalListSerializer,
    ShelterShortSerializer,
    AnimalCreateSerializer,
    AnimalDetailSerializer
)
from rest_framework import permissions
from rest_framework import status
from rest_framework.response import Response
from .models import Animal, Shelter
from .permissions import NotGuest, IsValidShelter, IsOwnerOrReadOnly
from django.core.exceptions import ValidationError
from collections import OrderedDict
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from .filters import AnimalFilter
from django.db.models import QuerySet


class AnimalListAPIView(ListAPIView):
    """
    An API View to display the list of Animal instances.
    """
    serializer_class = AnimalListSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = AnimalFilter
    search_fields = ['^name', 'id']
    ordering_fields = ['name', 'id']

    def get_queryset(self) -> QuerySet:
        """
        Returns a queryset with Animal instances.
        """
        cur_user = self.request.user
        if cur_user.is_superuser:
            return Animal.objects.select_related('shelter').filter(is_archived=False)
        return Animal.objects.select_related('shelter').filter(shelter=cur_user.shelter, is_archived=False)


class AnimalCreateAPIView(CreateAPIView):
    """
    An APIView for the creation of a new Animal instance.
    """
    serializer_class = AnimalCreateSerializer
    permission_classes = [permissions.IsAuthenticated, NotGuest]

    def create(self, request: HttpRequest, *args, **kwargs) -> Response:
        """
        Overrides the default self.create() method.
        Adds the User (stored in request.user) and Shelter (field of the User) instances to the
        validated data.
        Perfoms additional validation of the new object when it is being saved in the database.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data.update(
            {
                'owner': request.user,
                'shelter': request.user.shelter
            }
        )
        try:
            self.perform_create(serializer)
            data = serializer.data
            response_status = status.HTTP_201_CREATED
        except ValidationError as exc:
            data = OrderedDict(exc)
            response_status = status.HTTP_400_BAD_REQUEST

        headers = self.get_success_headers(data)
        return Response(data, status=response_status, headers=headers)


class ShelterListAPIView(ListAPIView):
    """
    An API View for displaying of the list of Shelter instances.
    """

    serializer_class = ShelterShortSerializer
    queryset = Shelter.objects.all()
    filter_backends = [filters.SearchFilter, DjangoFilterBackend, filters.OrderingFilter]
    search_fields = 'id', '^title',
    ordering_fields = 'id',
    filterset_fields = 'id', 'title',


class AnimalDetailAPIView(RetrieveUpdateDestroyAPIView):
    """
    An API View to Retrieve, Update, or Destroy an Animal instance.
    """
    serializer_class = AnimalDetailSerializer
    queryset = (
        Animal.objects.select_related('shelter', 'owner').filter(is_archived=False)
    )
    permission_classes = [permissions.IsAuthenticated, IsValidShelter, IsOwnerOrReadOnly]

    def delete(self, request: HttpRequest, *args, **kwargs) -> Response:
        """
        Sets the is_archived flag of the retrieved Animal instance to True.
        """
        instance = self.get_object()
        instance.is_archived = True
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def update(self, request: HttpRequest, *args, **kwargs) -> Response:
        """
        Overrides the default update method.
        Performs an additional validation when saving the retrieved instance.
        """
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        try:
            self.perform_update(serializer)
            data = serializer.data
            response_status = status.HTTP_200_OK
        except ValidationError as exc:
            data = OrderedDict(exc)
            response_status = status.HTTP_400_BAD_REQUEST
        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return Response(data=data, status=response_status)





