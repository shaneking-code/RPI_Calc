from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .utils.rpi import calc_rpi, get_season_params

class League(models.Model):

    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="user_leagues", null=True)
    name       = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Team(models.Model):

    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="user_teams", null=True)
    league     = models.ForeignKey(League, on_delete=models.CASCADE, related_name="teams", null=True)
    name       = models.CharField(max_length=100)
    
    class Meta:
        unique_together = ('league','name')

    def __str__(self):
        return self.name
    
class Season(models.Model):

    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="user_seasons", null=True)
    league     = models.ForeignKey(League, on_delete=models.CASCADE, related_name="seasons", null=True)
    start_date = models.DateField('Start date of season', null=True)
    end_date   = models.DateField('End date of season', null=True)
    name       = models.CharField(max_length=100, null=True)

    class Meta:
        unique_together = ('league', 'name')
        
    def __str__(self):
        return (f"{self.name}")

class Game(models.Model):

    created_by      = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="user_games", null=True)
    date            = models.DateField('Date of game')
    home_team       = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="home_games", null=True)
    away_team       = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="away_games", null=True)
    winner          = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="won_games", null=True)
    loser           = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="lost_games", null=True)
    season          = models.ForeignKey(Season, on_delete=models.CASCADE, related_name="season_games", null=True)
    league          = models.ForeignKey(League, on_delete=models.CASCADE, related_name="league_games", null=True)
    bulk_processing = models.BooleanField(default=False)

    def __str__(self):
        return (f"{self.home_team} vs. {self.away_team} ({self.date}) where {self.winner} defeated {self.loser}")
    
class RPI(models.Model):

    team   = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="team_rpis")
    season = models.ForeignKey(Season, on_delete=models.CASCADE, related_name="season_rpis")
    rpi    = models.DecimalField(decimal_places=6, max_digits=7)

    def __str__(self):
        return (f"{self.team}'s RPI from the {self.season}: {self.rpi}")

@receiver([post_save,post_delete], sender=Game)
def recalculate_rpis(sender, instance, **kwargs):
    if not instance.bulk_processing:
        try:
            season_games = instance.season.season_games.all()
            season_teams, season_games_obj = get_season_params(season_games)
            for team in season_teams:
                try:
                    rpi = RPI.objects.get(team=team,
                                          season=instance.season)
                    rpi.rpi = calc_rpi(team.name, season_games_obj)
                    rpi.save()
                except RPI.DoesNotExist as e:
                    print(f"Error: {e}")
                    rpi = RPI.objects.create(team=team, 
                                             season=instance.season,
                                             rpi=calc_rpi(team.name, season_games_obj))
                    rpi.save()
        except Season.DoesNotExist as se:
            print(f"Error: {se}")

        
