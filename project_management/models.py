from django.db import models
from django.contrib.auth.models import User

class Projects(models.Model):
    name= models.CharField(max_length=255,unique=True)
    description=models.TextField()
    users = models.ManyToManyField(User, related_name='user_projects')
    is_deleted=models.BooleanField(default=False)
    
    def soft_delete(self):
        self.is_deleted=True
        self.save()

    def assign_task_permission(self,user,permissions):
        task_permission ,created =TaskPermission.objects.get_or_create(user=user,project=self)
        task_permission.can_create = permissions.get('can_create',False)
        task_permission.can_read = permissions.get('can_read',False)
        task_permission.can_update = permissions.get('can_update',False)
        task_permission.can_delete = permissions.get('can_delete',False)
    
    def get_users_with_permissions(self):
        return User.objects.filter(user_project=self)

class Tasks(models.Model):
    project=models.ForeignKey(Projects, related_name='task_name',on_delete=models.CASCADE)
    title=models.CharField(max_length=255,unique=True)
    description=models.TextField() 
    status=models.CharField(max_length=255)
    due_date=models.DateField()
    is_deleted=models.BooleanField(default=False)

    def soft_delete(self):
        self.is_deleted=True
        self.save()


class TaskPermission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Projects, on_delete=models.CASCADE)
    can_create = models.BooleanField(default=True)
    can_read   = models.BooleanField(default=True)
    can_update = models.BooleanField(default=True)
    can_delete = models.BooleanField(default=True)