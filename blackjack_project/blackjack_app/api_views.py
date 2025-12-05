from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_protect
from django.contrib.sessions.models import Session
from blackjack_app.models import User, GameSession
import json
import random
import logging

logger = logging.getLogger(__name__)

# Card deck
DECK = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']


def get_card_value(card):
    """Get the value of a card"""
    if card in ['J', 'Q', 'K']:
        return 10
    elif card == 'A':
        return 11
    else:
        return int(card)


def calculate_score(hand):
    """Calculate blackjack score"""
    total = 0
    aces = 0
    
    for card in hand:
        value = get_card_value(card)
        if card == 'A':
            aces += 1
        total += value
    
    # Adjust for aces
    while total > 21 and aces > 0:
        total -= 10
        aces -= 1
    
    return total


def is_authenticated(request):
    """Check if user session is valid"""
    return 'user_id' in request.session


def get_user_from_session(request):
    """Get user object from session"""
    try:
        user_id = request.session.get('user_id')
        if not user_id:
            return None
        return User.objects.get(id=user_id)
    except User.DoesNotExist:
        request.session.flush()
        return None


@require_http_methods(["POST"])
@csrf_protect
def start_game(request):
    """Start a new blackjack game"""
    if not is_authenticated(request):
        return JsonResponse({'error': 'Non authentifié'}, status=401)
    
    try:
        user = get_user_from_session(request)
        if not user:
            return JsonResponse({'error': 'Utilisateur non trouvé'}, status=404)
        
        data = json.loads(request.body)
        bet_amount = int(data.get('bet_amount', 10))
        
        # Validate bet
        if bet_amount < 1 or bet_amount > 1000:
            return JsonResponse({'error': 'Mise invalide'}, status=400)
        
        # Get or create game session
        game_session = GameSession.objects.create(
            user=user,
            bet_amount=bet_amount,
            balance=1000,
            status='active',
        )
        
        # Deal initial cards
        player_hand = [random.choice(DECK) for _ in range(2)]
        dealer_hand = [random.choice(DECK) for _ in range(2)]
        
        game_session.player_hand = player_hand
        game_session.dealer_hand = dealer_hand
        game_session.player_score = calculate_score(player_hand)
        game_session.dealer_score = calculate_score([dealer_hand[0]])  # Hide dealer's second card
        game_session.save()
        
        # Check for blackjack
        if game_session.player_score == 21:
            game_session.status = 'win'
            game_session.balance += int(game_session.bet_amount * 1.5)
            game_session.save()
            return JsonResponse({
                'status': 'win',
                'message': 'Blackjack !',
                'player_hand': game_session.player_hand,
                'dealer_hand': dealer_hand,  # Reveal all cards
                'player_score': game_session.player_score,
                'dealer_score': calculate_score(dealer_hand),
                'balance': game_session.balance,
            })
        
        return JsonResponse({
            'status': 'active',
            'player_hand': game_session.player_hand,
            'dealer_hand': [game_session.dealer_hand[0], '?'],  # Hide second card
            'player_score': game_session.player_score,
            'dealer_score': game_session.dealer_score,
            'balance': game_session.balance,
            'game_id': game_session.id,
        })
    
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Données JSON invalides'}, status=400)
    except Exception as e:
        logger.error(f"Erreur au démarrage du jeu: {str(e)}")
        return JsonResponse({'error': 'Erreur serveur'}, status=500)


