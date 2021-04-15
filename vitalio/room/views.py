# Django
from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
import os
import environ
from django.conf import settings

# Models 
from provider.models import Booking

# Third Party
from twilio.rest import Client
from twilio.jwt.access_token import AccessToken
from twilio.jwt.access_token.grants import VideoGrant

# Twilio Account Values
account_sid="ACb4d2387e934ec98773f3fc4732cbce80"
auth_token="2bdf89f370d340ad3546d27639d45c09"
api_key_sid="SK413cfa1855c87162baeb39e5c8fbbb65"
api_key_secret="jIqm631MCt29lIWn8OLd9g1j6DC1ONEc"


def test_audio(request):

    if request.POST:

        booking_code = request.POST.get('booking_code')

        request.session['booking'] = booking_code

    return render(request, "room/test_audio.html")

def test_video(request):

    booking = request.session.get('booking')
    

    return render(request, "room/test_video.html")

@login_required
def room(request, roomcode=None):


    # Get Twilio Client
    client = Client(account_sid, auth_token)

    # Get Unique Booking Code
    booking_code = request.session.get('booking')

    roomcode = booking_code

    # Check if exists
    exists = client.video.rooms.list(unique_name=roomcode)

    # Create The Unique Room
    if exists is None:
        client.video.rooms.create(unique_name=roomcode)

    # Retrieve User Identity
    identity = request.user.email
    
    # Create Access Token
    token = AccessToken(account_sid, 
                        api_key_sid,
                        api_key_secret, identity=identity, ttl=300)
    
    token.add_grant(VideoGrant(room=roomcode))
    
    # Pass all relevant information to the context dictionary
    context = {
        "token": token.to_jwt().decode(),
        "identity": identity,
        "roomName": roomcode
    }

    return render(request, "room/room.html", context)
