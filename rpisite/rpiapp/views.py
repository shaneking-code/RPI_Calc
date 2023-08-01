from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Game, Season, Team, League
from .rpi_internal import calc_rpi
# Create your views here.
def index(request):

    # Show the most recent 5 games
    latest_games = Game.objects.all()[:5]
    all_leagues = League.objects.all()
    context = {
        "latest_games" : latest_games,
        "all_leagues" : all_leagues
    }

    return render(request, "rpiapp/index.html", context)

# Get details of a league through leagues/league_id/
def league_details(request, league_id):

    league = get_object_or_404(League, id=league_id)
    league_seasons = league.seasons.all()
    league_seasons = league_seasons.order_by("-year")
    league_teams = league.teams.all()
        
    context = {
        "league" : league,
        "league_seasons" : league_seasons,
        "league_teams" : league_teams
    }

    return render(request, "rpiapp/league_details.html", context)

# Get details of a game through leagues/league_id/games/game_id
def game_details(request, league_id, game_id):

    game = get_object_or_404(Game, id=game_id)
    context = {
        "game" : game
    }

    return render(request, "rpiapp/game_details.html", context)

# Get details of a season through leagues/league_id/seasons/season_id
def season_results(request, league_id, season_id):

    season = get_object_or_404(Season, id=season_id)
    season_games = season.season_games.all()
    season_games = season_games.order_by("date")
    season_teams = []
    for game in season_games:
        if game.winner.name not in season_teams:
            season_teams.append(game.winner.name)
        if game.loser.name not in season_teams:
            season_teams.append(game.loser.name)
    """
    standings = {}
    for team in League.objects.get(id=league_id).teams.all():
        for game in season_games:
            if team not in standings:
                standings[team] = {'wins':0,'losses':0}
            if game.winner == team:
                standings[team]['wins'] += 1
            if game.loser == team:
                standings[team]['losses'] += 1
    standings_sorted = dict(reversed(sorted(standings.items(), key=lambda x:x[1]['wins'])))
    """
    season_games_obj = []
    for game in season_games:
        season_games_obj.append({
            "Winner" : game.winner.name,
            "Loser" : game.loser.name,
            "Location" : game.home_team.name
        })
    
    rpis = []
    for team in season_teams:
        rpis.append(format(calc_rpi(team,season_games_obj), '.3f'))
    
    rpis_by_team = list(zip(rpis,season_teams))
    rpis_by_team = reversed(sorted(rpis_by_team, key=lambda x: x[0]))
    context = {
        "season" : season,
        "season_games" : season_games,
        "rpis_by_team" : rpis_by_team
    }

    return render(request, "rpiapp/season_results.html", context)

# Get details of a team through leagues/league_id/teams/team_id
def team_details(request, league_id, team_id):

    team = get_object_or_404(Team, id=team_id)
    team_games = team.home_games.all() | team.away_games.all()
    team_games = team_games.order_by("-season__year")

    team_games_by_season = {}
    for game in team_games:
        if game.season not in team_games_by_season:
            team_games_by_season[game.season] = {"games":[],
                                                 "wins":0,
                                                 "losses":0}
        team_games_by_season[game.season]['games'].append(game)
        if game.winner == team:
            team_games_by_season[game.season]['wins'] += 1
        if game.loser == team:
            team_games_by_season[game.season]['losses'] += 1
    context = {
        "team" : team,
        "team_games_by_season" : team_games_by_season,
    }

    return render(request, "rpiapp/team_details.html", context)

