from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.views.generic import ListView
from .models import League, Team, Season, Game
from .utils import calc_rpi
from .forms import RegisterForm
# VIEWS
# Account views

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
    return HttpResponseRedirect(reverse('rpiapp:index'))

# Show home page
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

    context = {
        "latest_games" : latest_games,
        "major_leagues_objs" : MAJOR_LEAGUES_OBJS,
        "ncaa_leagues_objs" : NCAA_LEAGUES_OBJS
    }

    return render(request, "rpiapp/index.html", context)

### SEARCH FUNCTIONS ###
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

### MODEL FUNCTIONS ###
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
@login_required
def add_league(request):

    if request.method == 'POST':
        league_name = request.POST.get('league_name')
        if League.objects.all().filter(name=league_name).exists():
            messages.error(request, f"League with name '{league_name}' already exists")

        else:
            league = League.objects.create(created_by=request.user, name=league_name)
            league.save()
            messages.success(request, f"League '{league}' created successfully")
            return HttpResponseRedirect(reverse('rpiapp:league_details', args=[league.id]))
    
    return HttpResponseRedirect(reverse('rpiapp:index'))

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
@login_required
def add_team(request,league_id):

    if request.method == 'POST':
        team_league = get_object_or_404(League, id=league_id)
        if request.user == team_league.created_by:
            team_name = request.POST.get('team_name')
            if Team.objects.filter(Q(name=team_name) & Q(league=team_league)).exists():
                messages.error(request, f"Team with name '{team_name}' already exists")
            else:
                team = Team.objects.create(created_by=request.user, name=team_name, league=team_league)
                team.save()
                messages.success(request, f"Team '{team}' created successfully")
        else:
            messages.error(request, "You cannot add this team as you do not own the league")

    return HttpResponseRedirect(reverse("rpiapp:league_details", args=[league_id]))

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

# Get details of a season through leagues/league_id/seasons/season_id
def season_details(request, league_id, season_id):

    season = get_object_or_404(Season, id=season_id)
    season_games = season.season_games.all().order_by("-date")
    league_teams = get_object_or_404(League, id=league_id).teams.all()

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

    context = {
        "season" : season,
        "season_games_by_date" : season_games_by_date,
        "league_teams" : league_teams,        
        "rpis_by_team" : rpis_by_team,
    }

    return render(request, "rpiapp/season_details.html", context)

# Add a season
@login_required
def add_season(request, league_id):

    league = get_object_or_404(League, id=league_id)
    if request.method == 'POST':
        if request.user == league.created_by:
            season_year = request.POST.get('year')
            if league.seasons.filter(year=season_year).exists():
                messages.error(request, f"{season_year} Season already exists")
                
            else:
                season = Season(created_by=request.user, year=season_year, league=league)
                season.save()
                messages.success(request, f"Season created successfully: {season.year}")
        else:
            messages.error(request, "You cannot add this season as you do not own the league")

    return HttpResponseRedirect(reverse('rpiapp:league_details', args=[league_id]))

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
    
# Get details of a game through leagues/league_id/games/game_id
def game_details(request, league_id, season_id, game_id):

    game = get_object_or_404(Game, id=game_id)
    context = {
        "game" : game
    }

    return render(request, "rpiapp/game_details.html", context)

# Add a game
@login_required
def add_game(request, league_id, season_id):
    
    league = get_object_or_404(League, id=league_id)
    if request.method == 'POST':
        if request.user == league.created_by:
            date = request.POST.get('date')
            winner = get_object_or_404(Team, name=request.POST.get('winner'), league=league)
            loser = get_object_or_404(Team, name=request.POST.get('loser'), league=league)
            home_team = get_object_or_404(Team, name=request.POST.get('home_team'), league=league)
            away_team = get_object_or_404(Team, name=request.POST.get('away_team'), league=league)
            season = get_object_or_404(Season, id=season_id)
            
            game = Game(created_by=request.user,
                        date=date,
                        winner=winner,
                        loser=loser,
                        home_team=home_team,
                        away_team=away_team,
                        season=season,
                        league=league)
            game.save()

            messages.success(request, f"Game between {game.home_team} and {game.away_team} on {game.date} created successfully")
        else:
            messages.error(request, "You cannot add this game as you do not own the league")

    return HttpResponseRedirect(reverse('rpiapp:season_details', kwargs={"season_id" : season_id,
                                                                             "league_id" : league_id}))

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