from rest_framework import serializers

from apps import user
from .models import Message
from apps.user.models import CustomUser

class MessageSerializer(serializers.ModelSerializer):
    sender_email = serializers.EmailField(source='sender.email', read_only=True)
    receiver_email = serializers.EmailField(source='receiver.email', read_only=True)

    class Meta:
        model = Message
        fields = ['id', 'sender_email', 'receiver_email', 'text', 'timestamp', 'is_read']
