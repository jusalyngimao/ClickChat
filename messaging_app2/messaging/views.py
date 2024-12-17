import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError
from .models import Message
from .serializers import MessageSerializer
from .utils import encrypt_message
import logging

def inbox(request):
    messages = Message.objects.filter(receiver=request.user)
    return render(request, 'messaging/inbox.html', {'messages': messages})

logger = logging.getLogger(__name__)

class SendMessageView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        sender = request.user
        receiver_id = request.data.get('receiver_id')
        content = request.data.get('content')

        # Validate receiver_id
        receiver = User.objects.filter(id=receiver_id).first()
        if not receiver:
            raise ValidationError("Receiver does not exist.")

        # Encrypt the message locally
        encrypted_content = encrypt_message(content)

        # Save message in the local app
        message = Message.objects.create(sender=sender, receiver=receiver, encrypted_content=encrypted_content)

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
            else:
                logger.error(f"Failed to send message, received status code {response.status_code}")
        except requests.exceptions.RequestException as e:
            logger.error(f"Error sending message to the second app: {str(e)}")
            return Response({"error": "Failed to send message to the second app"}, status=500)

        # Serialize and return the message locally saved
        serializer = MessageSerializer(message)
        return Response({
            "message": "Message saved locally, but failed to send remotely.",
            "message_data": serializer.data
        })

class ReceiveMessagesView(APIView):
    def post(self, request):
        # Your logic for receiving messages
        return Response({"message": "Received message"})