from django.urls import path
from .views import SendMessageView, ReceiveMessagesView  # Correct import from the current app
from . import views

urlpatterns = [
    path('send/', SendMessageView.as_view(), name='send_message'),
    path('receive/', ReceiveMessagesView.as_view(), name='receive_messages'),
    path('inbox/', views.inbox, name='inbox'),
]
