# Generated by Django 2.2.28 on 2023-11-12 12:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('animalerie', '0002_auto_20231107_1623'),
    ]

    operations = [
        migrations.AddField(
            model_name='equipement',
            name='taille_max',
            field=models.IntegerField(default=1),
        ),
    ]
