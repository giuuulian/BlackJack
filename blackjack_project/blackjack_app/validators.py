from django.core.exceptions import ValidationError

class CustomPasswordValidator:
    """
    Validate password strength:
    - Minimum 12 characters
    - At least 3 of: uppercase, lowercase, digits, special chars
    """
    def validate(self, password, user=None):
        import re
        
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
                "Le mot de passe doit contenir au moins 3 types de caractères.",
                code='password_weak',
            )
    
    def get_help_text(self):
        return "Minimum 12 caractères et 3 types de caractères requis."
