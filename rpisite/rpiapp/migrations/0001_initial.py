# Generated by Django 4.2.4 on 2023-08-31 17:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='League',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='user_leagues', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='user_teams', to=settings.AUTH_USER_MODEL)),
                ('league', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='teams', to='rpiapp.league')),
            ],
            options={
                'unique_together': {('league', 'name')},
            },
        ),
        migrations.CreateModel(
            name='Season',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField(null=True, verbose_name='Start date of season')),
                ('end_date', models.DateField(null=True, verbose_name='End date of season')),
                ('name', models.CharField(max_length=100, null=True)),
                ('location_matters', models.BooleanField(default=False)),
                ('high_weight', models.FloatField(default=1.0)),
                ('low_weight', models.FloatField(default=1.0)),
                ('wp_weight', models.FloatField(default=0.25)),
                ('owp_weight', models.FloatField(default=0.5)),
                ('oowp_weight', models.FloatField(default=0.25)),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='user_seasons', to=settings.AUTH_USER_MODEL)),
                ('league', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='seasons', to='rpiapp.league')),
            ],
            options={
                'unique_together': {('league', 'name', 'start_date', 'end_date')},
            },
        ),
        migrations.CreateModel(
            name='RPI',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rpi', models.DecimalField(decimal_places=6, max_digits=7)),
                ('season', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='season_rpis', to='rpiapp.season')),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='team_rpis', to='rpiapp.team')),
            ],
        ),
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(verbose_name='Date of game')),
                ('bulk_processing', models.BooleanField(default=False)),
                ('away_team', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='away_games', to='rpiapp.team')),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='user_games', to=settings.AUTH_USER_MODEL)),
                ('home_team', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='home_games', to='rpiapp.team')),
                ('league', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='league_games', to='rpiapp.league')),
                ('loser', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='lost_games', to='rpiapp.team')),
                ('season', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='season_games', to='rpiapp.season')),
                ('winner', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='won_games', to='rpiapp.team')),
            ],
        ),
    ]
