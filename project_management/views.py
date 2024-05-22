from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Projects, Tasks
from .serializers import ProjectSerializer, TaskSerializer
from django.contrib.auth.models import User


class ProjectViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        queryset = Projects.objects.filter(is_deleted=False)
        serializer = ProjectSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        try:
            project = Projects.objects.get(pk=pk, is_deleted=False)
        except Projects.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ProjectSerializer(project)
        return Response(serializer.data)

    def update(self, request, pk=None):
        try:
            project = Projects.objects.get(pk=pk, is_deleted=False)
        except Projects.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ProjectSerializer(project, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        try:
            project = Projects.objects.get(pk=pk, is_deleted=False)
        except Projects.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        project.soft_delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['put'], url_path='add_user')
    def add_user(self, request, pk=None):
        try:
            project = Projects.objects.get(pk=pk, is_deleted=False)
        except Projects.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        user_id = request.data.get('user_id')
        try:
            user = User.objects.get(id=user_id)
            project.users.add(user)
            return Response({'status': 'user added'}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)


class TaskViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        queryset = Tasks.objects.filter(is_deleted=False)
        serializer = TaskSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        try:
            task = Tasks.objects.get(pk=pk, is_deleted=False)
        except Tasks.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = TaskSerializer(task)
        return Response(serializer.data)

    def update(self, request, pk=None):
        try:
            task = Tasks.objects.get(pk=pk, is_deleted=False)
        except Tasks.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = TaskSerializer(task, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        try:
            task = Tasks.objects.get(pk=pk, is_deleted=False)
        except Tasks.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        task.soft_delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
