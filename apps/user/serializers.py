from rest_framework import  serializers
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.tokens import RefreshToken
from apps.user.models import CustomUser

class SignUpSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)    
    def validate(self, attrs):
        email = attrs.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise serializers.ValidationError({'email': 'User with this email already exists.'})        
        return attrs
    class Meta:
        model = CustomUser
        fields = ['email', 'password', 'full_name', 'phone_number']
        def create(self, validated_data):
         email = validated_data.pop('email')
         password = validated_data.pop('password')
         full_name = validated_data.get('full_name', '')
         phone_number = validated_data.get('phone_number', '')        
         user = CustomUser.objects.create_user(email=email, password=password, full_name=full_name, phone_number=phone_number, **validated_data)
         return user
    

class SignInSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    refresh_token = serializers.CharField(read_only=True)
    access_token = serializers.CharField(read_only=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            raise ValidationError({'error': 'Invalid email or password.'})

        if not user.check_password(password):
            raise ValidationError({'error': 'Invalid email or password.'})

        refresh = RefreshToken.for_user(user)
        attrs['refresh_token'] = str(refresh)
        attrs['access_token'] = str(refresh.access_token)
        return attrs

class SignOutSerializer(serializers.Serializer):
    refresh_token = serializers.CharField(write_only=True)

    def validate(self, attrs):
        self.refresh_token = attrs.get('refresh_token')
        return attrs    
    def save(self, **kwargs):
        try:
            token = RefreshToken(self.refresh_token)
            token.blacklist()
        except Exception as e:
            raise ValidationError({'error': str(e)})

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)
    class Meta:
        model = CustomUser
        fields = ['full_name', 'old_password', 'new_password', 'confirm_password']

    def validate(self, attrs):
        old_password = attrs.get('old_password')
        new_password = attrs.get('new_password')
        confirm_password = attrs.get('confirm_password')

        user = self.context['request'].user
        
        if not user:
            raise ValidationError({'error': 'User not found.'})
        
        if not user.check_password(old_password):
            raise ValidationError({'error': 'Old password is incorrect.'})
        
        if new_password != confirm_password:
            raise ValidationError({'error': 'New password and confirm password is not match.'})
        
        if old_password == new_password:
            raise ValidationError({'error': 'The new password is not the same as the old password.'})
        
        try:
            validate_password(new_password)
        except Exception as e:
            raise ValidationError({'error': str(e.messages)})
        
        self.user = user
        return attrs
    
    def save(self):
        new_password = self.validated_data['new_password']
        user = self.user
        user.set_password(new_password)
        user.save()
        return user


