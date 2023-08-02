from django.urls import path
from . import views

app_name = "rpiapp"
urlpatterns = [
    path("", views.index, name="index"),
    
    #path("search/leagues/", views.search_leagues, name="search_leagues"),
    #path("search/teams/", views.search_teams, name="search_teams"),
    #path("search/games/", views.search_games, name="search_games"),
    
    path("leagues/<int:league_id>/", views.league_details, name="league_details"),
    path("leagues/<int:league_id>/teams/<int:team_id>/", views.team_details, name="team_details"),
    path("leagues/<int:league_id>/games/<int:game_id>/", views.game_details, name="game_details"),
    path("leagues/<int:league_id>/seasons/<int:season_id>/", views.season_results, name="season_results"),
    path("addleague/", views.add_league, name="add_league"),
    path("addseason/<int:league_id>/", views.add_season, name="add_season"),
    path("addgame/league/<int:league_id>/season/<int:season_id>/", views.add_game, name="add_game")
]