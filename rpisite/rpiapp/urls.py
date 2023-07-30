from django.urls import path
from . import views

app_name = "rpiapp"
urlpatterns = [
    path("", views.index, name="index"),
    
    #path("search/leagues/", views.search_leagues, name="search_leagues"),
    #path("search/teams/", views.search_teams, name="search_teams"),
    #path("search/games/", views.search_games, name="search_games"),
    
    path("leagues/<int:league_id>/", views.league_details, name="league_details"),
    path("teams/<int:team_id>/", views.team_details, name="team_details"),
    path("games/<int:game_id>/", views.game_details, name="game_details"),

    path("leagues/<int:league_id>/teams/", views.league_teams, name="league_teams"),
    path("leagues/<int:game_id>/games/", views.league_games, name="league_games"),

    path("seasons/<int:season_id>/", views.season_results, name="season_results")
]