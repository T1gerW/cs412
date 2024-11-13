from django import forms
from .models import Voter

class VoterFilterForm(forms.Form):
    # Updated Party Affiliation Choices
    PARTY_CHOICES = [
        ('U', 'U'), ('D', 'D'), ('R', 'R'), ('J', 'J'), ('A', 'A'), 
        ('CC', 'CC'), ('X', 'X'), ('L', 'L'), ('Q', 'Q'), ('S', 'S'), 
        ('FF', 'FF'), ('G', 'G'), ('HH', 'HH'), ('T', 'T'), ('AA', 'AA'), 
        ('GG', 'GG'), ('Z', 'Z'), ('O', 'O'), ('P', 'P'), ('E', 'E'), 
        ('V', 'V'), ('H', 'H'), ('Y', 'Y'), ('W', 'W'), ('EE', 'EE'), 
        ('K', 'K')
    ]
    party_affiliation = forms.ChoiceField(choices=PARTY_CHOICES, required=False)

    # Other filters as before
    BIRTH_YEAR_CHOICES = [(year, year) for year in range(1920, 2024)]
    min_birth_year = forms.ChoiceField(choices=BIRTH_YEAR_CHOICES, required=False, label="Min Year of Birth")
    max_birth_year = forms.ChoiceField(choices=BIRTH_YEAR_CHOICES, required=False, label="Max Year of Birth")
    VOTER_SCORE_CHOICES = [(i, i) for i in range(0, 6)]
    voter_score = forms.ChoiceField(choices=VOTER_SCORE_CHOICES, required=False)
    v20state = forms.BooleanField(required=False, label="v20state", initial= False)
    v21town = forms.BooleanField(required=False, label="v21town", initial= False)
    v22primary = forms.BooleanField(required=False, label="v21primary", initial= False)
    v22general = forms.BooleanField(required=False, label="v22general", initial= False)
    v23town = forms.BooleanField(required=False, label="v23town", initial= False)

