from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_protect
from django.contrib.sessions.models import Session
from django.utils import timezone
import logging
import json
from blackjack_app.models import User, GameSession
from blackjack_app.forms import RegistrationForm, LoginForm

logger = logging.getLogger(__name__)


def home(request):
    """Home page - redirect to login if not authenticated"""
    if 'user_id' in request.session:
        return redirect('blackjack_app:game')
    return redirect('blackjack_app:login')


@require_http_methods(["GET", "POST"])
@csrf_protect
def register(request):
    """User registration with secure password hashing"""
    if request.method == 'GET':
        form = RegistrationForm()
        return render(request, 'register.html', {'form': form})
    
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            try:
                # Extract validated data
                email = form.cleaned_data['email']
                name = form.cleaned_data['name']
                password = form.cleaned_data['password']
                
                # Check if user already exists
                if User.objects.filter(email=email).exists():
                    form.add_error('email', 'Cet email est déjà utilisé.')
                    return render(request, 'register.html', {'form': form})
                
                # Create user with bcrypt-hashed password
                user = User(email=email, name=name)
                user.set_password(password)  # Uses bcrypt
                user.save()
                
                logger.info(f"Nouvel utilisateur créé: {email}")
                
                # Redirect to login
                return redirect('blackjack_app:login')
            
            except Exception as e:
                logger.error(f"Erreur lors de l'inscription: {str(e)}")
                # Show generic error to user
                return render(request, 'register.html', {
                    'form': form,
                    'error': 'Une erreur est survenue. Veuillez réessayer.'
                })
        
        return render(request, 'register.html', {'form': form})


@require_http_methods(["GET", "POST"])
@csrf_protect
def login(request):
    """User login with generic error messages"""
    if request.method == 'GET':
        form = LoginForm()
        return render(request, 'login.html', {'form': form})
    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            try:
                email = form.cleaned_data['email']
                password = form.cleaned_data['password']
                
                # Query user by email
                try:
                    user = User.objects.get(email=email)
                except User.DoesNotExist:
                    logger.warning(f"Tentative de connexion avec email inexistant: {email}")
                    # Generic error message for security
                    form.add_error(None, 'Email ou mot de passe incorrect.')
                    return render(request, 'login.html', {'form': form})
                
                # Verify password using bcrypt
                if not user.check_password(password):
                    logger.warning(f"Tentative de connexion échouée pour: {email}")
                    form.add_error(None, 'Email ou mot de passe incorrect.')
                    return render(request, 'login.html', {'form': form})
                
                # Create secure session
                request.session['user_id'] = user.id
                request.session['email'] = user.email
                request.session['name'] = user.name
                request.session['role'] = user.role
                request.session.set_expiry(1800)  # 30 minutes
                
                logger.info(f"Utilisateur connecté: {email}")
                return redirect('blackjack_app:game')
            
            except Exception as e:
                logger.error(f"Erreur lors de la connexion: {str(e)}")
                return render(request, 'login.html', {
                    'form': form,
                    'error': 'Une erreur est survenue. Veuillez réessayer.'
                })
        
        return render(request, 'login.html', {'form': form})


@require_http_methods(["GET"])
def logout(request):
    """Logout - destroy session"""
    user_email = request.session.get('email', 'Unknown')
    request.session.flush()  # Destroy session completely
    logger.info(f"Utilisateur déconnecté: {user_email}")
    return redirect('blackjack_app:login')


def is_authenticated(request):
    """Check if user is authenticated"""
    return 'user_id' in request.session


def require_login(view_func):
    """Decorator to require login for a view"""
    def wrapper(request, *args, **kwargs):
        if not is_authenticated(request):
            return redirect('blackjack_app:login')
        return view_func(request, *args, **kwargs)
    return wrapper


def require_admin(view_func):
    """Decorator to require admin role"""
    def wrapper(request, *args, **kwargs):
        if not is_authenticated(request):
            return redirect('blackjack_app:login')
        if request.session.get('role') != 'admin':
            return render(request, '403.html', status=403)
        return view_func(request, *args, **kwargs)
    return wrapper


@require_login
def game(request):
    """Blackjack game page"""
    user_id = request.session.get('user_id')
    user_name = request.session.get('name')
    
    try:
        user = User.objects.get(id=user_id)
        # Get or create current game session
        game_session, created = GameSession.objects.get_or_create(
            user=user,
            status='active',
            defaults={
                'balance': 1000,
                'bet_amount': 10,
            }
        )
        
        return render(request, 'game.html', {
            'user_name': user_name,
            'balance': game_session.balance,
            'bet_amount': game_session.bet_amount,
        })
    except User.DoesNotExist:
        request.session.flush()
        return redirect('blackjack_app:login')
    except Exception as e:
        logger.error(f"Erreur au chargement du jeu: {str(e)}")
        return render(request, 'game.html', {
            'error': 'Une erreur est survenue.'
        })


@require_admin
def admin_dashboard(request):
    """Admin dashboard - view all users"""
    try:
        users = User.objects.all().order_by('-created_at')
        return render(request, 'admin_dashboard.html', {
            'users': users,
            'total_users': users.count(),
        })
    except Exception as e:
        logger.error(f"Erreur dans l'admin dashboard: {str(e)}")
        return render(request, 'admin_dashboard.html', {
            'error': 'Une erreur est survenue.'
        })


def legal(request):
    """Legal and privacy policy page"""
    return render(request, 'legal.html')


def error_403(request, exception=None):
    """Handle 403 Forbidden errors"""
    return render(request, '403.html', status=403)


def error_404(request, exception=None):
    """Handle 404 Not Found errors"""
    return render(request, '404.html', status=404)


def error_500(request):
    """Handle 500 Internal Server errors"""
    logger.error("Erreur interne du serveur 500")
    return render(request, '500.html', status=500)
