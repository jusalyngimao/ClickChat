# messaging_app1/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .serializers import RegisterSerializer
from messaging.models import Message

def home(request):
    return render(request, 'users/home.html')
    # You can either render a home page or redirect to login if not authenticated
    if request.user.is_authenticated:
        return redirect('dashboard')  # Redirect authenticated users to the dashboard
    return redirect('login')  # Redirect unauthenticated users to login page

# Registration View
class RegisterView(APIView):
    permission_classes = []  # Allow all users, even if unauthenticated

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User registered successfully"})
        return Response(serializer.errors, status=400)
# Login View
def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'users/login.html', {'error': 'Invalid credentials'})
    return render(request, 'users/login.html')

# Dashboard View (User-specific messages)
@login_required
def dashboard(request):
    sent_messages = Message.objects.filter(sender=request.user)
    received_messages = Message.objects.filter(receiver=request.user)

    context = {
        "sent_messages": sent_messages,
        "received_messages": received_messages,
    }
    return render(request, 'users/dashboard.html', context)
