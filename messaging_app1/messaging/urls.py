# urls.py
from django.urls import path
from .views import SendMessageView, ReceiveMessagesView, dashboard

urlpatterns = [
    path('send/', SendMessageView.as_view(), name='send_message'),
    path('receive/', ReceiveMessagesView.as_view(), name='receive_messages'),
    path('dashboard/', dashboard, name='dashboard'),  # Add the dashboard view
]
