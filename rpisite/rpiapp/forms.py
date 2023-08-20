from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from datetime import datetime
from .models import League, Team, Season, Game

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username','email','password1','password2')

class EditUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username','email')

class AddLeagueForm(forms.ModelForm):
    name = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder':'Your League'}))
    class Meta:
        model = League
        fields = ['name',]

class AddTeamForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'placeholder' : 'Your Team'}))
    class Meta:
        model = Team
        fields = ['name',]

class AddSeasonForm(forms.ModelForm):
    class Meta:
        model = Season
        fields = ['start_date','end_date','name']
    
    def __init__(self, *args, **kwargs):
        super(AddSeasonForm, self).__init__(*args, **kwargs)
        self.fields['start_date'] = forms.DateField(initial=datetime.now(),
                                                    widget=forms.widgets.SelectDateWidget(years=range(datetime.now().year - 50, datetime.now().year + 6)))
        self.fields['end_date'] = forms.DateField(initial=datetime.now(),
                                                  widget=forms.widgets.SelectDateWidget(years=range(datetime.now().year - 50, datetime.now().year + 6)))
        self.fields['name'] = forms.CharField(widget=forms.TextInput(attrs={'placeholder':f'{datetime.now().year} - {datetime.now().year+1}'}))
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





