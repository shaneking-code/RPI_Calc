from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.contrib.auth.models import User
from ..models import League, Team, Game


def user_search(request):

    if request.method == 'POST':
        search_term = request.POST.get('user_search_term')
        search_results = User.objects.filter(username__contains=search_term)

        context = {
            "search_term" : search_term,
            "search_results" : search_results,
            "referer" : request.META.get('HTTP_REFERER')
        }

        return render(request, "rpiapp/search_templates/user_search.html", context)
    
def league_search(request):

    if request.method == 'POST':
        search_term = request.POST.get('league_search_term')
        search_results = League.objects.filter(name__contains=search_term)

        context = {
            "search_term" : search_term,
            "search_results" : search_results,
            "referer" : request.META.get('HTTP_REFERER')
        }

        return render(request, "rpiapp/search_templates/league_search.html", context)

# Search for a team
def team_search(request, league_id):

    if request.method == 'POST':
        search_term = request.POST.get('search_term')
        search_results = Team.objects.filter(Q(league__id=league_id) & Q(name__contains=search_term))
        league = get_object_or_404(League, id=league_id)

        context = {
            "search_term" : search_term,
            "search_results" : search_results,
            "league" : league, 
            "referer" : request.META.get('HTTP_REFERER')
        }

        return render(request, "rpiapp/search_templates/team_search.html", context)

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
            "referer" : request.META.get('HTTP_REFERER')
        }

        return render(request, "rpiapp/search_templates/game_search.html", context)