@require_http_methods(["POST"])
@csrf_protect
def hit(request):
    """Player hits - draws another card"""
    if not is_authenticated(request):
        return JsonResponse({'error': 'Non authentifié'}, status=401)
    
    try:
        user = get_user_from_session(request)
        if not user:
            return JsonResponse({'error': 'Utilisateur non trouvé'}, status=404)
        
        data = json.loads(request.body)
        game_id = int(data.get('game_id'))
        
        # Verify user owns this game
        game_session = GameSession.objects.get(id=game_id, user=user)
        
        if game_session.status != 'active':
            return JsonResponse({'error': 'Le jeu est terminé'}, status=400)
        
        # Draw a card
        new_card = random.choice(DECK)
        game_session.player_hand.append(new_card)
        game_session.player_score = calculate_score(game_session.player_hand)
        
        # Check for bust
        if game_session.player_score > 21:
            game_session.status = 'loss'
            game_session.balance -= game_session.bet_amount
            game_session.save()
            
            return JsonResponse({
                'status': 'loss',
                'message': 'Vous avez dépassé 21. Vous avez perdu !',
                'player_hand': game_session.player_hand,
                'player_score': game_session.player_score,
                'balance': game_session.balance,
            })
        
        game_session.save()
        
        return JsonResponse({
            'status': 'active',
            'player_hand': game_session.player_hand,
            'player_score': game_session.player_score,
            'balance': game_session.balance,
        })
    
    except GameSession.DoesNotExist:
        return JsonResponse({'error': 'Jeu non trouvé'}, status=404)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Données JSON invalides'}, status=400)
    except Exception as e:
        logger.error(f"Erreur au hit: {str(e)}")
        return JsonResponse({'error': 'Erreur serveur'}, status=500)


@require_http_methods(["POST"])
@csrf_protect
def stand(request):
    """Player stands - dealer plays"""
    if not is_authenticated(request):
        return JsonResponse({'error': 'Non authentifié'}, status=401)
    
    try:
        user = get_user_from_session(request)
        if not user:
            return JsonResponse({'error': 'Utilisateur non trouvé'}, status=404)
        
        data = json.loads(request.body)
        game_id = int(data.get('game_id'))
        
        # Verify user owns this game
        game_session = GameSession.objects.get(id=game_id, user=user)
        
        if game_session.status != 'active':
            return JsonResponse({'error': 'Le jeu est terminé'}, status=400)
        
        # Dealer plays
        dealer_hand = game_session.dealer_hand[:]
        while calculate_score(dealer_hand) < 17:
            dealer_hand.append(random.choice(DECK))
        
        player_score = game_session.player_score
        dealer_score = calculate_score(dealer_hand)
        
        # Determine winner
        if dealer_score > 21:
            status = 'win'
            game_session.balance += game_session.bet_amount
        elif player_score > dealer_score:
            status = 'win'
            game_session.balance += game_session.bet_amount
        elif dealer_score > player_score:
            status = 'loss'
            game_session.balance -= game_session.bet_amount
        else:
            status = 'draw'
        
        game_session.status = status
        game_session.dealer_hand = dealer_hand
        game_session.dealer_score = dealer_score
        game_session.save()
        
        messages = {
            'win': 'Vous avez gagné !',
            'loss': 'Vous avez perdu.',
            'draw': 'Égalité.',
        }
        
        return JsonResponse({
            'status': status,
            'message': messages.get(status, 'Jeu terminé.'),
            'player_hand': game_session.player_hand,
            'dealer_hand': game_session.dealer_hand,
            'player_score': player_score,
            'dealer_score': dealer_score,
            'balance': game_session.balance,
        })
    
    except GameSession.DoesNotExist:
        return JsonResponse({'error': 'Jeu non trouvé'}, status=404)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Données JSON invalides'}, status=400)
    except Exception as e:
        logger.error(f"Erreur au stand: {str(e)}")
        return JsonResponse({'error': 'Erreur serveur'}, status=500)


@require_http_methods(["POST"])
@csrf_protect
def reset_game(request):
    """Reset game - start new"""
    if not is_authenticated(request):
        return JsonResponse({'error': 'Non authentifié'}, status=401)
    
    try:
        user = get_user_from_session(request)
        if not user:
            return JsonResponse({'error': 'Utilisateur non trouvé'}, status=404)
        
        # Delete old game session
        GameSession.objects.filter(user=user).delete()
        
        # Create new game
        game_session = GameSession.objects.create(
            user=user,
            bet_amount=10,
            balance=1000,
            status='active',
        )
        
        return JsonResponse({
            'status': 'reset',
            'message': 'Nouveau jeu créé',
            'balance': game_session.balance,
        })
    
    except Exception as e:
        logger.error(f"Erreur au reset: {str(e)}")
        return JsonResponse({'error': 'Erreur serveur'}, status=500)
