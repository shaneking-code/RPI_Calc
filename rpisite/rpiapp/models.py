from django.db import models

class League(models.Model):

    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class Season(models.Model):

    league = models.ForeignKey(League, on_delete=models.CASCADE, related_name="seasons", null=True)
    year = models.IntegerField(default=2023)

    def __str__(self):
        return (f"{self.league}'s {self.year} Season")

class Team(models.Model):

    league = models.ForeignKey(League, on_delete=models.CASCADE, related_name="teams", null=True)
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
    
class Game(models.Model):

    date      = models.DateField('Date of game')
    home_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="home_games", null=True)
    away_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="away_games", null=True)
    winner    = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="won_games", null=True)
    loser     = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="lost_games", null=True)
    season    = models.ForeignKey(Season, on_delete=models.CASCADE, related_name="season_games", null=True)
    league    = models.ForeignKey(League, on_delete=models.CASCADE, related_name="league_games", null=True)

    def __str__(self):
        return (f"{self.home_team} vs. {self.away_team} ({self.date}) where {self.winner} defeated {self.loser}")
