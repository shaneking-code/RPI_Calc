from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db.models import Q
from .models import League, Team, Season, Game
from .rpi_internal import calc_rpi

# VIEWS

# Show home page
def index(request):

    # Show the most recent 5 games
    latest_games = Game.objects.all().order_by("-id")[:5]
    all_leagues = League.objects.all()
    context = {
        "latest_games" : latest_games,
        "all_leagues" : all_leagues,
    }

    return render(request, "rpiapp/index.html", context)

# Show error page
def error(request, error):

    context = {
        "error" : error
    }

    return render(request, "rpiapp/error.html", context)

#Search for a league
def league_search(request):

    if request.method == 'POST':
        search_term = request.POST.get('search_term')
        search_results = League.objects.filter(name__contains=search_term)

        context = {
            "search_term" : search_term,
            "search_results" : search_results
        }

        return render(request, "rpiapp/league_search.html", context)

# Search for a team
def team_search(request, league_id):

    if request.method == 'POST':
        search_term = request.POST.get('search_term')
        search_results = Team.objects.filter(Q(league__id=league_id) & Q(name__contains=search_term))

        context = {
            "search_term" : search_term,
            "search_results" : search_results
        }

        return render(request, "rpiapp/team_search.html", context)

# Search for a game (by date)
def game_search(request, league_id, season_id):

    if request.method == 'POST':
        search_date = request.POST.get('date')
        search_results = []
        for game in Game.objects.filter(Q(league__id=league_id) & Q(season__id=season_id)):
            if str(game.date) == search_date:
                search_results.append(game)
        
        context = {
            "search_date" : search_date,
            "search_results" : search_results
        }

        return render(request, "rpiapp/game_search.html", context)
    
# Get details of a league through leagues/league_id/
def league_details(request, league_id):

    league = get_object_or_404(League, id=league_id)
    league_seasons = league.seasons.all().order_by("-year")
    league_teams = league.teams.all().order_by("name")
        
    context = {
        "league" : league,
        "league_seasons" : league_seasons,
        "league_teams" : league_teams
    }

    return render(request, "rpiapp/league_details.html", context)

# Add a league
def add_league(request):

    if request.method == 'POST':
        league_name = request.POST.get('league_name')
        if League.objects.all().filter(name=league_name).exists():
            error = "League already exists"
            return HttpResponseRedirect(reverse('rpiapp:error', args=[error]))
        league = League.objects.create(name=league_name)
        league.save()

        return HttpResponseRedirect(reverse('rpiapp:league_details', args=[league.id]))
    
    else:

        return HttpResponseRedirect(reverse('rpiapp:index'))

# Delete a league
def delete_league(request, league_id):
    
    if request.method == 'POST':
        league = get_object_or_404(League, id=league_id)
        league.delete()

    return HttpResponseRedirect(reverse('rpiapp:index'))
    
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

# Add a team
def add_team(request,league_id):

    if request.method == 'POST':
        team_name = request.POST.get('team_name')
        team_league = get_object_or_404(League, id=league_id)
        if Team.objects.filter(Q(name=team_name) & Q(league=team_league)).exists():
            error = "Team already exists"
            return HttpResponseRedirect(reverse('rpiapp:error', args=[error]))
        team = Team.objects.create(name=team_name, league=team_league)
        team.save()

    return HttpResponseRedirect(reverse("rpiapp:league_details", args=[league_id]))

# Delete a team
def delete_team(request,league_id,team_id):

    if request.method == 'POST':
        team = get_object_or_404(Team, id=team_id)
        team.delete()

    return HttpResponseRedirect(reverse('rpiapp:league_details', args=[league_id]))

