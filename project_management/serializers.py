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

    def create(self, validated_data):
        users_data = validated_data.pop('users',[])
        project = Projects.objects.create(**validated_data)
        for user in users_data:
            project.users.add(user)
        return project
    
    def update(self, instance, validated_data):        
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.save()
        return instance


class AddUserSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model=Tasks
        fields='__all__'
