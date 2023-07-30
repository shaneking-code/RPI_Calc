from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Game, Season, Team, League
# Create your views here.
def index(request):

    # Show the most recent 5 games
    latest_games = Game.objects.all()[:5]
    context = {
        "latest_games" : latest_games
    }

    return render(request, "rpiapp/index.html", context)

# Get details of a league through leagues/league_id/
def league_details(request, league_id):

    league = get_object_or_404(League, id=league_id)
    league_seasons = league.seasons.all()
    league_teams = league.teams.all()
    context = {
        "league" : league,
        "league_seasons" : league_seasons,
        "league_teams" : league_teams
    }

    return render(request, "rpiapp/league_details.html", context)

# Get details of a game through games/game_id
def game_details(request, game_id):

    game = get_object_or_404(Game, id=game_id)
    context = {
        "game" : game
    }

    return render(request, "rpiapp/game_details.html", context)

# Get details of a season through seasons/season_id
def season_details(request, season_id):
    season = get_object_or_404(Season, id=season_id)
    season_games = season.games.all()
    context = {
        "season" : season,
        "season_games" : season_games
    }
    return render(request, "rpiapp/season_details.html", context)

# Get details of a season through leagues/seasons/season_id
def season_results(request, season_id):

    season = get_object_or_404(Season, id=season_id)
    season_games = season.games.all()
    season_games = season_games.order_by("date")
    context = {
        "season" : season,
        "season_games" : season_games
    }

    return render(request, "rpiapp/season_results.html", context)

# Get details of a team through teams/team_id
def team_details(request, team_id):

    team = get_object_or_404(Team, id=team_id)
    team_games = team.home_games.all() | team.away_games.all()
    games_by_season = {}
    for game in team_games:
        season = game.season
        if season not in games_by_season:
            games_by_season[season] = []
        games_by_season[season].append(game)
    context = {
        "team" : team,
        "games_by_season" : games_by_season
    }

    return render(request, "rpiapp/team_details.html", context)

# Get teams in a league through leagues/league_id/games
def league_teams(request, league_id):

    league = get_object_or_404(League, id=league_id)
    teams = league.teams.all()
    teams = teams.order_by("name")
    context = {
        "league" : league,
        "teams" : teams
    }

    return render(request, "rpiapp/league_teams.html", context)

# Get games in a league through leagues/league_id/games
def league_games(request, league_id):

    league = get_object_or_404(League, id=league_id)
    games = league.games.all()
    games = games.order_by("date")
    context = {
        "league" : league,
        "games" : games
    }

    return render(request, "rpiapp/league_games.html", context)
    

