from django.apps import apps
from .rpi import calc_rpi

def bulk_recalculate_rpis(season,games):
    RPI = apps.get_model('rpiapp', 'RPI')
    season_games_obj = []
    season_teams = set()
    for game in games:
        if game.winner not in season_teams:
            season_teams.add(game.winner)
        if game.loser not in season_teams:
            season_teams.add(game.loser)

        season_games_obj.append({
            "Winner" : game.winner.name,
            "Loser" : game.loser.name,
            "Location" : game.home_team.name
        })

    for team in season_teams:
        team_rpi, created = RPI.objects.get_or_create(team=team,season=season,rpi=-1)
        if created:
            print("CREATING" + str(team) + "'s RPI!!!")
        else:
            print("UPDATING" + str(team) + "'s RPI!!!")

        team_rpi.rpi = calc_rpi(team.name,season_games_obj)
        team_rpi.save()
        
def bulk_create_games(season,games,calculate_rpis):
    Game = apps.get_model('rpiapp','Game')
    Game.objects.bulk_create(games)
    if calculate_rpis:
        bulk_recalculate_rpis(season, games)