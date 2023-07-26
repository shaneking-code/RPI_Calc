from django.db import models

# Create your models here.
#class Team(models.Model):

#    name = models.CharField(max_length=100)

#    def __str__(self):
#        return self.name

class Season(models.Model):

    year = models.IntegerField(default=2023)

    def __str__(self):
        return (f"{self.year} Season")

class Team(models.Model):

    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class Game(models.Model):

    date      = models.DateField('Date of game')
    home_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="home_team", null=True)
    away_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="away_team", null=True)
    winner    = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="winner", null=True)
    loser     = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="loser", null=True)
    season    = models.ForeignKey(Season, models.CASCADE, related_name="season", null=True)

    def __str__(self):
        return (f"{self.home_team} vs. {self.away_team} ({self.date})\n"
                f"{self.winner} defeated {self.loser}")
