from rest_framework import serializers
from ..models import Tasks
from .user_serializers import UserWithPermissionsSerializer

class TaskSerializer(serializers.ModelSerializer):
    users = serializers.SerializerMethodField()

    class Meta:
        model = Tasks
        fields = ['id', 'title', 'description', 'status', 'due_date', 'is_deleted', 'project', 'users']

    def get_users(self, obj):
        users = obj.users.all()
        return UserWithPermissionsSerializer(users, many=True, context={'task_id': obj.id}).data
