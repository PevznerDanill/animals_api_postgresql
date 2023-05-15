import random
from django.forms.models import model_to_dict
from django.shortcuts import reverse
from django.test import TestCase
from rest_framework.test import APITestCase
from app_users.models import User
from app_animals.models import Shelter, Animal
from random import choice, choices, randint
from string import ascii_letters
from datetime import date, timedelta
from rest_framework import status
import json
from django.db.models import Q
from django.db.models import signals
import factory


class AnimalListAPIViewAPITestCase(APITestCase):

    fixtures = [
        'app_animals/fixtures/shelters.json',
        'app_users/fixtures/users.json',
        'app_animals/fixtures/animals.json'
    ]

    @classmethod
    def setUpTestData(cls):
        username = ''.join(choices(ascii_letters, k=8))
        password = ''.join(choices(ascii_letters, k=8))
        cls.shelter = choice(Shelter.objects.all())
        cls.user = User.objects.create_user(username=username, password=password, shelter=cls.shelter)

    def setUp(self) -> None:
        self.url = reverse('app_animals:animal_list')

    def test_animal_list(self):
        self.client.force_login(user=self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_to_python = json.loads(response.content)

        self.assertEqual(
            response_to_python.get('count'),
            Animal.objects.select_related('shelter').filter(shelter=self.shelter, is_archived=False).count()
        )
        self.client.logout()

    def test_animal_unauthorized(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class AnimalCreateAPIViewAPITestCase(APITestCase):
    fixtures = [
        'app_animals/fixtures/shelters.json',
    ]

    @classmethod
    def setUpTestData(cls):
        username = ''.join(choices(ascii_letters, k=8))
        password = ''.join(choices(ascii_letters, k=8))
        cls.shelter = choice(Shelter.objects.all())
        cls.user = User.objects.create_user(username=username, password=password, shelter=cls.shelter, is_guest=False)

    def setUp(self) -> None:
        self.url = reverse('app_animals:animal_new')

        self.random_joined_shelter = date.today() - timedelta(days=randint(1, 1000))
        self.random_age = self.random_joined_shelter - timedelta(days=randint(1, 1000))
        self.data = {
            'joined_shelter': str(self.random_joined_shelter),
            "age": str(self.random_age),
            "height": 19.0,
            "weight": 35.0,
            "distinctive_features": ''.join(choices(ascii_letters, k=50)),
            "name": ''.join(choices(ascii_letters, k=20))
        }

    def test_animal_create(self):
        self.client.force_login(user=self.user)
        response = self.client.post(self.url, self.data)
        expected_data = self.data.copy()
        expected_data.update({'owner': self.user.pk, 'shelter': self.user.shelter.pk, 'id': 1})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertJSONEqual(response.content, expected_data)
        self.assertTrue(
            Animal.objects.filter(name=self.data.get('name')).exists()
        )
        self.client.logout()

    def test_animal_create_bad_dates(self):
        self.client.force_login(user=self.user)
        bad_data = self.data.copy()
        age = str(self.random_joined_shelter)
        joined_shelter = str(self.random_age)
        bad_data.update(
            {
                "age": age,
                "joined_shelter": joined_shelter
            }
        )
        bad_response = self.client.post(self.url, bad_data)
        self.assertEqual(bad_response.status_code, status.HTTP_400_BAD_REQUEST)
        self.client.logout()

    def test_animal_create_partial_data(self):
        self.client.force_login(user=self.user)
        bad_data = self.data.copy()
        bad_data.pop('distinctive_features')
        bad_response = self.client.post(self.url, bad_data)
        self.assertEqual(bad_response.status_code, status.HTTP_400_BAD_REQUEST)
        self.client.logout()

    def test_animal_create_unauthorized(self):
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class ShelterListAPIViewAPITestCase(APITestCase):

    fixtures = [
        'app_animals/fixtures/shelters.json',
    ]

    def setUp(self) -> None:
        self.url = reverse('app_animals:shelter_list')

    def test_shelter_list(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_to_python = json.loads(response.content)
        self.assertEqual(
            response_to_python.get('count'),
            Shelter.objects.all().count()
        )


class AnimalDetailAPIViewAPITestCase(APITestCase):

    fixtures = [
        'app_animals/fixtures/shelters.json',
        'app_users/fixtures/users.json',
        'app_animals/fixtures/animals.json'
    ]

    @factory.django.mute_signals(signals.pre_save)
    def setUp(self) -> None:
        Animal.objects.update(is_archived=False)
        User.objects.update(is_guest=False)

        self.animal = choice(
            Animal.objects.select_related('shelter', 'owner')
        )
        self.url = reverse('app_animals:animal_detail', kwargs={'pk': self.animal.pk})

        expected_data = model_to_dict(self.animal)
        expected_data['age'] = str(expected_data['age'])
        expected_data['joined_shelter'] = str(expected_data['joined_shelter'])
        expected_data.pop('is_archived')
        self.expected_data = expected_data

    def test_animal_detail_get(self):
        user = choice(User.objects.select_related('shelter').prefetch_related('animals').filter(shelter=self.animal.shelter))
        self.client.force_login(user=user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertJSONEqual(response.content, self.expected_data)
        self.client.logout()

    def test_animal_detail_patch(self):
        animal_owner = self.animal.owner
        self.client.force_login(user=animal_owner)
        random_name = ''.join(choices(ascii_letters, k=10))
        response = self.client.patch(self.url, {'name': random_name})
        new_data = self.expected_data.copy()
        new_data['name'] = random_name
        self.assertJSONEqual(response.content, new_data)
        self.client.logout()

    def test_animal_detail_put(self):
        animal_owner = self.animal.owner
        self.client.force_login(user=animal_owner)
        random_distinctive_features = ''.join(choices(ascii_letters, k=10))
        response = self.client.patch(self.url, {'distinctive_features': random_distinctive_features})
        new_data = self.expected_data.copy()
        new_data['distinctive_features'] = random_distinctive_features
        self.assertJSONEqual(response.content, new_data)
        self.client.logout()

    def test_animal_detail_delete(self):
        animal_owner = self.animal.owner
        self.client.force_login(user=animal_owner)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.animal.refresh_from_db()
        self.assertTrue(
            self.animal.is_archived
        )
        self.client.logout()

    def test_animal_detail_forbidden(self):
        user = choice(User.objects.prefetch_related('animals').filter(~Q(animals=self.animal) & ~Q(is_superuser=True)))
        self.client.force_login(user=user)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.logout()

