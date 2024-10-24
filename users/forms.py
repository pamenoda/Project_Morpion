# Importation des modules nécessaires
from django import forms  # Importe le module forms de Django pour créer des formulaires
from django.contrib.auth.models import User  # Importe le modèle User pour gérer les utilisateurs
from django.contrib.auth.forms import UserCreationForm  # Importe la classe UserCreationForm pour la création d'utilisateurs
from .models import Profile  # Importe le modèle Profile du même répertoire

class UserRegisterForm(UserCreationForm):
    # Formulaire d'inscription d'utilisateur avec des champs supplémentaires
    email = forms.EmailField()  # Ajoute un champ email au formulaire

    class Meta:
        model = User  # Utilise le modèle User de Django
        fields = ['username', 'email', 'password1', 'password2']  # Spécifie les champs du formulaire

class UserUpdateForm(forms.ModelForm):
    # Formulaire de mise à jour des informations de l'utilisateur
    email = forms.EmailField()  # Ajoute un champ email au formulaire

    class Meta:
        model = User  # Utilise le modèle User de Django
        fields = ['username', 'email']  # Spécifie les champs du formulaire

class ProfileUpdateForm(forms.ModelForm):
    # Formulaire de mise à jour des informations du profil utilisateur
    class Meta:
        model = Profile  # Utilise le modèle Profile du même répertoire
        fields = ['image','symbol']  # Spécifie les champs du formulaire
    
