from django.urls import path
from .views import ask_for_upgrade


app_name = 'app_users'

urlpatterns = [
    path('upgrade/', ask_for_upgrade, name='user_upgrade')
]
