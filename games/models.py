from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.

# Définition du modèle de données pour les parties de jeu
class Game(models.Model):
    
    title = models.CharField(max_length=255) # Champ pour stocker le titre de la partie (maximum 255 caractères)
    creator = models.ForeignKey(User, on_delete=models.CASCADE) # Champ pour stocker le créateur de la partie, lié au modèle User de Django
    opponent = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='opponent')
    public = models.BooleanField(default=True) # Champ pour indiquer si la partie est publique ou privée (par défaut, publique)
    board_size = models.PositiveIntegerField(default=3) # Champ pour définir la taille du plateau de jeu (par défaut, 3x3 pour un tic-tac-toe)
    alignment_length = models.PositiveIntegerField(default=3) # Champ pour définir la longueur nécessaire pour gagner le jeu (par défaut, 3 pour un tic-tac-toe)
    code = models.CharField(max_length=8, blank=True, null=True) # Champ pour stocker le code d'accès pour les parties privées (max 8 caractères, facultatif)
    created_at = models.DateTimeField(auto_now_add=True) # Champ pour enregistrer la date et l'heure de création de la partie (auto-généré)
    finished = models.BooleanField(default=False) # on veut voir si la partie est finie ou pas
    symbol_creator = models.URLField(null=True, blank=True) # symbol du créateur
    symbol_opponent = models.URLField(null=True, blank=True) # symbol de l'opposant
    current_player = models.CharField(max_length=50,default='') # joueur entraint de joueur 
    board_state = models.JSONField() # matrice de type jsonfield que l'on initialise par la suite
    surrender = models.BooleanField(default=False) # booléen pour l'abandon 
    winner = models.CharField(max_length=255, null=True, blank=True) # et le nom du winner
    

    # Nouveau champ pour indiquer si la partie est en attente de joueur
    waiting_for_player = models.BooleanField(default=True) 

    #chatgpt
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    # initialise la matrice avec la taille récupérer du formulaire de création
    def initialize_board_state(self):
        if not self.board_state:
            self.board_state = [[None for _ in range(self.board_size)] for _ in range(self.board_size)]
        self.save()
            

    #moi même je met a jour la matrice avec le clique du joueur
    #fonction appelé dans la view qui traite la requete ajax post row col value
    def update_Grid(self,row,col,value):
        self.board_state[row-1][col-1] = value
        if value == self.creator.username : self.current_player = self.opponent.username
        else: self.current_player = self.creator.username
      
    #coreyschafer récupérer le créateur
    def get_user_created_games(cls, user):
        return cls.objects.filter(creator=user)
    
    #tostring 
    def __str__(self):
        return self.title

    #corey schafer
    def get_absolute_url(self):
        return reverse('game-detail',kwargs={'pk': self.pk})
    
    #chatgpt 
    #si le joueur a rejoint on appelle cette fonction dans la vue qui traite le join 
    def invite_opponent(self, user):
        if self.waiting_for_player:
            self.opponent = user
            # Définir les URL des images de profill
            self.symbol_creator = self.creator.profile.symbol.url
            self.symbol_opponent = user.profile.symbol.url
            self.waiting_for_player = False
            self.save()

    #moi même 
    def get_board(self):
        """
        Retourne une liste de listes représentant un plateau de jeu vide.
        """
        return self.board_state
    
   
   
