"""
Update the Django URL configuration to include the app URLs
"""
from django.urls import path, include
from blackjack_app import views

handler403 = 'blackjack_app.views.error_403'
handler404 = 'blackjack_app.views.error_404'
handler500 = 'blackjack_app.views.error_500'

urlpatterns = [
    path('', include('blackjack_app.urls')),
]
