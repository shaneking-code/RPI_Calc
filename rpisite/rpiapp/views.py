from django.shortcuts import render
from django.http import HttpResponse
from .models import Game, Season, Team
# Create your views here.
def index(request):

    # Show the most recent 5 games
    header = "<h1> Showing the most recent 5 games: <h1><br>"
    latest_games = Game.objects.all()[:5]
    output = "<br> ".join([str(game.winner) + " beat " + str(game.loser) + " on " + str(game.date) + " at " + str(game.home_team) for game in latest_games])
    return HttpResponse(header+output)

def season_detail(request, season_id):
    return HttpResponse(f"Viewing Season {season_id}")

def season_results(request, season_id):
    season = Season.objects.get(id=season_id)
    output = "<br> ".join([str(game.winner) for game in season.games.all()])
    return HttpResponse(output)

"""
def game_detail(request, game_id):
    game = Game.objects.get(id=game_id)
    output = str(game)
    return HttpResponse(output)
"""

