# Django
from django.urls import path, re_path

# Views
from .views import test_audio, test_video, room

urlpatterns = [
    path("test-audio", test_audio, name="test_audio"),
    path("test-video", test_video, name="test_video"),
    re_path("$", room, name="room"),
]