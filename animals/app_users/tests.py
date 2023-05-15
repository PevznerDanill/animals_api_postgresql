from django.db.models import signals
import factory
from rest_framework.test import APITestCase
from random import choice, choices
from .models import User
from django.shortcuts import reverse
from rest_framework import status
from app_animals.models import Shelter, Animal
from string import ascii_letters


class AskForUpgradeAPITestCase(APITestCase):

    fixtures = [
        'app_animals/fixtures/shelters.json',
        'app_users/fixtures/users.json'
    ]

    @classmethod
    def setUpTestData(cls):
        username = ''.join(choices(ascii_letters, k=8))
        password = ''.join(choices(ascii_letters, k=8))
        cls.shelter = choice(Shelter.objects.all())
        cls.user = User.objects.create_user(username=username, password=password, shelter=cls.shelter)

    def setUp(self) -> None:
        self.user.email = 'someemail@email.com'
        self.user.save(force_update=['email'])
        # admin_user = User.objects.get(is_superuser=True)
        # admin_user.email = 'somenewemail@mail.com'
        # admin_user.save()
        self.url = reverse('app_users:user_upgrade')

    def test_ask_for_upgrade_202(self):
        self.client.force_login(user=self.user)
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.user.refresh_from_db()
        self.assertTrue(self.user.asked_for_upgrade)
        self.client.logout()

    def test_ask_for_upgrade_208(self):
        self.user.asked_for_upgrade = True
        self.user.save()
        self.client.force_login(user=self.user)
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_208_ALREADY_REPORTED)
        self.client.logout()

    def test_ask_for_upgrade_400(self):
        self.user.email = ''
        self.user.save()
        self.client.force_login(user=self.user)
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.client.logout()

    def test_ask_for_update_401(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)











