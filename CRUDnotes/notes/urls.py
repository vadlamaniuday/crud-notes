from django.urls import path
from .views import (
    UserLoginView,
    UserRegistrationView,
    CreateNoteView,
    GetNoteView,
    ShareNoteView,
    UpdateNoteView,
    NoteVersionHistoryView,
)

urlpatterns = [
    path("signup/", UserRegistrationView.as_view(), name="user-registration"),
    path("login/", UserLoginView.as_view(), name="user-login"),
    path("notes/create/", CreateNoteView.as_view(), name="create-note"),
    path("notes/<int:id>/", GetNoteView.as_view(), name="get-note"),
    path("notes/share/", ShareNoteView.as_view(), name="share-note"),
    path("notes/<int:id>/", UpdateNoteView.as_view(), name="update-note"),
    path(
        "notes/version-history/<int:id>/",
        NoteVersionHistoryView.as_view(),
        name="note-version-history",
    ),
]
