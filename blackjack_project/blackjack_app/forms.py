from django import forms
from django.core.exceptions import ValidationError
import re

class PasswordValidator:
    """
    Validate password strength:
    - Minimum 12 characters
    - At least 3 of: uppercase, lowercase, digits, special chars
    """
    def __init__(self):
        pass
    
    def validate(self, password, user=None):
        if len(password) < 12:
            raise ValidationError(
                "Le mot de passe doit contenir au moins 12 caractères.",
                code='password_too_short',
            )
        
        has_upper = bool(re.search(r'[A-Z]', password))
        has_lower = bool(re.search(r'[a-z]', password))
        has_digit = bool(re.search(r'[0-9]', password))
        has_special = bool(re.search(r'[!@#$%^&*()_+\-=\[\]{};:\'",.<>?]', password))
        
        count = sum([has_upper, has_lower, has_digit, has_special])
        
        if count < 3:
            raise ValidationError(
                "Le mot de passe doit contenir au moins 3 types de caractères "
                "(majuscules, minuscules, chiffres, caractères spéciaux).",
                code='password_no_upper_or_lower',
            )
    
    def get_help_text(self):
        return "Votre mot de passe doit contenir au moins 12 caractères et 3 types de caractères."


class RegistrationForm(forms.Form):
    email = forms.EmailField(
        label='Email',
        max_length=254,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'exemple@email.com'
        })
    )
    name = forms.CharField(
        label='Nom',
        max_length=255,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Votre nom'
        })
    )
    password = forms.CharField(
        label='Mot de passe',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Min 12 caractères, 3 types requis'
        })
    )
    consent = forms.BooleanField(
        label='J\'accepte que mes données soient utilisées pour la création de compte et la gestion de mon profil.',
        required=True,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        })
    )
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        from blackjack_app.models import User
        if User.objects.filter(email=email).exists():
            raise ValidationError("Cet email est déjà utilisé.")
        return email
    
    def clean_name(self):
        name = self.cleaned_data.get('name')
        if len(name.strip()) < 2:
            raise ValidationError("Le nom doit contenir au moins 2 caractères.")
        return name.strip()
    
    def clean_password(self):
        password = self.cleaned_data.get('password')
        validator = PasswordValidator()
        validator.validate(password)
        return password


class LoginForm(forms.Form):
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'exemple@email.com'
        })
    )
    password = forms.CharField(
        label='Mot de passe',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Votre mot de passe'
        })
    )
