from django.shortcuts import render
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from django.contrib.auth.models import Group
from django.http import HttpResponseForbidden, HttpResponseRedirect, FileResponse
from django.contrib import auth
from .forms import *
import json
from .models import *
import qrcode
import io


def is_in_group(user, group_name):
    try:
        return Group.objects.get(name=group_name).user_set.filter(id=user.id).exists()
    except Group.DoesNotExist:
        return None


def index(request):
    return render(request, 'main/index.html')


def registration(request):

    if request.user.is_authenticated:
        return HttpResponseRedirect("/profile/")

    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            email = form.cleaned_data.get("email")
            for user in User.objects.all():
                if user.username == username:
                    error = 'This username already exists'
                    return render(request, 'registration/registration.html', {'form': form, 'errors': error})
                if user.email == email:
                    error = 'This mail already exists'
                    return render(request, 'registration/registration.html', {'form': form, 'errors': error})
            user = User.objects.create_user(username, email, password)
            user.save()
            auth.login(request, user)
        return HttpResponseRedirect('/profile/')

    else:
        form = UserForm()
        error = ''
    return render(request, 'registration/registration.html', {'form': form, 'error': error})


def login(request):
    errors = ""
    if request.user.is_authenticated:
        return HttpResponseRedirect("/profile/")
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = auth.authenticate(request, username=form.cleaned_data.get("username"),
                                     password=form.cleaned_data.get("password"))
            if user is not None:
                auth.login(request, user)
                return HttpResponseRedirect("/profile/")
            else:
                errors = "Authorization failed, incorrect username or password"
    else:
        form = LoginForm()
    return render(request, 'main/login.html', {"form": form, "errors": errors})


def profile(request):
    if request.method == 'POST' and request.FILES['img']:
        obj = UserUpgrade.objects.get(user=request.user)
        obj.img = request.FILES['img']
        obj.save()
    return render(request, 'main/profile.html', {"img": UserUpgrade.objects.get(user=request.user).img})


def download_qrcode(request):
    code = qrcode.make(Token.objects.get(user=request.user))
    buff = io.BytesIO()
    code.save(buff, 'png')
    file = io.BytesIO(buff.getvalue())
    file.name = 'qr-code.png'
    return FileResponse(file)


def med_card(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/login/')

    return render(request, 'main/med_card.html', {'cards': Card.objects.filter(patient=request.user.id)})


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

