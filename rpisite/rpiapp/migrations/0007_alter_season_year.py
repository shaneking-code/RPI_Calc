# Generated by Django 4.2.3 on 2023-07-25 03:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rpiapp', '0006_alter_season_year'),
    ]

    operations = [
        migrations.AlterField(
            model_name='season',
            name='year',
            field=models.IntegerField(default=2023),
        ),
    ]