from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .utils import send_email_to_upgrade
from django.db import transaction
from rest_framework import status


@api_view(["POST"])
def ask_for_upgrade(request):
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





