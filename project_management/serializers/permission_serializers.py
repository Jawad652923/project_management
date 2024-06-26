from rest_framework import serializers
from ..models import TaskPermission


class TaskPermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskPermission
        fields = ['can_create', 'can_read', 'can_update', 'can_delete']
