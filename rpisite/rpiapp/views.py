from django import forms
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.views.generic import ListView
from .models import League, Team, Season, Game
from .utils import calc_rpi
from .forms import *
import csv
import datetime

# VIEWS
##################### ACCOUNT VIEWS #####################
class user_profile(ListView):
    model = User
    context_object_name = "user_created"
    template_name = "rpiapp/user_profile.html"

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        leagues = League.objects.filter(created_by=self.request.user)
        teams = Team.objects.filter(created_by=self.request.user)
        context['leagues'] = leagues
        context['teams'] = teams
        return context

@login_required
def edit_profile(request, user_id):
    user_instance = get_object_or_404(User, id=user_id)
    update_form = EditUserForm(instance=user_instance)
    password_reset_form = PasswordChangeForm(user_instance)

    if request.method == 'POST':
        if 'update_fields' in request.POST:
            update_form = EditUserForm(request.POST, instance=user_instance)
            if update_form.is_valid():
                update_form.save()
                messages.success(request, "Profile changed successfully")
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        if 'password_change' in request.POST:
            password_reset_form = PasswordChangeForm(user_instance, request.POST)
            if password_reset_form.is_valid():
                user = password_reset_form.save()
                update_session_auth_hash(request, user)
                messages.success(request, "Password updated successfully")
                return HttpResponseRedirect(reverse("rpiapp:index"))

    context = {
        "update_form" : update_form,
        "password_reset_form" : password_reset_form,
        "user_instance" : user_instance
    }
    return render(request, "registration/edit_profile.html", context)

def register_user(request):

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = user.username
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return HttpResponseRedirect(reverse('rpiapp:index'))
    else:
        form = RegisterForm()

    return render(request, "registration/register.html", {"form" : form })

def login_user(request):

    if request.method == 'POST':
        form = AuthenticationForm(None, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            login(request, user)
            return HttpResponseRedirect(reverse('rpiapp:index'))
    else:
        form = AuthenticationForm()
    
    return render(request, "registration/login.html", {"form" : form})

def logout_user(request):
    logout(request)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

##################### HOME PAGE VIEW #####################
def index(request):

    # Show the most recent 5 games
    latest_games = Game.objects.all().order_by("-id")[:5]

    MAJOR_LEAGUES = ["Major League Baseball", 
                     "National Basketball Association", 
                     "National Football League", 
                     "National Hockey League", 
                     ]
    MAJOR_LEAGUES_OBJS = []
    for league in MAJOR_LEAGUES:
        MAJOR_LEAGUES_OBJS.append(get_object_or_404(League, name=league))

    NCAA_LEAGUES = ["NCAA Baseball",
                    "NCAA Football",
                    "NCAA Men's Basketball", 
                    "NCAA Women's Basketball", 
                    "NCAA Men's Hockey",
                    "NCAA Women's Hockey"
                    ]
    NCAA_LEAGUES_OBJS = []
    for league in NCAA_LEAGUES:
        NCAA_LEAGUES_OBJS.append(get_object_or_404(League, name=league))

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
        "latest_games" : latest_games,
        "major_leagues_objs" : MAJOR_LEAGUES_OBJS,
        "ncaa_leagues_objs" : NCAA_LEAGUES_OBJS,
        "add_league_form" : add_league_form
    }

    return render(request, "rpiapp/index.html", context)

##################### SEARCH FUNCTIONS #####################
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
        league = get_object_or_404(League, id=league_id)

        context = {
            "search_term" : search_term,
            "search_results" : search_results,
            "league" : league
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
            "search_results" : search_results,
        }

        return render(request, "rpiapp/game_search.html", context)

##################### MODEL FUNCTIONS #####################
##################### LEAGUE VIEWS #####################
# Get details of a league through leagues/league_id/
def league_details(request, league_id):

    league = get_object_or_404(League, id=league_id)
    league_seasons = league.seasons.all().order_by("-year")
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
                if Season.objects.filter(league=league, year=add_season_form.cleaned_data['year']).exists():
                    print("YAYAYAYAYAYAYAYAYA")
                    messages.error(request, "Season with this year in this league exists already")
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
                season = add_season_form.save()
                season.league = league
                season.created_by = request.user
                season.save()
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

    return render(request, "rpiapp/league_details.html", context)

# Edit a league
@login_required
def edit_league(request, league_id):
    league_instance = get_object_or_404(League, id=league_id)

    if request.method == 'POST' and (request.user == league_instance.created_by or request.user.is_superuser):
        form = EditLeagueForm(request.POST, instance=league_instance)
        if form.is_valid():
            if League.objects.all().filter(name=form.cleaned_data['name']).exists():
                messages.error(request, "League with that name exists already")
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            form.save()
            messages.success(request, "League updated successfully")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        form = EditLeagueForm(instance=league_instance)
    
    context = {
        "form" : form,
        "league" : league_instance
    }

    return render(request, "rpiapp/edit_league.html", context)
    
# Delete a league
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

##################### TEAM VIEWS #####################
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

@login_required
def edit_team(request, league_id, team_id):

    team_instance = get_object_or_404(Team, id=team_id)
    if request.method == 'POST' and (request.user == team_instance.created_by or request.user.is_superuser):
        form = EditTeamForm(request.POST, instance=team_instance)
        if form.is_valid():
            if Team.objects.all().filter(league__id = league_id, name=form.cleaned_data['name']).exists():
                messages.error(request, "Team in this league with that name already exists")
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            form.save()
            messages.success(request, "Team updated successfully")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        form = EditTeamForm(instance=team_instance)
    
    context = {
        "form" : form,
        "team" : team_instance
    }

    return render(request, "rpiapp/edit_team.html", context)


