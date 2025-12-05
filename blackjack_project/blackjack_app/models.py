from django.db import models
from django.contrib.auth.hashers import make_password
import bcrypt

class User(models.Model):
    ROLE_CHOICES = [
        ('user', 'User'),
        ('admin', 'Admin'),
    ]
    
    email = models.EmailField(unique=True, max_length=254)
    name = models.CharField(max_length=255)
    password_hash = models.CharField(max_length=255)  
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'users'
        indexes = [
            models.Index(fields=['email']),
        ]
    
    def set_password(self, raw_password):
        """Hash password with bcrypt before storing"""
        salt = bcrypt.gensalt(rounds=12)
        self.password_hash = bcrypt.hashpw(
            raw_password.encode('utf-8'), 
            salt
        ).decode('utf-8')
    
    def check_password(self, raw_password):
        """Verify password against bcrypt hash"""
        return bcrypt.checkpw(
            raw_password.encode('utf-8'), 
            self.password_hash.encode('utf-8')
        )
    
    def is_admin(self):
        return self.role == 'admin'
    
    def __str__(self):
        return self.email


class GameSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='game_sessions')
    player_hand = models.JSONField(default=list)
    dealer_hand = models.JSONField(default=list)
    player_score = models.IntegerField(default=0)
    dealer_score = models.IntegerField(default=0)
    status = models.CharField(max_length=20, default='active') 
    bet_amount = models.IntegerField(default=10)
    balance = models.IntegerField(default=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'game_sessions'
    
    def __str__(self):
        return f"{self.user.email} - {self.status}"
