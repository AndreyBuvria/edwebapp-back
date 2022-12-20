from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r'course', views.CourseView, 'course')
router.register(r'task', views.TaskView, 'task')

urlpatterns = [
    path('', include(router.urls))
]