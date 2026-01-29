from django.urls import path
from .views import SignUpAPIView, SignInAPIView, SignOutAPIView

urlpatterns = [
    path('signup/', SignUpAPIView.as_view(), name='signup'),
    path('signin/', SignInAPIView.as_view(), name='signin'),
    path('signout/', SignOutAPIView.as_view(), name='signout'),

]
