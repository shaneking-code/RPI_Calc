# Generated by Django 4.2.3 on 2023-07-25 03:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rpiapp', '0002_delete_rpi'),
    ]

    operations = [
        migrations.CreateModel(
            name='Season',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.DateField(verbose_name='Year of season')),
            ],
        ),
        migrations.RemoveField(
            model_name='game',
            name='away_team',
        ),
        migrations.RemoveField(
            model_name='game',
            name='home_team',
        ),
        migrations.RemoveField(
            model_name='game',
            name='loser',
        ),
        migrations.RemoveField(
            model_name='game',
            name='winner',
        ),
        migrations.DeleteModel(
            name='Team',
        ),
        migrations.AddField(
            model_name='game',
            name='season',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='season', to='rpiapp.season'),
        ),
    ]