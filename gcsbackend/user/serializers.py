from rest_framework.serializers import ModelSerializer,ValidationError
from . import models

class UserSerializer(ModelSerializer):
    class Meta:
        model=models.CustomUser
        fields=['username','email','type','password']
        extra_kwargs = {"password": {"write_only": True}}

    def validate(self,data):
        if models.CustomUser.objects.filter(username=data.get("username")).exists():
            raise ValidationError({'Error':'Username Already Registered'})
        elif models.CustomUser.objects.filter(email=data.get("Email")).exists():
            raise ValidationError({'Error':'Email Already Registered'})
        return data
    def create(self, validated_data):
        password = validated_data.pop("password")
        user = models.CustomUser(**validated_data)
        user.set_password(password) 
        user.save()
        return user