from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Note


User = get_user_model()


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["username", "email", "password"]

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data["username"], email=validated_data["email"]
        )
        user.set_password(validated_data["password"])
        user.save()
        return user


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=False)
    email = serializers.EmailField(required=False)
    password = serializers.CharField()

    def validate(self, data):
        username = data.get("username")
        email = data.get("email")
        password = data.get("password")

        if not (username or email):
            raise serializers.ValidationError("Username or email is required")

        user = authenticate(
            request=self.context.get("request"),
            username=username,
            email=email,
            password=password,
        )

        if not user:
            raise serializers.ValidationError("Invalid credentials")

        data["user"] = user
        return data


class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ["title", "content", "author"]


class NoteDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ["id", "title", "content", "published_at"]


class NoteShareSerializer(serializers.Serializer):
    note_id = serializers.IntegerField()
    shared_users = serializers.ListField(
        child=serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    )


class NoteUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ["title", "content"]
