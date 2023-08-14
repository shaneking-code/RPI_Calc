from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views
from rpiapp.views import user_profile

app_name = "rpiapp"
urlpatterns = [

    # User URLs
    path("register/", views.register_user, name="register_user"),
    path("login/", views.login_user, name="login_user"),
    path("logout/", views.logout_user, name="logout_user"),
    path("userprofile/<int:user_id>/", login_required(user_profile.as_view()), name="user_profile"),
    path("userprofile/<int:user_id>/edit/", views.edit_profile, name="edit_profile"),
    # Index URL
    path("", views.index, name="index"),

    # Search URLs
    path("leagues/search/", views.league_search, name="league_search"),
    path("leagues/<int:league_id>/teams/search/", views.team_search, name="team_search"),
    path("leagues/<int:league_id>/seasons/<int:season_id>/games/search/", views.game_search, name="game_search"),
    
    # Detail URLs
    path("leagues/<int:league_id>/", views.league_details, name="league_details"),
    path("leagues/<int:league_id>/teams/<int:team_id>/", views.team_details, name="team_details"),
    path("leagues/<int:league_id>/seasons/<int:season_id>/", views.season_details, name="season_details"),
    path("leagues/<int:league_id>/seasons/<int:season_id>/games/<int:game_id>/", views.game_details, name="game_details"),

    # Edit URLs
    path("leagues/<int:league_id>/edit/", views.edit_league, name="edit_league"),
    path("leagues/<int:league_id>/teams/<int:team_id>/edit/", views.edit_team, name="edit_team"),
    path("leagues/<int:league_id>/seasons/<int:season_id>/edit/", views.edit_season, name="edit_season"),
    path("leagues/<int:league_id>/seasons/<int:season_id>/games/<int:game_id>/edit/", views.edit_game, name="edit_game"),

    # Delete URLs
    path("leagues/<int:league_id>/deleteleague/", views.delete_league, name="delete_league"),
    path("leagues/<int:league_id>/teams/<int:team_id>/deleteteam/", views.delete_team, name="delete_team"),
    path("leagues/<int:league_id>/seasons/<int:season_id>/deleteseason/", views.delete_season, name="delete_season"),
    path("leagues/<int:league_id>/seasons/<int:season_id>/games/<int:game_id>/deletegame/", views.delete_game, name="delete_game"),

    # Add Games through File
    path("leagues/<int:league_id>/seasons/<int:season_id>/addgames/", views.bulk_game_upload, name="bulk_game_upload")
]