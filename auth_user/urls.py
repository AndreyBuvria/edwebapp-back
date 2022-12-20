from django.urls import include, path
from rest_framework.routers import SimpleRouter

from . import views

router = SimpleRouter()
router.register(r'users', views.UserEnvView)

urlpatterns = [
    path('signup/', views.SignupView.as_view()),
    path('token/', views.TokenObtainCustomView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', views.TokenRefreshCustomView.as_view(), name='token_refresh'),
    path('token/verify/', views.TokenRefreshVerifyView.as_view(), name='token-verify'),
    path('role/verify/', views.RoleVerifyView.as_view(), name='role-verify'),

    path('', include(router.urls))
]