from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active']
        write_only_fields = ['password']

class ObtainTokenPairWithUserSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data['user'] = UserSerializer(self.user).data
        return data

class PosteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Poste
        fields = "__all__"

class PersonnelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Personnel
        fields = "__all__"

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['poste'] = str(instance.poste)
        return representation