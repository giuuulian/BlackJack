from django.contrib import admin
from blackjack_app.models import User, GameSession

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'name', 'role', 'created_at')
    list_filter = ('role', 'created_at')
    search_fields = ('email', 'name')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(GameSession)
class GameSessionAdmin(admin.ModelAdmin):
    list_display = ('user', 'status', 'bet_amount', 'balance', 'created_at')
    list_filter = ('status', 'created_at')
    readonly_fields = ('created_at', 'updated_at')
