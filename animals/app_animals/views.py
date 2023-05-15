from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView, ListAPIView, CreateAPIView, RetrieveUpdateDestroyAPIView
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
from rest_framework.exceptions import PermissionDenied
from .permissions import NotGuest, IsValidShelter, IsOwnerOrReadOnly
from django.core.exceptions import ValidationError
from collections import OrderedDict


class AnimalListAPIView(ListAPIView):
    serializer_class = AnimalListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        cur_user = self.request.user
        if cur_user.is_superuser:
            return Animal.objects.select_related('owner', 'shelter').filter(is_archived=False)
        return Animal.objects.select_related('owner', 'shelter').filter(shelter=cur_user.shelter, is_archived=False)


class AnimalCreateAPIView(CreateAPIView):
    serializer_class = AnimalCreateSerializer
    permission_classes = [permissions.IsAuthenticated, NotGuest]


    def create(self, request, *args, **kwargs):
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
    serializer_class = ShelterShortSerializer
    queryset = Shelter.objects.all()


class AnimalDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = AnimalDetailSerializer
    queryset = (
        Animal.objects.select_related('shelter', 'owner').filter(is_archived=False)
    )
    permission_classes = [permissions.IsAuthenticated, NotGuest, IsValidShelter, IsOwnerOrReadOnly]

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_archived = True
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def update(self, request, *args, **kwargs):
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





