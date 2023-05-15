from rest_framework.permissions import BasePermission, SAFE_METHODS
from app_users.models import User
from django.http import HttpRequest
from rest_framework.views import View
from .models import Animal
from rest_framework import permissions


class NotGuest(BasePermission):

    def has_permission(self, request: HttpRequest, view: View) -> bool:

        return not request.user.is_guest or request.user.is_superuser


class IsValidShelter(BasePermission):

    def has_object_permission(self, request: HttpRequest, view: View, obj: Animal) -> bool:

        return obj.shelter == request.user.shelter or request.user.is_superuser


class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):

        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.owner == request.user or request.user.is_superuser
