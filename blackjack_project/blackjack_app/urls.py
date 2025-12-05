from django.urls import path, re_path
from . import views, api_views

app_name = 'blackjack_app'

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('game/', views.game, name='game'),
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('legal/', views.legal, name='legal'),
    
    # API endpoints
    path('api/game/start/', api_views.start_game, name='api_start_game'),
    path('api/game/hit/', api_views.hit, name='api_hit'),
    path('api/game/stand/', api_views.stand, name='api_stand'),
    path('api/game/reset/', api_views.reset_game, name='api_reset_game'),
]
