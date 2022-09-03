from django.shortcuts import render

from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework import status
from .serializers import TaskSerializers, RegisterSerializers
from .models import Task
from rest_framework.decorators import api_view
from knox.auth import AuthToken
from rest_framework.authtoken.serializers import AuthTokenSerializer


@api_view(['POST'])
def login(request):
    serializer = AuthTokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer._validated_data['user']
    _, token = AuthToken.objects.create(user)

    return Response({
        'user_info': {
            'id': user.id,
            'username': user.username
        },
        'token': token
    })


@api_view(['GET'])
def get_user_details(request):
    user = request.user
    if user.is_authenticated:
        return Response({
            'user_info': {
                'id': user.id,
                'username': user.username
            }
        })
    return Response({'error': 'Not authenticated'}, status=404)


@api_view(['POST'])
def register(request):
    serializer = RegisterSerializers(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.save()

    _, token = AuthToken.objects.create(user)

    return Response({
        'user_info': {
            'id': user.id,
            'username': user.username
        },
        'token': token
    })


@api_view(['GET'])
def list_blog(request):
    tasks = Task.objects.all()
    serializer = TaskSerializers(tasks, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def create_blog(request):
    serializer = TaskSerializers(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def blog_details(request, pk):
    try:
        tasks = Task.objects.get(pk=pk)
    except Task.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = TaskSerializers(tasks)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = TaskSerializers(tasks, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        tasks.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
