# messaging_app2/middleware.py
from django.http import HttpResponse

class EncryptionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Custom middleware logic here
        response = self.get_response(request)
        return response
