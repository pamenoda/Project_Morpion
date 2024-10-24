from django.urls import path
from .views import HomeView


urlpatterns = [
    path('', HomeView.as_view(), name='core-home'), #chemin de la page d'accueil
]
