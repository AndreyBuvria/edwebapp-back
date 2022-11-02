from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.SignupView.as_view()),
    path('token/', views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', views.TokenRefreshView.as_view(), name='token_refresh')
]