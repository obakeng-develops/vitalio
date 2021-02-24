# Django
from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
import os

# Models 
from provider.models import Booking

# Third Party
from twilio.rest import Client
from twilio.jwt.access_token import AccessToken
from twilio.jwt.access_token.grants import VideoGrant

# Twilio Account Values
account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']
api_key_sid = os.environ['TWILIO_API_KEY_SID']
api_key_secret = os.environ['TWILIO_API_KEY_SECRET']


def test_audio(request):

    if request.POST:

        booking_code = request.POST.get('booking_code')

        request.session['booking'] = booking_code

    return render(request, "room/test_audio.html")

def test_video(request):

    booking = request.session.get('booking')

    return render(request, "room/test_video.html")

def room(request, roomcode=None):

    client = Client(account_sid, auth_token)

    booking_code = request.session.get('booking')

    roomcode = booking_code

    exists = client.video.rooms.list(unique_name=roomcode)

    if exists is None:
        client.video.rooms.create(type='go', unique_name=roomcode)

    identity = request.user.email
    
    token = AccessToken(account_sid, 
                        api_key_sid,
                        api_key_secret, identity=identity, ttl=300)
    
    token.add_grant(VideoGrant(room=roomcode))
    
    context = {
        "token": token.to_jwt().decode(),
        "identity": identity,
        "roomName": roomcode
    }

    return render(request, "room/room.html", context)
