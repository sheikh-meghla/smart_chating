from rest_framework import generics
from .models import Message
from .serializers import MessageSerializer
from apps.user.models import CustomUser
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

class SendMessageView(generics.CreateAPIView):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def post(self, request):
        sender = request.user
        receiver_email = request.data.get('receiver_email')
        text = request.data.get('text')

        if not receiver_email or not text:
            return Response({"error": "Receiver email and text required"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            receiver = CustomUser.objects.get(email=receiver_email)
        except CustomUser.DoesNotExist:
            return Response({"error": "Receiver not found"}, status=status.HTTP_404_NOT_FOUND)
        
        message = Message.objects.create(sender=sender, receiver=receiver, text=text)
        serializer = self.get_serializer(message)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class MessageListView(generics.ListAPIView):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    def get_queryset(self):
        user = self.request.user
        return Message.objects.filter(sender=user) | Message.objects.filter(receiver=user)
