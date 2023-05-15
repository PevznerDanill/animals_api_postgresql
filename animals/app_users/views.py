from django.http import HttpRequest
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .utils import send_email_to_upgrade
from django.db import transaction
from rest_framework import status


@api_view(["POST"])
def ask_for_upgrade(request: HttpRequest) -> Response:
    """
    An api view function to request the upgrade of a user's status.
    First checks if the user is authenticated.
    If he is, checks if he has already asked for an upgrade.
    If he has not, checks if the post data contains the email of the user of it is saved
    in the database.
    If there is a user email, accepts the request: sends an email (send_email_to_upgrade() function)
    to the admin and returns a 202 Response.
    If the user has already asked for an upgrade, returns a 208 Response.
    If the user has not provided his email, returns a 400 Response.
    If the user is not authenticated, returns a 401 Response.

    """
    if request.user.is_authenticated:
        cur_user = request.user
        if 'email' in request.data or cur_user.email:
            if cur_user.asked_for_upgrade is False:
                with transaction.atomic():
                    if not cur_user.email:
                        cur_user.email = request.data.get('email')

                    cur_user.asked_for_upgrade = True
                    cur_user.save(force_update=['email', 'asked_for_upgrade'])
                    send_email_to_upgrade(user=cur_user)

                    return Response(
                        {
                            'details': 'You request was submitted'
                        },
                        status=status.HTTP_202_ACCEPTED
                    )
            else:
                return Response(
                    {
                        'details': 'Your request is being processed'
                    },
                    status=status.HTTP_208_ALREADY_REPORTED
                )
        return Response(
            {
                'details': "To make this request you have to pass your email"
            },
            status=status.HTTP_400_BAD_REQUEST
        )
    return Response(
        {
            'details': 'Credentials are not provided'
        },
        status=status.HTTP_401_UNAUTHORIZED
    )





