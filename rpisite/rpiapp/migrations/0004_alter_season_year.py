# Generated by Django 4.2.3 on 2023-07-25 03:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rpiapp', '0003_season_remove_game_away_team_remove_game_home_team_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='season',
            name='year',
            field=models.IntegerField(),
        ),
    ]