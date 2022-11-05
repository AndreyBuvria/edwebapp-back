from django.urls import include, path
from rest_framework.routers import SimpleRouter

from . import views

router = SimpleRouter()
router.register(r'users', views.UserEnvView)

urlpatterns = [
    path('signup/', views.SignupView.as_view()),
    path('token/', views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', views.TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', views.TokenRefreshVerifyView.as_view(), name='token-verify'),

    path('', include(router.urls))
]