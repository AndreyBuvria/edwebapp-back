from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import CourseModel, TaskModel
from .serializers import CourseSerializer, TaskSerializer

# Create your views here.

class CourseView(viewsets.ModelViewSet):
    queryset = CourseModel.objects.all()
    serializer_class = CourseSerializer
    permission_classes = (IsAuthenticated, )
    authentication_classes = (JWTAuthentication,)

    def list(self, request, *args, **kwargs):
        usr = JWTAuthentication().authenticate(request)[1]
        filtered_queryset = self.get_queryset().filter(members__in=[usr['user_id']]).extra(order_by=('id',))
        queryset = self.filter_queryset(filtered_queryset)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)

class TaskView(viewsets.ModelViewSet):
    queryset = TaskModel.objects.all()
    serializer_class = TaskSerializer
    permission_classes = (IsAuthenticated, )
    authentication_classes = (JWTAuthentication,)
    