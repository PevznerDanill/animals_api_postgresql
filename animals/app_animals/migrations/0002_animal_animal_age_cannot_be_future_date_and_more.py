# Generated by Django 4.2.1 on 2023-05-13 09:26

import datetime
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.db.models.functions.datetime


class Migration(migrations.Migration):

    dependencies = [
        ('app_animals', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Animal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('age', models.DateField(default=datetime.date.today, validators=[django.core.validators.MaxValueValidator(limit_value=datetime.date.today)])),
                ('joined_shelter', models.DateField(default=datetime.date.today, validators=[django.core.validators.MaxValueValidator(limit_value=datetime.date.today)])),
                ('distinctive_features', models.CharField(max_length=128)),
                ('weight', models.FloatField(default=0)),
                ('height', models.FloatField(default=0)),
                ('shelter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='animals', to='app_animals.shelter')),
            ],
            options={
                'verbose_name': 'animal',
                'verbose_name_plural': 'animals',
            },
        ),
        migrations.AddConstraint(
            model_name='animal',
            constraint=models.CheckConstraint(check=models.Q(('age__lte', django.db.models.functions.datetime.Now())), name='age_cannot_be_future_date'),
        ),
        migrations.AddConstraint(
            model_name='animal',
            constraint=models.CheckConstraint(check=models.Q(('joined_shelter__lte', django.db.models.functions.datetime.Now())), name='date_of_joining_shelter_cannot_be_future_date'),
        ),
    ]
