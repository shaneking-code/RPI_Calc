from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import League, Team, Season, Game

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username','email','password1','password2')

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
        self.fields['date'] = forms.DateField(widget=forms.widgets.SelectDateWidget(years=range(instance.season.year, instance.season.year+1)))
        self.fields['winner'].queryset = instance.season.league.teams.all()
        self.fields['loser'].queryset = instance.season.league.teams.all()
        self.fields['home_team'].queryset = instance.season.league.teams.all()
        self.fields['away_team'].queryset = instance.season.league.teams.all()





