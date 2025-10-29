from rest_framework.views import APIView
from rest_framework.response import Response
from . import serializers
from . import models
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

class SignupView(APIView):
    def post(self,request):
        try:
            serial=serializers.UserSerializer(data=request.data)
            if serial.is_valid():
                serial.save()
                return Response({'Sucess':'Signup Sucessfully'},status=200)
            return Response({'Error':serial.errors},status=400)
        except Exception as e:
            return Response({"error": str(e)}, status=500)
        
class LoginView(APIView):
    def post(self,request):
        try:
            username=request.data.get("username","")
            email=request.data.get("email","")
            password=request.data.get("password","")
            if username=="" and email=="":
                return Response({'Error':'Username or Email cant be empty'},status=400)
            user=None
            if username!="":
                user=authenticate(username=username,password=password)
            else:
                try:
                    user_obj = models.CustomUser.objects.get(email=email)
                    user = authenticate(username=user_obj.username, password=password)
                except models.CustomUser.DoesNotExist:
                    user = None

            if user is not None:
                serial=serializers.UserSerializer(user)
                refresh=RefreshToken.for_user(user)
                return Response({'Sucess':'User logged in Sucessfully','data':serial.data,'refresh':str(refresh),'access':str(refresh.access_token)},status=200)
            return Response({'Error':'Invalid credentials'},status=400)
        except Exception as e:
            return Response({"error": str(e)}, status=500)
