from django.contrib.auth import get_user_model
from django.http import Http404
from rest_framework import status, viewsets
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView, TokenVerifyView)

from auth_user.permissions import IsAllowedToGetObject

from .serializers import (CustomTokenObtainPairSerializer, UserReadSerializer,
                          UserSerializer)


class UserEnvView(viewsets.ReadOnlyModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = UserReadSerializer
    permission_classes = (IsAuthenticated, IsAllowedToGetObject)
    authentication_classes = (JWTAuthentication,)


class TokenObtainCustomView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class TokenRefreshCustomView(TokenRefreshView):
    pass

class TokenRefreshVerifyView(TokenVerifyView):
    pass

class SignupView(CreateAPIView):

    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    
    def post(self, request):
        for key, value in get_user_model().USER_LEVEL_CHOICES:
            if value.casefold() == request.data['role'].casefold():
                self.role_key = key

        try:
            self.role_key
        except:
            return Response({'role': [ 'A role with that name does not exist' ]}, status=status.HTTP_400_BAD_REQUEST)

        user_serializer = self.get_serializer(data={ **request.data, 'role': self.role_key })

        if user_serializer.is_valid(raise_exception=True):
            user_serializer.save()

            return Response({
                'user': 'created'
            }, status=status.HTTP_201_CREATED)

