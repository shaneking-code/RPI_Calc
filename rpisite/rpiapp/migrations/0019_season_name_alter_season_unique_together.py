# Generated by Django 4.2.3 on 2023-08-14 20:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rpiapp', '0018_alter_season_unique_together_season_end_date_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='season',
            name='name',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterUniqueTogether(
            name='season',
            unique_together={('league', 'name')},
        ),
    ]
