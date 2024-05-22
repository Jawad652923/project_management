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

class Tasks(models.Model):
    project=models.ForeignKey(Projects, related_name='tasks',on_delete=models.CASCADE)
    title=models.CharField(max_length=255,unique=True)
    description=models.TextField()
    status=models.CharField(max_length=255)
    due_date=models.DateField()
    is_deleted=models.BooleanField(default=False)

    def soft_delete(self):
        self.is_deleted=True
        self.save()
