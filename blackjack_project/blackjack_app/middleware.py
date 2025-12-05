from django.middleware.security import SecurityMiddleware

class SecurityHeadersMiddleware:
    """Add security headers to all responses"""
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        response = self.get_response(request)
        
        # Prevent MIME type sniffing
        response['X-Content-Type-Options'] = 'nosniff'
        
        # Prevent clickjacking (deny iframe)
        response['X-Frame-Options'] = 'DENY'
        
        # Prevent XSS (old browsers)
        response['X-XSS-Protection'] = '1; mode=block'
        
        return response