# Get details of a season through leagues/league_id/seasons/season_id
def season_results(request, league_id, season_id):

    season = get_object_or_404(Season, id=season_id)
    season_games = season.season_games.all().order_by("-date")
    league_teams = get_object_or_404(League, id=league_id).teams.all()

    season_teams = set()
    # Populate season_teams
    for game in season_games:
        # If game winner is not in season_teams, add them
        if game.winner.name not in season_teams:
            season_teams.add(game.winner)
        # If game loser is not in season_teams, add them
        if game.loser.name not in season_teams:
            season_teams.add(game.loser)

    season_games_by_date = {}
    # Populate season_games_by_date
    for game in season_games:
        # If date has no games associated, add it
        if game.date not in season_games_by_date:
            season_games_by_date[game.date] = [game]
        # If date has games associated, append it
        else:
            season_games_by_date[game.date].append(game)

    # Get (date, games) pairs from dict
    season_games_by_date = season_games_by_date.items()

    # Populate season_games_obj
    season_games_obj = []
    for game in season_games:
        season_games_obj.append({
            "Winner" : game.winner.name,
            "Loser" : game.loser.name,
            "Location" : game.home_team.name
        })
    
    rpis = []
    for team in set(season_teams):
        rpis.append(format(calc_rpi(team.name,season_games_obj), '.3f'))
    
    rpis_by_team = list(zip(rpis,season_teams))
    rpis_by_team = reversed(sorted(rpis_by_team, key=lambda x: x[0]))

    context = {
        "season" : season,
        "season_games_by_date" : season_games_by_date,
        "league_teams" : league_teams,        
        "rpis_by_team" : rpis_by_team,
    }

    return render(request, "rpiapp/season_results.html", context)

# Add a season
def add_season(request, league_id):

    league = get_object_or_404(League, id=league_id)
    if request.method == 'POST':
        season_year = request.POST.get('year')
        if league.seasons.filter(year=season_year).exists():
            error = "Season already exists"
            return HttpResponseRedirect(reverse('rpiapp:error', args=[error]))
        season = Season(year=season_year,league=League.objects.get(id=league_id))
        season.save()
        return HttpResponseRedirect(reverse('rpiapp:season_results', kwargs={"league_id" : league_id,
                                                                             "season_id" : season.id}))
    else:
        return HttpResponseRedirect(reverse('rpiapp:league_details', args=[league_id]))

# Delete a season
def delete_season(request, league_id, season_id):

    if request.method == 'POST':
        season = get_object_or_404(Season, id=season_id)
        season.delete()

    return HttpResponseRedirect(reverse('rpiapp:league_details', args=[league_id]))
    
# Get details of a game through leagues/league_id/games/game_id
def game_details(request, league_id, season_id, game_id):

    game = get_object_or_404(Game, id=game_id)
    context = {
        "game" : game
    }

    return render(request, "rpiapp/game_details.html", context)

# Add a game
def add_game(request, league_id, season_id):
    
    if request.method == 'POST':
        date = request.POST.get('date')
        winner = Team.objects.get(name=request.POST.get('winner'))
        loser = Team.objects.get(name=request.POST.get('loser'))
        home_team = Team.objects.get(name=request.POST.get('home_team'))
        away_team = Team.objects.get(name=request.POST.get('away_team'))
        season = Season.objects.get(id=season_id)
        league = League.objects.get(id=league_id)
        game = Game(date=date,
                    winner=winner,
                    loser=loser,
                    home_team=home_team,
                    away_team=away_team,
                    season=season,
                    league=league)
        game.save()

        return HttpResponseRedirect(reverse('rpiapp:season_results', kwargs={ "season_id" : season_id,
                                                                             "league_id" : league_id}))
    else:

        return HttpResponseRedirect(reverse('rpiapp:season_results', args=[season_id]))

# Delete a game
def delete_game(request, league_id, season_id, game_id):

    if request.method == 'POST':
        game = get_object_or_404(Game, id=game_id)
        game.delete()

    return HttpResponseRedirect(reverse('rpiapp:season_results', kwargs={ "season_id" : season_id,
                                                                             "league_id" : league_id}))