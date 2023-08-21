from django.urls import path
from .views import delete_views, detail_views, edit_views, misc_views, search_views, user_views

app_name = "rpiapp"
urlpatterns = [

    # User URLs
    path("register/", user_views.register_user, name="register_user"),
    path("login/", user_views.login_user, name="login_user"),
    path("logout/", user_views.logout_user, name="logout_user"),
    path("users/<int:user_id>/", user_views.user_profile, name="user_profile"),
    path("users/<int:user_id>/edit/", user_views.edit_profile, name="edit_profile"),
    path("users/<int:user_id>/delete", user_views.delete_profile, name="delete_profile"),

    # Search URLs
    path("users/search/", search_views.user_search, name="user_search"),
    path("leagues/search/", search_views.league_search, name="league_search"),
    path("leagues/<int:league_id>/teams/search/", search_views.team_search, name="team_search"),
    path("leagues/<int:league_id>/seasons/<int:season_id>/games/search/", search_views.game_search, name="game_search"),
    
    # Index URL
    path("", detail_views.index, name="index"),

    # Detail URLs
    path("leagues/<int:league_id>/", detail_views.league_details, name="league_details"),
    path("leagues/<int:league_id>/teams/<int:team_id>/", detail_views.team_details, name="team_details"),
    path("leagues/<int:league_id>/seasons/<int:season_id>/", detail_views.season_details, name="season_details"),
    path("leagues/<int:league_id>/seasons/<int:season_id>/games/<int:game_id>/", detail_views.game_details, name="game_details"),

    # Edit URLs
    path("leagues/<int:league_id>/edit/", edit_views.edit_league, name="edit_league"),
    path("leagues/<int:league_id>/teams/<int:team_id>/edit/", edit_views.edit_team, name="edit_team"),
    path("leagues/<int:league_id>/seasons/<int:season_id>/edit/", edit_views.edit_season, name="edit_season"),
    path("leagues/<int:league_id>/seasons/<int:season_id>/games/<int:game_id>/edit/", edit_views.edit_game, name="edit_game"),

    # Delete URLs
    path("leagues/<int:league_id>/delete/", delete_views.delete_league, name="delete_league"),
    path("leagues/<int:league_id>/teams/<int:team_id>/delete/", delete_views.delete_team, name="delete_team"),
    path("leagues/<int:league_id>/seasons/<int:season_id>/delete/", delete_views.delete_season, name="delete_season"),
    path("leagues/<int:league_id>/seasons/<int:season_id>/games/<int:game_id>/delete/", delete_views.delete_game, name="delete_game"),

    # Add Games through File
    path("leagues/<int:league_id>/seasons/<int:season_id>/addgames/", misc_views.bulk_game_upload, name="bulk_game_upload")
]