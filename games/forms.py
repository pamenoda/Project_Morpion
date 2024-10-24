# Dans forms.py pour l'application games
from django import forms
from .models import Game

# corey schafer vidéo 
class GameForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = ['title', 'public', 'board_size', 'alignment_length']
#chatgpt 
class JoinGameForm(forms.Form):
    access_code = forms.CharField(max_length=8)