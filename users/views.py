from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserSerializer, LeaderBoardSerializer
from .models import User
from rest_framework.exceptions import AuthenticationFailed
from rest_framework import viewsets, mixins, generics
from .utils import create_token
import jwt
import datetime


class registerAPIView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        response = Response()
        token = create_token(user.id, user.username)
        
        response.set_cookie(key='jwt', value=token, httponly=True)

        response.data = {
            'token': token
        }
        return response


class LoginAPIView(APIView):
    def post(self, request):
        username = request.data['username']
        password = request.data['password']

        user = User.objects.filter(username=username).first()

        if user is None:
            raise AuthenticationFailed('User not found')
            
        if not user.check_password(password):
            raise AuthenticationFailed('Invalid password')

        token = create_token(user.id, user.username)
        
        response = Response() 

        response.set_cookie(key='jwt', value=token, httponly=True)

        response.data = {
            'token': token
        }

        return response

class LogoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {'message': 'successful'}
        return response


class UserAPIView(APIView):
    def get(self, request):
        authorization_header = request.META.get('HTTP_AUTHORIZATION')
        auth_type, token = authorization_header.split(' ')

        if not token:
            raise AuthenticationFailed("Unauthenticated!")
        
        try:
            payload = jwt.decode(token, 'secret', algorithms="HS256")

        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Unauthenticated!")
        
        user = User.objects.filter(username=payload['username']).first()
        serializer = UserSerializer(user)

        return Response(serializer.data)


class UserUpdateAPIView(APIView):   
    def put(self, request, *args, **kwargs):
        authorization_header = request.META.get('HTTP_AUTHORIZATION')
        auth_type, token = authorization_header.split(' ')

        if not token:
            raise AuthenticationFailed("Unauthenticated!")
        
        try:
            payload = jwt.decode(token, 'secret', algorithms="HS256")
            instance = User.objects.filter(username=payload['username']).first()
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Unauthenticated!")
        serializer = UserSerializer(data=request.data, instance=instance)
        serializer.is_valid()
        serializer.save()
        return Response(serializer.data)


class UserListAPIView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
