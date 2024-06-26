from rest_framework import serializers
from ..models import Projects
from .user_serializers import UserWithPermissionsSerializer


class ProjectSerializer(serializers.ModelSerializer):
    users = serializers.SerializerMethodField()

    class Meta:
        model = Projects
        fields = ['id', 'users', 'name', 'description', 'is_deleted']

    def get_users(self, obj):
        users_with_permissions = obj.users.all()
        serializer_context = {'project_id': obj.id}
        return UserWithPermissionsSerializer(users_with_permissions, many=True, context=serializer_context).data

    def create(self, validated_data):
        users_data = validated_data.pop('users', [])
        project = Projects.objects.create(**validated_data)
        for user in users_data:
            project.users.add(user)
        return project


class UpdateProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Projects
        fields = ['name', 'description']

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.save()
        return instance


class AddUserSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
