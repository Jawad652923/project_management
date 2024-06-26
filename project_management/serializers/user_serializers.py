from rest_framework import serializers
from django.contrib.auth.models import User
# from .permission_serializers import TaskPermissionSerializer
from ..models import TaskPermission


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class UserWithPermissionsSerializer(serializers.ModelSerializer):
    permissions = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'permissions']

    def get_permissions(self, obj):
        project_id = self.context.get('project_id')
        try:
            task_permission = TaskPermission.objects.get(user=obj, project_id=project_id)
            return {
                'can_create': task_permission.can_create,
                'can_read': task_permission.can_read,
                'can_update': task_permission.can_update,
                'can_delete': task_permission.can_delete,
            }
        except TaskPermission.DoesNotExist:
            return {}
