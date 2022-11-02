from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import CustomTokenObtainPairSerializer, UserSerializer
from core.models import Role

class TokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class TokenRefreshView(TokenRefreshView):
    pass

class SignupView(APIView):

    serializer_class = UserSerializer
    
    def post(self, request):
        first_name = request.data['firstname']
        last_name = request.data['lastname']
        username = request.data['username']
        role_name = request.data['role']
        email = request.data['email']
        about = request.data['about']
        password = request.data['password']

        try:
            role = Role.objects.get(name__iexact=role_name).pk
        except:
            return Response({'role': [ 'A role with that name does not exist' ]}, status=status.HTTP_400_BAD_REQUEST)

        user_dict = {
            'first_name': first_name,
            'last_name': last_name,
            'username': username,
            'role': role,
            'email': email,
            'about': about,
            'password': password
        }

        user_serializer = self.serializer_class(data=user_dict)

        if user_serializer.is_valid(raise_exception=True):
            user_serializer.save()

            return Response({
                'user': 'created'
            }, status=status.HTTP_201_CREATED)

