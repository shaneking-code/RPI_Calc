from django.apps import apps
from .rpi import calc_rpi, get_season_params

def bulk_recalculate_rpis(season,games):
    RPI = apps.get_model('rpiapp', 'RPI')
    season_teams, season_games_obj = get_season_params(games)

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