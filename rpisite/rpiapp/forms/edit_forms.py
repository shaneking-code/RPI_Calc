from django import forms
from ..models import League, Team, Season, Game

class EditLeagueForm(forms.ModelForm):
    class Meta:
        model = League
        exclude = ('created_by',)

class EditTeamForm(forms.ModelForm):
    class Meta:
        model = Team
        exclude = ('created_by', 'league',)

class EditSeasonForm(forms.ModelForm):
    class Meta:
        model = Season
        exclude = ('created_by', 'league',)

class EditGameForm(forms.ModelForm):

    class Meta:
        model = Game
        fields = ('date','winner','loser','home_team','away_team')
    
    def __init__(self, *args, **kwargs):
        instance = kwargs['instance']
        super(EditGameForm, self).__init__(*args, **kwargs)
        self.fields['date'] = forms.DateField(widget=forms.widgets.SelectDateWidget(years=range(instance.season.start_date.year, instance.season.end_date.year+1)))
        self.fields['winner'].queryset = instance.season.league.teams.all().order_by("name")
        self.fields['loser'].queryset = instance.season.league.teams.all().order_by("name")
        self.fields['home_team'].queryset = instance.season.league.teams.all().order_by("name")
        self.fields['away_team'].queryset = instance.season.league.teams.all().order_by("name")