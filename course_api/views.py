from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import CourseModel, TaskModel
from .serializers import CourseAddSerializer, CourseListSerializer, TaskSerializer

# Create your views here.

class CourseView(viewsets.ModelViewSet):
    queryset = CourseModel.objects.all()
    serializers = {
        'default': CourseListSerializer,
        'add': CourseAddSerializer,
        'task': TaskSerializer,
    }
    permission_classes = (IsAuthenticated, )
    authentication_classes = (JWTAuthentication,)

    def get_serializer_class(self):
        if self.action == 'getTasksByCourseId':
            return self.serializers['task']
        elif self.action == 'addUserToCourse':
            return self.serializers['add']
        return self.serializers['default'] 

    def list(self, request):
        usr = JWTAuthentication().authenticate(request)[1]
        filtered_queryset = self.get_queryset().filter(members__in=[usr['user_id']]).extra(order_by=('id',))
        queryset = self.filter_queryset(filtered_queryset)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=True, permission_classes=(IsAuthenticated, ),
            authentication_classes=(JWTAuthentication, ), url_path='tasks', url_name='tasks')
    def getTasksByCourseId(self, request, pk):
        task_queryset = TaskModel.objects.all()
        queryset = self.filter_queryset(task_queryset.filter(related_course=pk))
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=['patch'], detail=False, permission_classes=(IsAuthenticated, ),
            authentication_classes=(JWTAuthentication, ), url_path='add_user', url_name='add_user')
    def addUserToCourse(self, request):
        key_serializer = self.get_serializer(data=request.data)
        key_serializer.is_valid(raise_exception=True)
        course_key = key_serializer.data['key']
        try:
            course = self.get_queryset().get(key=course_key)
        except:
            return Response(
                { 
                    'status': 'FAILED',
                    'response': {
                        'course': 'A course with such key does not exist' 
                    }
                }, status=status.HTTP_400_BAD_REQUEST)

        usr_token_data = JWTAuthentication().authenticate(request)[1]
        usr_in_course = course.members.filter(id=usr_token_data['user_id'])
        
        if not usr_in_course:
            course.members.add(usr_token_data['user_id'])
            return Response(
                { 'status': 'OK',
                    'response': {
                        'course': {
                            'id': course.id
                        }
                    } 
                }, status=status.HTTP_200_OK)

        return Response(
            { 
                'status': 'OK',
                'response': {
                    'user': 'A user is already part of this course', 
                }
            }, status=status.HTTP_200_OK)


class TaskView(viewsets.ModelViewSet):
    queryset = TaskModel.objects.all()
    serializer_class = TaskSerializer
    permission_classes = (IsAuthenticated, )
    authentication_classes = (JWTAuthentication,)