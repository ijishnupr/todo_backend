# views.py

from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token 
from django.contrib.auth import authenticate,login
from django.contrib.auth.models import User
from .serializer import *
@api_view(['POST'])
def signup(request):
    if request.method == 'POST':
       
        name = request.data.get('name')
        email = request.data.get('email')
        password = request.data.get('password')

        
        if not all([name, email, password]):
            return Response({'error': 'Please provide name, email, and password'}, status=400)

       
        if User.objects.filter(email=email).exists():
            return Response({'error': 'User with this email already exists'}, status=400)

       
        user = User.objects.create_user(username=email, email=email, password=password, first_name=name, last_name=name)

        return Response({'message': 'User created successfully'}, status=201)
    else:
        return Response({'error': 'Method not allowed'}, status=405)
  

@api_view(['POST'])
def login(request):
    
    email = request.data.get('email')
    password = request.data.get('password')
    if not email or not password:
        return Response({'error': 'Please provide both email and password'}, status=status.HTTP_400_BAD_REQUEST)
    
    user = authenticate(request,email=email,password=password)
    user=User.objects.get(email=email)
    if user:
        
        token,created=Token.objects.get_or_create(user=user)
        return Response({ 
            'token':token.key,
        }, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
@permission_classes([AllowAny])
def add_todo(request):
    serializer = TodoSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response('Todo added successfully', status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([AllowAny])
def list_todo(request):
    data=Todo.objects.all()
    serializers=TodoSerializer(data,many=True)
    return Response(serializers.data,status=status.HTTP_200_OK)

@api_view(['PATCH'])
@permission_classes([AllowAny])
def edit_todo(request):
    todo_id = request.data.get('id',)

    try:
        todo = Todo.objects.get(pk=todo_id)
    except Todo.DoesNotExist:
        print('not found')
        return Response({'error': 'Todo not found'})

    serializer = TodoSerializer(todo, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response('Todo updated successfully', status=status.HTTP_200_OK)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([AllowAny])
def delete_todo(request):
    todo_id=request.GET.get('id')
    print(todo_id)
    try:
        todo = Todo.objects.get(pk=todo_id)
    except Todo.DoesNotExist:
        return Response({'error': 'Todo not found'})

    todo.delete()
    return Response('Todo deleted successfully', status=status.HTTP_204_NO_CONTENT)
@api_view(['GET'])
@permission_classes([AllowAny])
def view_todo(request):
    id = request.GET.get('id')
    if id:
        try:
            todo = Todo.objects.get(id=id)
            serializer = TodoSerializer(todo)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Todo.DoesNotExist:
            return Response({'error': 'Todo not found'})
    else:
        return Response({'error': 'Please provide an ID'}, status=status.HTTP_400_BAD_REQUEST)