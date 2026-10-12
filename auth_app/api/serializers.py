from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.authtoken.models import Token


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    repeated_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'repeated_password']

    def validate(self, data):
        if data['password'] != data['repeated_password']:
            raise serializers.ValidationError(
                {"password": "Entered passwords do not match."})

        if User.objects.filter(email__iexact=data['email']).exists():
            raise serializers.ValidationError(
                {"email": "Entered email is already used."}
            )

        return data

    def create(self, validated_data):
        validated_data.pop('repeated_password')
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        Token.objects.create(user=user)
        return user


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        if not User.objects.filter(email__iexact=data['email']).exists():
            raise serializers.ValidationError(
                {"email": "Email not registered."})

        user = User.objects.get(email__iexact=data['email'])
        if not user.check_password(data['password']):
            raise serializers.ValidationError(
                {"password": "Incorrect password."}
            )

        data["user"] = user
        return data
