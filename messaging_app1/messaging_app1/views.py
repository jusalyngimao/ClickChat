from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from .serializers import RegisterSerializer
from messaging.models import Message
from django.contrib.auth import logout

# Get the custom user model
User = get_user_model()

# Home View
def home(request):
    """
    Display the home page.
    If the user is authenticated, pass `authenticated: True` in the context.
    """
    context = {"authenticated": request.user.is_authenticated}
    return render(request, 'users/home.html', context)

# Registration View
class RegisterView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        """
        Handle unsupported GET requests for registration.
        """
        return Response(
            {"message": "GET method is not supported, please use POST"}, 
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )

    def post(self, request):
        """
        Handle user registration with username and password.
        """
        username = request.data.get('username')
        password = request.data.get('password')

        if username and password:
            # Create a new user
            User.objects.create_user(username=username, password=password)
            return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)

        return Response({"error": "Invalid data"}, status=status.HTTP_400_BAD_REQUEST)

# Login View (API)
class LoginView(APIView):
    """
    Handle user login and return a token for API authentication.
    """
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # Generate or retrieve token
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        
        return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)

# Login View (Traditional Django)
def login_view(request):
    """
    Render the login page and handle login using Django's built-in authentication.
    """
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')  # Redirect after successful login
        else:
            return render(request, 'users/login.html', {'error': 'Invalid credentials'})
    return render(request, 'users/login.html')

# Dashboard View
@login_required
def dashboard(request):
    """
    Display a dashboard showing messages sent and received by the logged-in user.
    """
    sent_messages = Message.objects.filter(sender=request.user)
    received_messages = Message.objects.filter(receiver=request.user)

    context = {
        "sent_messages": sent_messages,
        "received_messages": received_messages,
    }
    return render(request, 'users/dashboard.html', context)

def logout_view(request):
    logout(request)
    return redirect('home')