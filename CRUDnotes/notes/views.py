from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from .serializers import (
    UserRegistrationSerializer,
    UserLoginSerializer,
    NoteSerializer,
    NoteDetailSerializer,
    NoteShareSerializer,
    NoteUpdateSerializer,
)
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from .models import Note
from rest_framework import serializers
from django.contrib.auth import login, authenticate
from rest_framework.authtoken.views import ObtainAuthToken


class UserRegistrationView(APIView):
    # This code snippet defines a POST method that takes a request, validates the data using a serializer, saves the data if it's valid, and returns the appropriate response with status codes.

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):
    def post(self, request):
        # Validate user input
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            # Authenticate user
            user = authenticate(
                username=serializer.validated_data["username"],
                password=serializer.validated_data["password"],
            )
            # If user is authenticated, log in and generate token

            if user:
                login(request, user)
                token, created = Token.objects.get_or_create(user=user)
                return Response({"token": token.key}, status=status.HTTP_200_OK)
            else:
                # Return error for invalid username or password
                return Response(
                    {"error": "Invalid username or password."},
                    status=status.HTTP_401_UNAUTHORIZED,
                )
        # Return validation errors for invalid input
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CreateNoteView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        # Set the author of the note as the current user
        request.data["author"] = request.user.id

        serializer = NoteSerializer(data=request.data)
        # Check if the serializer is valid and then save the data with a success message
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Note created successfully"}, status=status.HTTP_201_CREATED
            )
        # Return error response with serializer errors

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetNoteView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        try:
            # Retrieve the note by its ID
            note = Note.objects.get(id=id)

            # Check if the requesting user is the owner or a shared user
            if request.user == note.author or request.user in note.shared_users.all():
                # Serialize and return the note details
                serializer = NoteDetailSerializer(note)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(
                    {"error": "You do not have permission to view this note."},
                    status=status.HTTP_403_FORBIDDEN,
                )

        except Note.DoesNotExist:
            return Response(
                {"error": "Note not found."}, status=status.HTTP_404_NOT_FOUND
            )


class ShareNoteView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Serialize the request data
        serializer = NoteShareSerializer(data=request.data)
        # Check if the data is valid
        if serializer.is_valid():
            note_id = serializer.validated_data["note_id"]
            shared_users = serializer.validated_data["shared_users"]

            try:
                # Retrieve the note based on note_id
                note = Note.objects.get(id=note_id)
                # Check if the user making the request is the author of the note

                if request.user == note.author:
                    note.shared_users.set(shared_users)
                    note.save()
                    return Response(
                        {"message": "Note shared successfully"},
                        status=status.HTTP_200_OK,
                    )
                else:
                    return Response(
                        {"error": "You do not have permission to share this note."},
                        status=status.HTTP_403_FORBIDDEN,
                    )

            except Note.DoesNotExist:
                return Response(
                    {"error": "Note not found."}, status=status.HTTP_404_NOT_FOUND
                )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateNoteView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, id):
        try:
            # Get the note with the given ID
            note = Note.objects.get(id=id)

            # Check if the requesting user is the owner or a shared user
            if request.user == note.author or request.user in note.shared_users.all():
                serializer = NoteUpdateSerializer(note, data=request.data, partial=True)

                if serializer.is_valid():
                    # Save the updated note and update the versions list
                    updated_content = serializer.validated_data["content"]
                    note.content = updated_content
                    note.versions.append(
                        {
                            "timestamp": serializers.DateTimeField().to_representation(
                                serializers.DateTimeField().get_current_time()
                            ),
                            "edited_by": request.user.username,
                            "content_changes": updated_content,
                        }
                    )
                    note.save()
                    return Response(
                        {"message": "Note updated successfully"},
                        status=status.HTTP_200_OK,
                    )

                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            else:
                return Response(
                    {"error": "You do not have permission to update this note."},
                    status=status.HTTP_403_FORBIDDEN,
                )

        except Note.DoesNotExist:
            return Response(
                {"error": "Note not found."}, status=status.HTTP_404_NOT_FOUND
            )


class NoteVersionHistoryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        try:
            # Get the note with the specified ID
            note = Note.objects.get(id=id)

            # Check if the requesting user is the owner or a shared user
            if request.user == note.author or request.user in note.shared_users.all():
                # Get the version history of the note
                version_history = note.versions
                return Response(
                    {"version_history": version_history}, status=status.HTTP_200_OK
                )

            else:
                return Response(
                    {
                        "error": "You do not have permission to view the version history of this note."
                    },
                    status=status.HTTP_403_FORBIDDEN,
                )

        except Note.DoesNotExist:
            # Return error response if note is not found

            return Response(
                {"error": "Note not found."}, status=status.HTTP_404_NOT_FOUND
            )
