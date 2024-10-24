# Dans views.py pour l'application games
from django.shortcuts import redirect, render,get_object_or_404
from django.views import View
from django.views.generic import CreateView,DetailView,UpdateView,DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from .models import Game
from .forms import GameForm,JoinGameForm
from django.contrib import messages
from django.urls import reverse
import random
import string
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from datetime import timedelta
from datetime import datetime
from django.db.models import Q



    
#corey schafer
def home(request):
    #retrouve toutes les games et toutes les games de l'user
    games = Game.objects.all()
    user_created_games = []

    if request.user.is_authenticated:
        user_created_games = Game.get_user_created_games(request.user)

    return render(request, 'core/home.html', {'games': games, 'user_created_games': user_created_games})

#corey Schafer 
class CreateGame(LoginRequiredMixin,CreateView):
    # View pour créer une nouvelle game
    model = Game
    form_class = GameForm 
    template_name = "games/create_game.html"

    def form_valid(self, form):
        form.instance.creator = self.request.user
        form.instance.current_player = self.request.user.username
        alignment_length = form.cleaned_data.get('alignment_length')
        board_size = form.cleaned_data.get('board_size')

        #existing_game = Game.objects.filter(creator=self.request.user,finished=False).first()

       # if existing_game:
       #     return HttpResponseRedirect(reverse('game-detail', kwargs={'pk': existing_game.pk}))
        
        
        # Générer un code d'accès aléatoire (8 caractères) chatgpt
        code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        
        form.instance.code = code

        # Nouvelle partie en attente d'un joueur ma logique
        form.instance.waiting_for_player = True

        # ma logique pour vérifier si l'alignement est supérieur à la taille 
        if alignment_length > board_size:
            form.add_error('alignment_length', 'Alignment length cannot be greater than board size.')
            return self.form_invalid(form)
        # Appeler la méthode d'initialisation du plateau de jeu du modèle
        form.instance.initialize_board_state()
        return super().form_valid(form)
    # renvoi le créateur dans le menu pour modifier supprimer ou jouer la game
    def get_success_url(self): 
        return reverse('game-detail', kwargs={'pk': self.object.id})
  

#coreySchafer vue de la game dans le menu de modification 
class GameDetail(DetailView):
    model = Game
    template_name = "games/game_detail.html"


    
#coreyschafer permet de modifier la game 
class GameUpdate(LoginRequiredMixin,UserPassesTestMixin, UpdateView):
    model = Game
    # champ modifiable
    fields = ['title', 'public', 'board_size', 'alignment_length']
    # vérifie le formulaire renvoyé par l'user
    def form_valid(self, form):
        form.instance.creator = self.request.user
        # Vérifier si alignment_length est supérieur à board_size
        alignment_length = form.cleaned_data.get('alignment_length')
        board_size = form.cleaned_data.get('board_size')
        # vérifie si alignement est supérieur a la taille d'une ligne du plateau 
        if alignment_length > board_size:
            form.add_error('alignment_length', 'Alignment length cannot be greater than board size.')
            return self.form_invalid(form)
        
        return super().form_valid(form)
    """
    La méthode test_func dans la classe GameUpdate est une méthode spéciale utilisée avec la classe UserPassesTestMixin 
    dans le contexte des vues  de Django. 
    Son objectif est de fournir une logique pour tester si un utilisateur a le droit d'accéder à une vue particulière.
     en l'occurence on vérifie bien que le créateur de la game est celui qui veut l'update
    """
    def test_func(self) :
        game = self.get_object()
        if self.request.user == game.creator:
            return True
        return False

#coreyschafer
class GameDelete(LoginRequiredMixin,UserPassesTestMixin,DeleteView):

    model = Game
    success_url ="/"
    # on supprime la game on n'a plus accès a celle ci en faisant ca 
    # meme vérification que avant de la modification 
    def test_func(self) :
        game = self.get_object()
        if self.request.user == game.creator:
            return True
        return False
"""
moi même 
view qui traite la requete ajax post pour mettre a jour la matrice dans le model 
on récupère row et col et le nom du joueur en string
"""
@csrf_exempt   
def post_Data(request,pk):
    if request.method == "POST":
        game = get_object_or_404(Game,id=pk)
        row = int(request.POST.get('row'))
        col = int(request.POST.get('col'))
        value = request.POST.get('value')
        if request.user.username == value:
            game.update_Grid(row,col,value)
            game.save()
            return JsonResponse({'messages':"message"})
        else:
            return JsonResponse({'message':"ce n'est pas votre tour"})
