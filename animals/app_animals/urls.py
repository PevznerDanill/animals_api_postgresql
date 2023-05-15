from django.urls import path
from .views import AnimalListAPIView, ShelterListAPIView, AnimalCreateAPIView, AnimalDetailAPIView


app_name = 'app_animals'

urlpatterns = [
    path('', AnimalListAPIView.as_view(), name='animal_list'),
    path('shelters/', ShelterListAPIView.as_view(), name='shelter_list'),
    path('new/', AnimalCreateAPIView.as_view(), name='animal_new'),
    path('<int:pk>/', AnimalDetailAPIView.as_view(), name='animal_detail')
]
