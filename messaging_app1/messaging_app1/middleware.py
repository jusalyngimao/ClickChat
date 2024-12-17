from django.utils.deprecation import MiddlewareMixin
from cryptography.fernet import Fernet

SECRET_KEY = b'my_secret_key_for_fernet'

class EncryptionMiddleware(MiddlewareMixin):
    def process_request(self, request):
        """
        Log and optionally encrypt incoming requests.
        """
        # Example: Log the request details
        print(f"Incoming request: {request.method} {request.path}")
        
        # You can inspect or modify request data here if needed
        return None

    def process_response(self, request, response):
        """
        Encrypt response data if it's a JSON payload.
        """
        if response.get('Content-Type') == 'application/json':
            fernet = Fernet(SECRET_KEY)
            encrypted_data = fernet.encrypt(response.content).decode()
            response.content = encrypted_data
        return response
