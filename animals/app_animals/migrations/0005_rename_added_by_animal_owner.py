# Generated by Django 4.2.1 on 2023-05-15 07:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_animals', '0004_animal_added_by'),
    ]

    operations = [
        migrations.RenameField(
            model_name='animal',
            old_name='added_by',
            new_name='owner',
        ),
    ]
