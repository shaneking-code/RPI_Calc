from django.urls import path
from . import views

app_name = "rpiapp"
urlpatterns = [
    path("", views.index, name="index"),
    path("error/<str:error>/", views.error, name="error"),

    path("leagues/search/", views.league_search, name="league_search"),
    path("leagues/<int:league_id>/teams/search/", views.team_search, name="team_search"),
    path("leagues/<int:league_id>/seasons/<int:season_id>/search/", views.game_search, name="game_search"),
    #path("search/leagues/", views.search_leagues, name="search_leagues"),
    #path("search/teams/", views.search_teams, name="search_teams"),
    #path("search/games/", views.search_games, name="search_games"),
    
    path("leagues/<int:league_id>/", views.league_details, name="league_details"),
    path("leagues/<int:league_id>/teams/<int:team_id>/", views.team_details, name="team_details"),
    path("leagues/<int:league_id>/seasons/<int:season_id>/", views.season_results, name="season_results"),
    path("leagues/<int:league_id>/seasons/<int:season_id>/games/<int:game_id>/", views.game_details, name="game_details"),


    path("addleague/", views.add_league, name="add_league"),
    path("addteam/league/<int:league_id>", views.add_team, name="add_team"),
    path("addseason/<int:league_id>/", views.add_season, name="add_season"),
    path("addgame/league/<int:league_id>/season/<int:season_id>/", views.add_game, name="add_game"),

    path("deleteleague/<int:league_id>/", views.delete_league, name="delete_league"),
    path("deleteteam/league/<int:league_id>/team/<int:team_id>/", views.delete_team, name="delete_team"),
    path("deleteseason/league/<int:league_id>/season/<int:season_id>/", views.delete_season, name="delete_season"),
    path("deletegame/league/<int:league_id>/season/<int:season_id>/game/<int:game_id>/", views.delete_game, name="delete_game"),
]