# Delete a team
@login_required
def delete_team(request,league_id,team_id):

    if request.method == 'POST':
        team = get_object_or_404(Team, id=team_id)
        if request.user == team.created_by or request.user.is_superuser:
            team.delete()
            messages.success(request, f"Team '{team}' deleted successfully")
        else:
            messages.error(request, "You cannot delete this team as you do not own it")

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

##################### SEASON VIEWS #####################
# Get details of a season through leagues/league_id/seasons/season_id
def season_details(request, league_id, season_id):

    league = get_object_or_404(League, id=league_id)
    season = get_object_or_404(Season, id=season_id)
    season_games = season.season_games.all().order_by("-date")
    league_teams = league.teams.all()

    season_teams = set()
    # Populate season_teams
    for game in season_games:
        if game.winner.name not in season_teams:
            season_teams.add(game.winner)
        if game.loser.name not in season_teams:
            season_teams.add(game.loser)

    season_games_by_date = {}
    # Populate season_games_by_date
    for game in season_games:
        if game.date not in season_games_by_date:
            season_games_by_date[game.date] = [game]
        else:
            season_games_by_date[game.date].append(game)


    season_games_obj = []
    # Populate season_games_obj
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

    if request.method == 'POST':
        add_game_form = AddGameForm(request.POST, season=season)
        if add_game_form.is_valid():
            game = add_game_form.save(commit=False)
            game.created_by = request.user
            game.league = league
            game.season = season
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

    return render(request, "rpiapp/season_details.html", context)

@login_required
def edit_season(request, league_id, season_id):
    season_instance = get_object_or_404(Season, id=season_id)

    if request.method == 'POST' and (request.user == season_instance.created_by or request.user.is_superuser):
        form = EditSeasonForm(request.POST, instance=season_instance)
        if form.is_valid():
            if Season.objects.all().filter(league__id=league_id, year=form.cleaned_data['year']).exists():
                messages.error(request, "Season in this league in that year exists already")
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            form.save()
            messages.success(request, "Season updated successfully")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        form = EditSeasonForm(instance=season_instance)
    
    context = {
        "form" : form,
        "season" : season_instance
    }

    return render(request, "rpiapp/edit_season.html", context)

# Delete a season
@login_required
def delete_season(request, league_id, season_id):

    if request.method == 'POST':
        season = get_object_or_404(Season, id=season_id)
        if request.user == season.created_by or request.user.is_superuser:
            season.delete()
            messages.success(request, f"Season deleted successfully: {season.year}")
        else:
            messages.error(request, "You cannot delete this season as you do not own it")

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

##################### GAME VIEWS #####################
# Get details of a game through leagues/league_id/games/game_id
def game_details(request, league_id, season_id, game_id):

    game = get_object_or_404(Game, id=game_id)
    context = {
        "game" : game
    }

    return render(request, "rpiapp/game_details.html", context)
                                                                         
@login_required
def edit_game(request, league_id, season_id, game_id):
    game_instance = get_object_or_404(Game, id=game_id)

    if request.method == 'POST' and (game_instance.created_by == request.user or request.user.is_superuser):
        form = EditGameForm(request.POST, instance=game_instance)
        if form.is_valid():
            form.save()
            messages.success(request, "Game updated successfully")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        form = EditGameForm(instance=game_instance)
    
    context = {
        "form" : form,
        "game" : game_instance
    }

    return render(request, "rpiapp/edit_game.html", context)

# Delete a game
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

# BULK GAME UPLOAD VIEW #
@login_required
def bulk_game_upload(request, league_id, season_id):

    season = get_object_or_404(Season, id=season_id)
    league = season.league

    if request.method == 'POST':
        games_csv = request.FILES.get('games_csv')
        decoded_games_csv = games_csv.read().decode('utf-8').splitlines()
        games_csv_reader = csv.reader(decoded_games_csv, delimiter=",")
        next(games_csv_reader)
        for row in games_csv_reader:
            date = datetime.datetime.strptime(row[0], '%m/%d/%Y').date()
            if date.year != season.year:
                messages.error(request, f"Contains game outside of year {season.year}")
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            home_team, ht_created = Team.objects.get_or_create(name=row[3], league=league, created_by=request.user)
            away_team, at_created = Team.objects.get_or_create(name=row[4], league=league, created_by=request.user)
            winner, w_created = Team.objects.get_or_create(name=row[1], league=league, created_by=request.user)
            loser, l_created = Team.objects.get_or_create(name=row[2], league=league, created_by=request.user)
            created_by = request.user
            game = Game.objects.create(
                created_by = created_by,
                date = date,
                home_team = home_team,
                away_team=away_team,
                winner=winner,
                loser=loser,
                season=season,
                league=league
            )
            game.save()
            if w_created:
                messages.success(request, f"Team '{winner}' created")
            if l_created:
                messages.success(request, f"Team '{loser}' created")
            if ht_created:
                messages.success(request, f"Team '{home_team}' created")
            if at_created:
                messages.success(request, f"Team '{away_team}' created")

        messages.success(request, "Games imported successfully")
        return HttpResponseRedirect(reverse('rpiapp:season_details', kwargs={"league_id":league.id,
                                                                             "season_id":season.id}))
    
    context = {
        "season" : season
    }
    return render(request, "rpiapp/add_games_bulk.html", context)
