from ..models import RPI, Game
from .rpi import calc_rpi, get_season_params

def toggle_bulk_processing(games, value):
    for game in games:
        game.bulk_processing = value
    Game.objects.bulk_update(games, ['bulk_processing'])
    
def bulk_calculate_rpis(season,games):
    season_teams, season_games_obj = get_season_params(games)
    for team in season_teams:
        if RPI.objects.filter(team=team,season=season).exists():
            team_rpi = RPI.objects.get(team=team,season=season)
            team_rpi.rpi = calc_rpi(team.name,
                                    season_games_obj,
                                    season.location_matters,
                                    season.high_weight,
                                    season.low_weight,
                                    season.wp_weight,
                                    season.owp_weight,
                                    season.oowp_weight)
            team_rpi.save()
        else:
            team_rpi = RPI.objects.create(team=team,season=season,rpi=calc_rpi(team.name,
                                                                            season_games_obj,
                                                                            season.location_matters,
                                                                            season.high_weight,
                                                                            season.low_weight,
                                                                            season.wp_weight,
                                                                            season.owp_weight,
                                                                            season.oowp_weight))
            team_rpi.save()

def bulk_create_games(season,games,calculate_rpis):
    Game.objects.bulk_create(games)
    toggle_bulk_processing(games, False)
    if calculate_rpis:
        bulk_calculate_rpis(season, games)
