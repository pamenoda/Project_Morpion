from django.views.generic import TemplateView
from games.models import Game

class HomeView(TemplateView):
    template_name = 'core/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['games'] = Game.objects.all()  # Récupérez tous les objets Game

        if self.request.user.is_authenticated:
            context['user_created_games'] = Game.get_user_created_games(Game,self.request.user)
        else:
            context['user_created_games'] = []

        return context


