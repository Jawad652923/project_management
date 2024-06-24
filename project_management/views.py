from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from .models import Projects, Tasks
from .serializers import ProjectSerializer, TaskSerializer, AddUserSerializer
import logging


class ProjectListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        projects = Projects.objects.filter(is_deleted=False)
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            project = serializer.save()

            user_ids = request.data.get('user_ids', [])
            success, error_message = self.add_users(project, user_ids)
            if success:
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                project.delete()
                return Response({'error': error_message}, status=status.HTTP_404_NOT_FOUND)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def add_users(self, project, user_ids):
        try:
            for user_id in user_ids:
                user = User.objects.get(id=user_id)
                project.users.add(user)
            return True, ""
        except User.DoesNotExist:
            return False, "One or more users not found"


class ProjectDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        return get_object_or_404(Projects, pk=pk, is_deleted=False)

    def get(self, request, pk):
        project = self.get_object(pk)
        serializer = ProjectSerializer(project)
        return Response(serializer.data)

    def put(self, request, pk):
        project = self.get_object(pk)
        serializer = ProjectSerializer(project, data=request.data)

        if 'user_ids' in request.data:
            context = {'action': 'add_user'}
            serializer = ProjectSerializer(project, data=request.data, context=context)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        project = self.get_object(pk)
        project.soft_delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProjectAddUserAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, pk):
        project = get_object_or_404(Projects, pk=pk, is_deleted=False)
        logging.debug(f"Request data: {request.data}")
        serializer = AddUserSerializer(data=request.data)
        if serializer.is_valid():
            user_id = serializer.validated_data['user_id']
            try:
                user = User.objects.get(id=user_id)
                project.users.add(user)
                return Response({'status': 'user added'}, status=status.HTTP_200_OK)
            except User.DoesNotExist:
                return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        logging.debug(f"Serializer errors: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProjectAssignPermissionsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        project = get_object_or_404(Projects, pk=pk, is_deleted=False)
        user_id = request.data.get('user_id')
        permissions = {
            'can_create': request.data.get('can_create', False),
            'can_read': request.data.get('can_read', False),
            'can_update': request.data.get('can_update', False),
            'can_delete': request.data.get('can_delete', False),
        }
        try:
            user = User.objects.get(id=user_id)
            project.assign_task_permissions(user, permissions)
            return Response({'status': 'Permissions assigned'}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)


class TaskListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        tasks = Tasks.objects.filter(is_deleted=False)
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TaskDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        return get_object_or_404(Tasks, pk=pk, is_deleted=False)

    def get(self, request, pk):
        task = self.get_object(pk)
        serializer = TaskSerializer(task)
        return Response(serializer.data)

    def put(self, request, pk):
        task = self.get_object(pk)
        serializer = TaskSerializer(task, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        task = self.get_object(pk)
        task.soft_delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
