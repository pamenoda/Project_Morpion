# Dans urls.py pour l'application games
from django.urls import path
from .views import CreateGame,GameDetail,GameUpdate,GameDelete,join_Game,GameBoardView,post_Data,get_Board,surrender_game,statistics_player,game_finished

urlpatterns = [
    # chemin liaison entre view et template
    path('create/', CreateGame.as_view(), name="create-game"),
    path('<int:pk>/',GameDetail.as_view(),name="game-detail"),
    path('<int:pk>/update/', GameUpdate.as_view(), name="game-update"),
    path('<int:pk>/delete/', GameDelete.as_view(), name="game-delete"),
    path('<int:game_id>/join/', join_Game, name='join-game'),
    path('<int:pk>/board/', GameBoardView.as_view(), name='game-board'),
    path('<int:pk>/board/post-data/',post_Data , name='post-data'),
    path('<int:pk>/board/get-board/',get_Board,name="get-board"),
    path('<int:pk>/board/surrender_game/',surrender_game,name="surrender-game"),
    path('statistics/',statistics_player,name="statistics-player"),
    path('<int:pk>/board/game_finished/',game_finished,name="game-finished")
    
]
