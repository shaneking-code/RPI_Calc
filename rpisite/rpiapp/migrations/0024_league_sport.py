# Generated by Django 4.2.3 on 2023-08-22 03:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rpiapp', '0023_remove_league_high_weight_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='league',
            name='sport',
            field=models.CharField(max_length=100, null=True),
        ),
    ]