"""  
moi même
view qui traite la requete ajax get pour mettre a jour la vue graphique du jeu         
"""
def get_Board(request,pk):
    game = get_object_or_404(Game,id=pk)
    if request.method =="GET":
        if game.waiting_for_player == False:
            if game.surrender:
                user = User.objects.get(username=game.winner)
                if user == request.user:
                    if game.winner == game.creator.username:
                        messages.warning(request,f"you won against {game.opponent} by surrender")
                    else:
                        messages.warning(request,f"you won against {game.creator} by surrender")

            game_data = {
                'board':game.get_board(),
                'activePlayer': game.current_player,
                'boardSize': game.board_size,  
                'symbolCreator': game.symbol_creator,
                'symbolOpponent': game.symbol_opponent,
                'winner' : game.winner,
                'surrender':game.surrender,
                'opponent':game.opponent.username,
                'alignement':game.alignment_length
            }

            return JsonResponse({'game':game_data})
        else:
            return JsonResponse({"message":"waiting for player"})
        
# méthode appeler lorsque la game est finie   
@csrf_exempt 
def game_finished(request,pk):
    game = get_object_or_404(Game,id=pk)
    game.finished = True
    game.save()
    return JsonResponse({"msg": "game finished"})

# requete ajax post qui est  traité par la view au cas ou un joueur décide d'abandonner 
@csrf_exempt # moi même 
def surrender_game(request,pk):
    if request.method =="POST":
        game = get_object_or_404(Game,id=pk)
        game.surrender = True
        game.finished = True
        if request.user.username == game.creator.username:
            game.winner = game.opponent.username
        elif request.user.username == game.opponent.username:
            game.winner = game.creator.username
        else:
            return JsonResponse({'message': 'Unauthorized'}, status=401)
        
        game.save()
        # Redirection vers l'accueil
        return JsonResponse({'sucess':'successs'})
     
    return JsonResponse({'message': 'error incorrect'})

# view qui renvoi les données necessaire a la page statistics.html 
def statistics_player(request):
    template_name = 'games/statistics.html' 
    #https://www.w3schools.com/python/python_datetime.asp
    actual_date = datetime.now()
    month = actual_date.month
    year = actual_date.year
    first_day = datetime(year,month,1)
    last_day = datetime(year,month,31)

    
    length = (last_day-first_day).days + 1

    #blackbox IA
    
    day_labels = []
    games_played = []

    for i in range(length):
        current_date = first_day + timedelta(days=i)
        #coreySchafer
        games= Game.objects.filter(Q(created_at__date=current_date.date(),creator=request.user) 
                                   | Q(created_at__date=current_date.date(),opponent=request.user)).filter(finished=True)
        
        day_labels.append(current_date.day)
        games_played.append(games.count())

    return render(request,template_name,{'dayLabels': day_labels, 'gamesPlayed': games_played})

"""
code géneré  par chatgpt 
permet de gerer le cas ou un joueur décide de rejoindre la game  
"""
def join_Game(request, game_id):
    game = get_object_or_404(Game, id=game_id)

    if game.waiting_for_player:
        # Si la partie est publique ou l'utilisateur fournit le code d'accès correct
        if game.public or (request.method == 'POST' and request.POST.get('access_code') == game.code):
            game.invite_opponent(request.user)

            # Redirigez l'utilisateur vers la page de détails de la partie
            return redirect('game-board', pk=game_id)
        else:
            form = JoinGameForm()
            return render(request, 'games/join_game.html', {'game': game, 'form': form})

    else:
        messages.error(request, 'Cette partie n\'est pas disponible pour rejoindre.')

    # Redirigez l'utilisateur vers la page d'accueil ou toute autre vue appropriée
    return redirect('core-home')

#coreyschafer view vue d'ensemble sur le plateau de django 
class GameBoardView(View):
    template_name = 'games/game_board.html'
    def get(self, request, *args, **kwargs):
        game = get_object_or_404(Game, pk=kwargs['pk'])
        return render(request, self.template_name, {'game': game})



