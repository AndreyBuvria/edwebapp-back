from django.urls import include, path
from rest_framework.routers import DynamicRoute, Route, SimpleRouter

from . import views

simpleRouter = SimpleRouter()
taskRouter = SimpleRouter()
simpleRouter.register(r'course', views.CourseView, 'course')
taskRouter.register(r'task', views.TaskView, 'task')

urlpatterns = [
    path('', include(simpleRouter.urls)),
    path('', include(taskRouter.urls))
]