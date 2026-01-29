from .models import CustomUser
from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.validators import ValidationError

from .serializers import (
    SignUpSerializer,
    SignInSerializer,
    SignOutSerializer,
    ChangePasswordSerializer,

    UserInfoSerializer,
)


class SignUpAPIView(APIView):
    permission_classes = []

    def post(self, request):

        serializer = SignUpSerializer(data=request.data)

        if serializer.is_valid():

            serializer.save()

            return Response({
                "status" : "success",
                "message" : "User registered successfully.",
                "data" : serializer.data
            })
        raise ValidationError(serializer.errors)

class SignInAPIView(APIView):

    permission_classes = []

    def post(self, request):
        
        serializer = SignInSerializer(data=request.data)
        
        if serializer.is_valid():
            return Response({
                "status" : "success",
                "message" : "User signed in successfully.",
                "data" : serializer.data
            })
        raise ValidationError(serializer.errors)


class SignOutAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def post(self, request):
        serializer = SignOutSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            return Response({
                "status" : "success",
                "message" : "Sign Out Successfull"
            })
        
        raise ValidationError(serializer.errors)

class ChangePasswordAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status" : "success",
                "message" : "Password changed successfully.",
                "data" : serializer.data
            })
        raise ValidationError(serializer.errors)

class MyProfileAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        vendor = request.user

        user_info = CustomUser.objects.prefetch_related('vendor_profile').get(id=vendor.id)
        serializer = UserInfoSerializer(user_info)
        

        return Response({
            "status" : "success",
            "message" : "Profile retrieved successfully.",
            "data" : serializer.data
        })
