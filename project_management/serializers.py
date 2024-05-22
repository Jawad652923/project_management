from rest_framework import  serializers
from django.contrib.auth.models import User
from .models import Projects,Tasks

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['id','username','email']


class ProjectSerializer(serializers.ModelSerializer):
    users = UserSerializer(many=True , read_only=True)

    class Meta:
        model=Projects
        fields='__all__'

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model=Tasks
        fields='__all__'
