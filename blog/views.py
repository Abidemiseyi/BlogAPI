from django.shortcuts import render

from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework import status
from .serializers import TaskSerializers
from .models import Task
from rest_framework.decorators import api_view


@api_view(['GET'])
def task_list(request):
    if request.method == 'GET':
        tasks = Task.objects.all()
        serializer = TaskSerializers(tasks, many=True)
        return Response(serializer.data)


@api_view(['POST'])
def task_create(request):
    if request.method == 'POST':
        serializer = TaskSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def task_detail(request, pk):
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
