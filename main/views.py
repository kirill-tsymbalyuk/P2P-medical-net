from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['GET'])
def get_history(request):

    if request.method == "GET":
        print(request.body)
