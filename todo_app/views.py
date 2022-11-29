from django.shortcuts import render, HttpResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.conf import settings
from .models import TodoItem
from .serializers import TaskSerializer
import jwt
from base64 import b64decode
from pprint import pprint
# Create your views here.


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def testView(request):
    return Response({"message": "hi"})


@api_view(['GET', 'POST', 'PATCH'])
@permission_classes([IsAuthenticated])
def listview(request):
    Autho = request.headers['Authorization'][7:]
    result = jwt.decode(Autho, key=settings.SECRET_KEY,
                        algorithms="HS256", verify=True)
    if request.method == 'GET':
        task = TodoItem.objects.filter(user=result["user_id"])
        serializer = TaskSerializer(task, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        data = request.data['detail']
        data['user'] = result['user_id']
        serializer = TaskSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    if request.method == 'PATCH':
        pprint(request.data['detail']['id'])
        instance = TodoItem.objects.get(
            id=request.data['detail']['id'], user=result['user_id'])
        serializer = TaskSerializer(instance, data=request.data['detail'])
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response('hola')


@api_view(['POST'])
def delete_task_view(request):
    Autho = request.headers['Authorization'][7:]
    result = jwt.decode(Autho, key=settings.SECRET_KEY,
                        algorithms="HS256", verify=True)
    if request.method == 'POST':
        task = TodoItem.objects.get(
            id=request.data['task_id'], user=result['user_id'])
        task.delete()
        return Response({'message': 'Successfully deleted'})
