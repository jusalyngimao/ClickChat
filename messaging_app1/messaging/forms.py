# messaging/forms.py
from django import forms
from django.contrib.auth import get_user_model
from .models import Message

User = get_user_model()

class SendMessageForm(forms.ModelForm):
    """
    Form to send a message to another user.
    """
    class Meta:
        model = Message
        fields = ['receiver', 'content']
        
    receiver = forms.ModelChoiceField(queryset=User.objects.all(), empty_label="Select a user", label="Receiver")
    content = forms.CharField(widget=forms.Textarea(attrs={'rows': 4, 'cols': 40}), label="Message")
