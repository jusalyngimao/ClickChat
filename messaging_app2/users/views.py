from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import RegisterSerializer
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from messaging.models import Message

@login_required
def dashboard(request):
    sent_messages = Message.objects.filter(sender=request.user)
    received_messages = Message.objects.filter(receiver=request.user)

    context = {
        "sent_messages": sent_messages,
        "received_messages": received_messages,
    }
    return render(request, 'users/dashboard.html', context)

class RegisterView(APIView):
    permission_classes = []

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User registered successfully"})
        return Response(serializer.errors, status=400)
