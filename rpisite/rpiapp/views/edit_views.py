from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from ..models import League, Team, Season, Game
from ..forms.edit_forms import EditLeagueForm, EditTeamForm, EditSeasonForm, EditGameForm

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
        if request.user != league_instance.created_by:
            messages.error(request, "You do not own this league")
            return HttpResponseRedirect(reverse('rpiapp:league_details', args=[league_instance.id]))
        form = EditLeagueForm(instance=league_instance)
    
    context = {
        "form" : form,
        "league" : league_instance,
    }

    return render(request, "rpiapp/edit_templates/edit_league.html", context)

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
        if request.user != team_instance.created_by:
            messages.error(request, "You do not own this team")
            return HttpResponseRedirect(reverse('rpiapp:team_details', kwargs={"league_id":team_instance.league.id,
                                                                               "team_id":team_instance.id}))
        form = EditTeamForm(instance=team_instance)
    
    context = {
        "form" : form,
        "team" : team_instance
    }

    return render(request, "rpiapp/edit_templates/edit_team.html", context)

@login_required
def edit_season(request, league_id, season_id):
    season_instance = get_object_or_404(Season, id=season_id)

    if request.method == 'POST' and (request.user == season_instance.created_by or request.user.is_superuser):
        form = EditSeasonForm(request.POST, instance=season_instance)
        if form.is_valid():
            form.save()
            messages.success(request, "Season updated successfully")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        if request.user != season_instance.created_by:
            messages.error(request, "You do not own this season")
            return HttpResponseRedirect(reverse('rpiapp:season_details', kwargs={'league_id':season_instance.league.id,
                                                                                 "season_id":season_instance.id}))
        form = EditSeasonForm(instance=season_instance)
    
    context = {
        "form" : form,
        "season" : season_instance
    }

    return render(request, "rpiapp/edit_templates/edit_season.html", context)

@login_required
def edit_game(request, league_id, season_id, game_id):

    game_instance = get_object_or_404(Game, id=game_id)

    if request.method == 'POST' and (game_instance.created_by == request.user or request.user.is_superuser):
        form = EditGameForm(request.POST, instance=game_instance)
        if form.is_valid():
            date = form.cleaned_data['date']
            if date < game_instance.season.start_date or date > game_instance.season.end_date:
                messages.error(request, f"Game outside of date range ({game_instance.season.start_date})-({game_instance.season.end_date})")
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            form.save()
            messages.success(request, "Game updated successfully")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        if request.user != game_instance.created_by:
            messages.error(request, "You do not own this game")
            return HttpResponseRedirect(reverse('rpiapp:game_details', kwargs={"league_id":game_instance.league.id,
                                                                                 "season_id":game_instance.season.id,
                                                                                 "game_id":game_instance.id}))
        form = EditGameForm(instance=game_instance)
    
    context = {
        "form" : form,
        "game" : game_instance
    }

    return render(request, "rpiapp/edit_templates/edit_game.html", context)
