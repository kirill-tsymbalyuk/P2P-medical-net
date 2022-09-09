from django.shortcuts import render
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from django.contrib.auth.models import Group
from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.contrib import auth
from .forms import UserForm
import json
from .models import *


def is_in_group(user, group_name):
    try:
        return Group.objects.get(name=group_name).user_set.filter(id=user.id).exists()
    except Group.DoesNotExist:
        return None


def index(request):
    return render(request, 'main/index.html')


def registration(request):

    if request.user.is_authenticated:
        return HttpResponseRedirect("/accounts/profile/")

    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get("name")
            password = form.cleaned_data.get("password")
            mail = form.cleaned_data.get("mail")
            for user in User.objects.all():
                if user.username == name:
                    error = 'This username already exists'
                    return render(request, 'registration/registration.html', {'form': form, 'error': error})
                if user.email == mail:
                    error = 'This mail already exists'
                    return render(request, 'registration/registration.html', {'form': form, 'error': error})
            user = User.objects.create_user(name, mail, password)
            user.save()
            auth.login(request, user)
        return HttpResponseRedirect('/accounts/profile/')

    else:
        form = UserForm()
        error = ''
    return render(request, 'registration/registration.html', {'form': form, 'error': error})


@api_view(['GET', 'POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_history(request):
    history = {}
    for card in Card.objects.filter(patient=request.user.id):
        history[card.name+" - "+str(card.date)[:16]] = card.text
    return Response(history)


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def set_data(request):
    if request.method == "POST":
        if is_in_group(request.user, 'Doctors'):
            data = json.loads(request.body)
            patient = Token.objects.get(key=data['patient_key']).user
            Card.objects.create(patient=patient, text=data['text'], name=data['name']).save()
            return Response("Ok")

        else:
            return HttpResponseForbidden("You are not a doctor")

    return Response("Method is not allowed")


def profile(request):
    return render(request, 'main/med_card.html')
