"""
Serializers for the user API View.
"""
from django.contrib.auth import (
    get_user_model,
)

from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode

from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed

from ..models import UserProfile, SellerShop


class RegisterUserSerializer(serializers.ModelSerializer):
    """Registration user Serializer for the user objects."""
    password2 = serializers.CharField(
        style={'input_type': 'password'},
        write_only=True
    )

    class Meta:
        model = get_user_model()
        fields = ('first_name', 'last_name', 'username', 'email',
                  'password', 'password2', 'phone_number')
        extra_kwargs = {'password': {'write_only': True, 'min_length': 8}}

    def save(self, **kwargs):
        """Save user and check valid password"""
        password = self.validated_data['password']
        password2 = self.validated_data['password2']

        if password != password2:
            raise serializers.ValidationError(
                {'error': 'P1 and P2 should be same.'})

        if get_user_model().objects.filter(
                email=self.validated_data['email']).exists():
            raise serializers.ValidationError(
                {'error': 'Email already exists.'})

        user = get_user_model().objects.create_user(
            email=self.validated_data['email'], password=password,
            username=self.validated_data['username'],
            first_name=self.validated_data['first_name'],
            last_name=self.validated_data['last_name'],
            phone_number=self.validated_data['phone_number'])
        user.set_password(password)
        user.save()

        return user

    def create(self, validated_data):
        """Create and return a user with encrypted password."""
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """Update and return user."""
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user


class RegisterSellerShopUserSerializer(RegisterUserSerializer):

    def save(self, **kwargs):
        """Save user and check valid password"""
        password = self.validated_data['password']
        password2 = self.validated_data['password2']

        if password != password2:
            raise serializers.ValidationError(
                {'error': 'P1 and P2 should be same.'})

        if get_user_model().objects.filter(
                email=self.validated_data['email']).exists():
            raise serializers.ValidationError(
                {'error': 'Email already exists.'})

        user = get_user_model().objects.create_user(
            email=self.validated_data['email'], password=password,
            username=self.validated_data['username'],
            first_name=self.validated_data['first_name'],
            last_name=self.validated_data['last_name'],
            phone_number=self.validated_data['phone_number'],
            role=1)
        user.set_password(password)
        user.save()

        return user


class EmailVerificationSerializer(serializers.Serializer):
    token = serializers.CharField(max_length=555)

    class Meta:
        fields = ('token',)


class PasswordTokenCheckSerializer(EmailVerificationSerializer):
    uidb64 = serializers.CharField(max_length=20)


class ResetPasswordEmailSerializer(serializers.Serializer):
    """Serializer for reset password with send email."""
    email = serializers.EmailField(max_length=100)

    class Meta:
        fields = ('email',)


class SetNewPasswordSerializer(serializers.Serializer):
    """Serializer for set new password for user."""
    password = serializers.CharField(
        min_length=8, max_length=68, write_only=True)
    password2 = serializers.CharField(
        min_length=8, max_length=68, write_only=True)

    token = serializers.CharField(write_only=True)
    uidb64 = serializers.CharField(write_only=True)

    class Meta:
        fields = ('password', 'password2', 'token', 'uidb64')

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')

        if password != password2:
            raise serializers.ValidationError(
                {'error': 'P1 and P2 should be same.'})

        try:

            token = attrs.get('token')
            uidb64 = attrs.get('uidb64')

            id = force_str(urlsafe_base64_decode(uidb64))
            user = get_user_model().objects.get(id=id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                raise AuthenticationFailed('The reset link is invalid.', 401)

            user.set_password(password)
            user.save()

        except Exception:
            raise AuthenticationFailed(
                'The reset link is invalid. exeption', 401)
        return super().validate(attrs)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('id', 'first_name', 'last_name', 'username', 'email',
                  'phone_number', 'role', 'is_active')
        extra_kwargs = {'role': {'read_only': True},
                        'is_active': {'read_only': True}}


class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=False)

    class Meta:
        model = UserProfile
        fields = '__all__'

    def update(self, instance, validated_data):
        nested_serializer = self.fields['user']
        nested_instance = instance.user
        nested_data = validated_data.pop('user', {})

        nested_serializer.update(nested_instance, nested_data)
        return super().update(instance, validated_data)


class SellerShopProfileSerializer(serializers.ModelSerializer):
    owner = serializers.EmailField()

    class Meta:
        model = SellerShop
        fields = '__all__'

    def get_owner(self, obj):
        return get_user_model().objects.get(id=obj.id)
