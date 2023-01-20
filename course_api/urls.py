from django.urls import include, path
from rest_framework.routers import SimpleRouter

from . import views

courseRouter = SimpleRouter()
taskRouter = SimpleRouter()
courseRouter.register(r'course', views.CourseView, 'course')
taskRouter.register(r'task', views.TaskView, 'task')

urlpatterns = [
    path('', include(courseRouter.urls)),
    path('', include(taskRouter.urls))
]