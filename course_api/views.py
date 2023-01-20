from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import CourseModel, TaskModel
from .serializers import CourseAddSerializer, CourseListSerializer, TaskSerializer

from core.constants import status_course

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
        else:
            return self.serializers['default'] 

    @action(methods=['get'], detail=False, permission_classes=(IsAuthenticated, ),
            authentication_classes=(JWTAuthentication, ), url_path='usr_joined', url_name='usr_joined')
    def getCoursesUserJoinedTo(self, request):
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
    
    @action(methods=['get'], detail=True, permission_classes=(IsAuthenticated, ),
            authentication_classes=(JWTAuthentication, ), url_path='check_user', url_name='check_user')
    def checkUserMembership(self, request, pk):
        usr_token_data = JWTAuthentication().authenticate(request)[1]
        course = self.get_queryset().get(id=pk)
        usr_in_course = course.members.filter(id=usr_token_data['user_id'])
        
        if not usr_in_course:
            return Response(
                {
                    'status': 'FAILED',
                    'response': {
                        'msg': 'A user has not joined to the course'
                    }
                }, status=status.HTTP_404_NOT_FOUND)
        
        return Response(
            {
                'status': 'OK',
                'response': {}
            }, status=status.HTTP_200_OK)

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
                    'status': status_course.COURSE_CODE_IS_INVALID,
                    'response': {
                        'course': 'A course with such key does not exist' 
                    }
                }, status=status.HTTP_404_NOT_FOUND)

        usr_token_data = JWTAuthentication().authenticate(request)[1]
        usr_in_course = course.members.filter(id=usr_token_data['user_id'])
        
        if not usr_in_course:
            course.members.add(usr_token_data['user_id'])
            return Response(
                { 'status': status_course.USER_JOINED,
                    'response': {
                        'course': {
                            'id': course.id
                        }
                    } 
                }, status=status.HTTP_200_OK)

        return Response(
            { 
                'status': status_course.USER_ALREADY_JOINED,
                'response': {
                    'user': 'A user is already part of this course', 
                }
            }, status=status.HTTP_200_OK)

    @action(methods=['patch'], detail=True, permission_classes=(IsAuthenticated, ),
            authentication_classes=(JWTAuthentication, ), url_path='remove_user', url_name='remove_user')
    def removeUserFromCourse(self, request, pk):
        try:
            course = self.get_queryset().get(id=pk)
        except:
            return Response(
                { 
                    'status': status_course.COURSE_ID_IS_INVALID,
                    'response': {
                        'course': 'A course with such id does not exist' 
                    }
                }, status=status.HTTP_400_BAD_REQUEST)

        usr_token_data = JWTAuthentication().authenticate(request)[1]
        usr_in_course = course.members.filter(id=usr_token_data['user_id'])
        
        if not usr_in_course:
            return Response(
                {
                    'status': status_course.USER_IS_NOT_JOINED,
                    'response': {
                        'msg': 'A user is not joined to the course'
                    }
                }, status=status.HTTP_200_OK
            )

        course.members.remove(usr_token_data['user_id'])
        return Response(
            { 
                'status': status_course.USER_REMOVED,
                'response': {} 
            }, status=status.HTTP_200_OK)


class TaskView(viewsets.ModelViewSet):
    queryset = TaskModel.objects.all()
    serializer_class = TaskSerializer
    permission_classes = (IsAuthenticated, )
    authentication_classes = (JWTAuthentication,)