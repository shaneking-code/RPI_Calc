# Generated by Django 4.2.3 on 2023-07-28 06:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rpiapp', '0011_league_season_league'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='league',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='teams', to='rpiapp.league'),
        ),
        migrations.AlterField(
            model_name='game',
            name='away_team',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='away_games', to='rpiapp.team'),
        ),
        migrations.AlterField(
            model_name='game',
            name='home_team',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='home_games', to='rpiapp.team'),
        ),
        migrations.AlterField(
            model_name='game',
            name='loser',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='lost_games', to='rpiapp.team'),
        ),
        migrations.AlterField(
            model_name='game',
            name='season',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='games', to='rpiapp.season'),
        ),
        migrations.AlterField(
            model_name='game',
            name='winner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='won_games', to='rpiapp.team'),
        ),
        migrations.AlterField(
            model_name='season',
            name='league',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='seasons', to='rpiapp.league'),
        ),
    ]