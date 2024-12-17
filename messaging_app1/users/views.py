# 1. Import required libraries and modules
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import RegisterSerializer
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from messaging.models import Message

# 2. Dashboard view: Renders the user dashboard page
@login_required  # Ensures the user is logged in before accessing the dashboard
def dashboard(request):
    # 2.1 Retrieve sent and received messages for the logged-in user
    sent_messages = Message.objects.filter(sender=request.user)
    received_messages = Message.objects.filter(receiver=request.user)

    # 2.2 Pass the retrieved messages to the context for rendering the template
    context = {
        "sent_messages": sent_messages,
        "received_messages": received_messages,
    }
    
    # 2.3 Render the 'users/dashboard.html' template with context data
    return render(request, 'users/dashboard.html', context)


# 3. RegisterView: API view for handling user registration
class RegisterView(APIView):
    # 3.1 Set permissions (empty here means no permission required for registration)
    permission_classes = []  # You can change this to [AllowAny] if needed

    def post(self, request):
        # 3.2 Deserialize the registration data using the RegisterSerializer
        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():
            # 3.3 Save the new user if the data is valid
            serializer.save()
            # 3.4 Return a success response with a 201 status code
            return Response({"message": "User registered successfully"}, status=201)
        
        # 3.5 If the data is not valid, return the error response with a 400 status code
        return Response(serializer.errors, status=400)
