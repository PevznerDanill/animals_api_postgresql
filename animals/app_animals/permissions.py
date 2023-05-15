from rest_framework.permissions import BasePermission, SAFE_METHODS
from django.http import HttpRequest
from rest_framework.views import View
from .models import Animal
from rest_framework import permissions


class NotGuest(BasePermission):
    """
    Checks the status of the user. Is a guest and not superuser, returns False
    """

    def has_permission(self, request: HttpRequest, view: View) -> bool:

        return not request.user.is_guest or request.user.is_superuser


class IsValidShelter(BasePermission):
    """
    Checks if the user belongs to the same shelter as the retrieved Animal instance.
    If not and not superuser, returns False.
    """

    def has_object_permission(self, request: HttpRequest, view: View, obj: Animal) -> bool:

        return obj.shelter == request.user.shelter or request.user.is_superuser


class IsOwnerOrReadOnly(BasePermission):
    """
    Checks if the user is the owner of the retrieved Animal instance.
    If not, only safe methods are allowed.
    """
    def has_object_permission(self, request, view, obj):

        if request.method in permissions.SAFE_METHODS:
            return True

        return (obj.owner == request.user and not request.user.is_guest) or request.user.is_superuser
