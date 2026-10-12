from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.authtoken.models import Token


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    repeated_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'repeated_password']

    def validate(self, attrs):
        if attrs['password'] != attrs['repeated_password']:
            raise serializers.ValidationError(
                {"password": "Entered passwords do not match."})

        if User.objects.filter(email__iexact=attrs['email']).exists():
            raise serializers.ValidationError(
                {"email": "Entered email is already used."}
            )

        return attrs

    def create(self, validated_data):
        validated_data.pop('repeated_password')
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        Token.objects.create(user=user)
        return user
