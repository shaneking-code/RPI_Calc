from django.contrib import admin
from .models import League, Team, Season, Game
# Register your models here.

@admin.register(League)
class LeagueAdmin(admin.ModelAdmin):
    fields = ["name"]

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    fields = ["name","league"]

@admin.register(Season)
class SeasonAdmin(admin.ModelAdmin):
    fields = ["year","league"]

