from rest_framework import  serializers
from django.contrib.auth.models import User
from .models import Projects,Tasks,TaskPermission

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['id','username','email']

class TaskPermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskPermission
        fields = ['can_create', 'can_read', 'can_update', 'can_delete']

class UserWithPermissionsSerializer(serializers.ModelSerializer):
    permissions = TaskPermissionSerializer(source='taskpermission_set', many=True, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'permissions']

    def get_permissions(self, obj):
        project_id = self.context.get('project_id')
        
        task_permission = TaskPermission.objects.filter(user=obj, project_id=project_id).first()
        
        if task_permission:
            return {
                'can_create': task_permission.can_create,
                'can_read': task_permission.can_read,
                'can_update': task_permission.can_update,
                'can_delete': task_permission.can_delete,
            }
        else:
            return {}


class ProjectSerializer(serializers.ModelSerializer):
    users = UserWithPermissionsSerializer(many=True, read_only=True)

    class Meta:
        model = Projects
        fields = ['id', 'users', 'name', 'description', 'is_deleted']

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


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model=Tasks
        fields='__all__'



