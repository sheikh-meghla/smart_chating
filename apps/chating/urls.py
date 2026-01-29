from django.urls import path
from .views import SendMessageView, MessageListView

urlpatterns = [
    path('send/', SendMessageView.as_view(), name='send-message'),
    path('messages/', MessageListView.as_view(), name='messages-list'),

]
