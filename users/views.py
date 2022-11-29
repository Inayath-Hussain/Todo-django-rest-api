from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import UserSerializer, MyTokenObtainPairSerializer
from .models import CustomUser
from pprint import pprint
# Create your views here.


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class RegisterView(APIView):

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user = CustomUser.objects.get(email=request.data['email'])
        refresh = RefreshToken.for_user(user)
        result = {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }
        return Response(result)


class LoginView(APIView):
    def post(self, request):
        cred = (request._request).body.decode().split('"')
        email = cred[3]
        password = cred[7]
        try:
            user = CustomUser.objects.get(email=email)
        except ObjectDoesNotExist:
            return Response({"error": "email dosen't exist"})
        if not user.check_password(password):
            return Response({"error": 'Password is incorrect'})
        result = MyTokenObtainPairView.as_view()(request=request._request).data
        return Response(result)
        # else:
        #     if user.check_password(request.data['password']):
        #         refresh = RefreshToken.for_user(user)
        #         result = {
        #             'refresh': str(refresh),
        #             'access': str(refresh.access_token)
        #         }
        #         return Response(result)
        #     else:
        #         return Response({'error message': 'password is incorrect'})
