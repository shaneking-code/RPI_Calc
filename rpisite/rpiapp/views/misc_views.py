from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from ..models import Team, Season, Game
from ..utils.bulk_rpi import bulk_create_games
import csv
import datetime

@login_required
def bulk_game_upload(request, league_id, season_id):

    season = get_object_or_404(Season, id=season_id)
    league = season.league

    if request.method == 'POST':
        games_csv = request.FILES.get('games_csv')
        decoded_games_csv = games_csv.read().decode('utf-8').splitlines()
        games_csv_reader = csv.reader(decoded_games_csv, delimiter=",")
        next(games_csv_reader)
        games = []
        for row in games_csv_reader:
            date = datetime.datetime.strptime(row[0], '%m/%d/%Y').date()
            if date < season.start_date or date > season.end_date:
                messages.error(request, f"Contains game outside of date range ({season.start_date})-({season.end_date})")
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            home_team, ht_created = Team.objects.get_or_create(name=row[3], league=league, created_by=request.user)
            away_team, at_created = Team.objects.get_or_create(name=row[4], league=league, created_by=request.user)
            winner, w_created = Team.objects.get_or_create(name=row[1], league=league, created_by=request.user)
            loser, l_created = Team.objects.get_or_create(name=row[2], league=league, created_by=request.user)
            created_by = request.user
            game = Game(
                created_by = created_by,
                date = date,
                home_team = home_team,
                away_team=away_team,
                winner=winner,
                loser=loser,
                season=season,
                league=league,
                bulk_processing=True
            )
            games.append(game)
            if w_created:
                messages.success(request, f"Team '{winner}' created")
            if l_created:
                messages.success(request, f"Team '{loser}' created")
            if ht_created:
                messages.success(request, f"Team '{home_team}' created")
            if at_created:
                messages.success(request, f"Team '{away_team}' created")
        bulk_create_games(season, games, True)
        messages.success(request, "Games imported successfully")
        return HttpResponseRedirect(reverse('rpiapp:season_details', kwargs={"league_id":league.id,
                                                                             "season_id":season.id}))
    
    context = {
        "season" : season
    }
    return render(request, "rpiapp/misc_templates/add_games_bulk.html", context)