# Generated by Django 4.2.3 on 2023-07-25 03:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rpiapp', '0004_alter_season_year'),
    ]

    operations = [
        migrations.AlterField(
            model_name='season',
            name='year',
            field=models.IntegerField(default=2023),
        ),
    ]
