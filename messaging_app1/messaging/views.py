import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Message
from .serializers import MessageSerializer
from .utils import encrypt_message, decrypt_message  # Import decrypt function
from django.http import HttpResponse
from django.shortcuts import render
from .utils import decrypt_message

def dashboard(request):
    sent_messages = Message.objects.filter(sender=request.user)
    received_messages = Message.objects.filter(receiver=request.user)

    # Decrypt the content before passing it to the template
    for message in sent_messages:
        message.decrypted_content = decrypt_message(message.encrypted_content)

    for message in received_messages:
        message.decrypted_content = decrypt_message(message.encrypted_content)

    return render(request, 'users/dashboard.html', {
        'user': request.user,
        'sent_messages': sent_messages,
        'received_messages': received_messages,
    })

# Create a simple home view
def home(request):
    return HttpResponse("Welcome to the messaging app!")

class SendMessageView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        sender = request.user
        receiver_id = request.data.get('receiver_id')
        content = request.data.get('content')

        # Encrypt the message locally
        encrypted_content = encrypt_message(content)

        # Save message in the local app
        message = Message.objects.create(sender=sender, receiver_id=receiver_id, encrypted_content=encrypted_content)

        # Send encrypted message to the second app via REST API
        remote_api_url = "http://127.0.0.1:8001/api/messages/receive/"  # Replace with actual URL of the second app
        headers = {"Authorization": f"Bearer {request.auth}"}
        payload = {
            "sender": sender.username,
            "content": encrypted_content,
        }
        try:
            response = requests.post(remote_api_url, json=payload, headers=headers)
            if response.status_code == 200:
                return Response({"message": "Message sent successfully"})
        except requests.exceptions.RequestException as e:
            return Response({"error": "Failed to send message to the second app"}, status=500)
        
        return Response({"message": "Message saved locally, but failed to send remotely."})


class ReceiveMessagesView(APIView):
    """
    API view to handle receiving messages from the second app.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        sender = request.data.get('sender')
        content = request.data.get('content')

        if not sender or not content:
            return Response({"error": "Sender and content are required."}, status=400)

        # Decrypt the content before saving
        decrypted_content = decrypt_message(content)

        # Save the received message (store decrypted content if needed)
        Message.objects.create(sender=sender, receiver=request.user, encrypted_content=decrypted_content)

        return Response({"message": "Message received successfully."})

