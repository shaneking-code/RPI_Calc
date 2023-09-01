from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from ..forms.add_forms import AddLeagueForm, AddTeamForm, AddSeasonForm, AddGameForm
from ..models import League, Team, Season, Game, RPI
from ..utils.rpi import get_season_params

def index(request):

    # Show the most recent 5 games

    if request.method == 'POST':
        add_league_form = AddLeagueForm(request.POST)
        if add_league_form.is_valid():
            league = add_league_form.save()
            league.created_by = request.user
            league.save()
            messages.success(request, f"League '{league}' created successfully")
            return HttpResponseRedirect(reverse("rpiapp:league_details", args=[league.id]))
    else:
        add_league_form = AddLeagueForm()

    context = {
        "add_league_form" : add_league_form
    }

    return render(request, "rpiapp/detail_templates/index.html", context)

def league_details(request, league_id):

    league = get_object_or_404(League, id=league_id)
    league_seasons = league.seasons.all().order_by("-start_date")
    league_teams = league.teams.all().order_by("name")
    add_team_form = AddTeamForm()
    add_season_form = AddSeasonForm()

    if request.method == 'POST':
        if 'add_team' in request.POST:
            add_team_form = AddTeamForm(request.POST)
            if add_team_form.is_valid():
                if Team.objects.filter(league=league, name=add_team_form.cleaned_data['name']).exists():
                    messages.error(request, "Team with this name in this league exists already")
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
                team = add_team_form.save()
                team.league = league
                team.created_by = request.user
                team.save()
                messages.success(request, f"Team {team} created successfully")
        if 'add_season' in request.POST:
            add_season_form = AddSeasonForm(request.POST)
            if add_season_form.is_valid():
                if Season.objects.filter(league=league, name=add_season_form.cleaned_data['name']).exists():
                    messages.error(request, "Season with this name in this league exists already")
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
                season = add_season_form.save()
                season.league = league
                season.created_by = request.user
                season.save()
                for team in league_teams:
                    RPI.objects.create(team=team,season=season,rpi=-1)
                messages.success(request, f"Season {season} created successfully")
        
    else:
        add_team_form = AddTeamForm()
        add_season_form = AddSeasonForm()

    context = {
        "league" : league,
        "league_seasons" : league_seasons,
        "league_teams" : league_teams,
        "add_team_form" : add_team_form,
        "add_season_form" : add_season_form
    }

    return render(request, "rpiapp/detail_templates/league_details.html", context)

def team_details(request, league_id, team_id):

    team = get_object_or_404(Team, id=team_id)
    team_games = team.home_games.all() | team.away_games.all()
    team_games = team_games.order_by("-season__start_date")

    team_games_by_season = {}
    for game in team_games:
        if game.season not in team_games_by_season:
            team_games_by_season[game.season] = {"games":[],
                                                 "wins":0,
                                                 "losses":0,
                                                 "rpi":format(get_object_or_404(RPI, team=team, season=game.season).rpi, '.3f')}
        team_games_by_season[game.season]['games'].append(game)
        if game.winner == team:
            team_games_by_season[game.season]['wins'] += 1
        if game.loser == team:
            team_games_by_season[game.season]['losses'] += 1

    context = {
        "team" : team,
        "team_games_by_season" : team_games_by_season,
    }

    return render(request, "rpiapp/detail_templates/team_details.html", context)

def season_details(request, league_id, season_id):

    league = get_object_or_404(League, id=league_id)
    season = get_object_or_404(Season, id=season_id)
    season_games = season.season_games.all().order_by("-date")
    league_teams = league.teams.all()

    season_teams, _ = get_season_params(season_games)

    season_games_by_date = {}
    # Populate season_games_by_date
    for game in season_games:
        if game.date not in season_games_by_date:
            season_games_by_date[game.date] = [game]
        else:
            season_games_by_date[game.date].append(game)

    rpis = []
    for team in set(season_teams):
        rpi = RPI.objects.get(team=team, season=season)
        rpis.append(format(rpi.rpi, '.3f'))
    
    rpis_by_team = list(zip(rpis,season_teams))
    rpis_by_team = reversed(sorted(rpis_by_team, key=lambda x: x[0]))

    if request.method == 'POST':
        add_game_form = AddGameForm(request.POST, season=season)
        if add_game_form.is_valid():
            date = add_game_form.cleaned_data['date']
            if date < season.start_date or date > season.end_date:
                messages.error(request, f"Game outside of date range ({season.start_date})-({season.end_date})")
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            game = add_game_form.save(commit=False)
            game.created_by = request.user
            game.league = league
            game.season = season
            game.bulk_processing = False
            game.save()
            
            messages.success(request, f"Game: '{game}' created successfully")
            return HttpResponseRedirect(reverse("rpiapp:season_details", kwargs={"league_id" : league_id,
                                                                                 "season_id" : season_id}))
    else:
        add_game_form = AddGameForm(season=season)

    context = {
        "season" : season,
        "season_games_by_date" : season_games_by_date,
        "league_teams" : league_teams,        
        "rpis_by_team" : rpis_by_team,
        "add_game_form" : add_game_form
    }

    return render(request, "rpiapp/detail_templates/season_details.html", context)

def game_details(request, league_id, season_id, game_id):

    game = get_object_or_404(Game, id=game_id)
    context = {
        "game" : game
    }

    return render(request, "rpiapp/detail_templates/game_details.html", context)
            