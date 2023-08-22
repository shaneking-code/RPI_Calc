from django import forms
from datetime import datetime
from ..models import League, Team, Season, Game

class AddLeagueForm(forms.ModelForm):
    name = forms.CharField(label='Name', widget=forms.TextInput(attrs={'placeholder':'Your League'}))
    sport = forms.CharField(label='Sport', widget=forms.TextInput(attrs={'placeholder':'Baseball'}))
    class Meta:
        model = League
        exclude = ['created_by']

class AddTeamForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'placeholder' : 'Your Team'}))
    class Meta:
        model = Team
        fields = ['name',]

class AddSeasonForm(forms.ModelForm):
    class Meta:
        model = Season
        exclude = ['created_by','league']
    
    def __init__(self, *args, **kwargs):
        super(AddSeasonForm, self).__init__(*args, **kwargs)
        self.fields['start_date'] = forms.DateField(initial=datetime.now(),
                                                    widget=forms.widgets.SelectDateWidget(years=range(datetime.now().year - 50, datetime.now().year + 6)))
        self.fields['end_date'] = forms.DateField(initial=datetime.now(),
                                                  widget=forms.widgets.SelectDateWidget(years=range(datetime.now().year - 50, datetime.now().year + 6)))
        self.fields['name'] = forms.CharField(widget=forms.TextInput(attrs={'placeholder':f'{datetime.now().year} - {datetime.now().year+1}'}))

        self.fields['wp_weight'].required = False
        self.fields['owp_weight'].required = False
        self.fields['oowp_weight'].required = False
        self.fields['high_weight'].required = False
        self.fields['low_weight'].required = False
        
class AddGameForm(forms.ModelForm):

    def __init__(self, *args, season, **kwargs):
        super(AddGameForm, self).__init__(*args, **kwargs)
        self.fields['date'].widget = forms.SelectDateWidget(years=range(season.start_date.year, season.end_date.year+1))
        self.fields['winner'].queryset = Team.objects.filter(league=season.league).order_by("name")
        self.fields['loser'].queryset = Team.objects.filter(league=season.league).order_by("name")
        self.fields['home_team'].queryset = Team.objects.filter(league=season.league).order_by("name")
        self.fields['away_team'].queryset = Team.objects.filter(league=season.league).order_by("name")

    class Meta:
        model = Game
        fields = ['date','winner','loser','home_team','away_team',]
