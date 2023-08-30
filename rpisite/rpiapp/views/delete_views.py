from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from ..models import League, Team, Season, Game
from ..utils.bulk_rpi import bulk_calculate_rpis, toggle_bulk_processing

@login_required
def delete_league(request, league_id):
    
    if request.method == 'POST':
        league = get_object_or_404(League, id=league_id)
        if request.user == league.created_by or request.user.is_superuser:
            league.delete()
            messages.success(request, f"League '{league}' deleted successfully")
        else:
            messages.error(request, "You cannot delete this league as you do not own it")

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required
def delete_team(request, league_id, team_id):

    if request.method == 'POST':
        league = get_object_or_404(League, id=league_id)
        team = get_object_or_404(Team, id=team_id)
        if request.user == team.created_by or request.user.is_superuser:
            league_games = league.league_games.all()
            league_seasons = league.seasons.all()
            toggle_bulk_processing(league_games, True)            
            team.delete()
            for season in league_seasons:
                bulk_calculate_rpis(season, season.season_games.all())
            toggle_bulk_processing(league_games, False) 
            messages.success(request, f"Team '{team}' deleted successfully")
        else:
            messages.error(request, "You cannot delete this team as you do not own it")

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required
def delete_season(request, league_id, season_id):

    if request.method == 'POST':
        season = get_object_or_404(Season, id=season_id)
        if request.user == season.created_by or request.user.is_superuser:
            season.delete()
            messages.success(request, f"Season deleted successfully: {season.name}")
        else:
            messages.error(request, "You cannot delete this season as you do not own it")

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required
def delete_game(request, league_id, season_id, game_id):

    if request.method == 'POST':
        game = get_object_or_404(Game, id=game_id)

        if request.user == game.created_by or request.user.is_superuser:
            game.delete()
            messages.success(request, f"Game between {game.home_team} and {game.away_team} on {game.date} deleted successfully")
        else:
            messages.error(request, "You cannot delete this game as you do not own it")

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
