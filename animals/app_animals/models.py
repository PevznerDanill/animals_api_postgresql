from django.db import models
from django.db.models.functions import Now
from django.core.validators import MaxValueValidator, MinValueValidator
from datetime import date
from django.core.exceptions import ValidationError
from typing import Optional


class Shelter(models.Model):
    """
    Describes the Shelter model.
    """
    title = models.CharField(max_length=64)

    def __str__(self):
        return f'{self.title}#{self.pk}'


class Animal(models.Model):
    """
    Describes the Animal model.
    """
    shelter = models.ForeignKey(to=Shelter, related_name='animals', on_delete=models.CASCADE)
    name = models.CharField(max_length=64)
    age = models.DateField(
        validators=[MaxValueValidator(limit_value=date.today)],
        default=date.today
    )
    joined_shelter = models.DateField(
        validators=[MaxValueValidator(limit_value=date.today)],
        default=date.today
    )
    distinctive_features = models.CharField(max_length=128)
    weight = models.FloatField(default=0)
    height = models.FloatField(default=0)
    is_archived = models.BooleanField(default=False)
    owner = models.ForeignKey(to='app_users.User', on_delete=models.PROTECT, related_name='animals')

    def __str__(self) -> str:
        """
        Returns a string representation of the object with its name and id fields.
        """
        return f'{self.name}#{self.pk}'

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(age__lte=Now()),
                name='age_cannot_be_future_date'
            ),
            models.CheckConstraint(
                check=models.Q(joined_shelter__lte=Now()),
                name='date_of_joining_shelter_cannot_be_future_date'
            ),
        ]
        verbose_name = 'animal'
        verbose_name_plural = 'animals'

    def clean(self):
        """
        Checks if the birthdate is not later than the date of joining shelter.
        """
        if self.joined_shelter < self.age:
            raise ValidationError(
                {
                    'joined_shelter': 'The date of birth cannot '
                                      'be later than the date of joining shelter.'
                }
            )

    def save(self, *args, **kwargs):
        """
        Ensures the clean method is called before saving.
        """
        self.full_clean()
        super().save(*args, **kwargs)


