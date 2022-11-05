from rest_framework.permissions import SAFE_METHODS, BasePermission
from rest_framework_simplejwt.authentication import JWTAuthentication


class IsAllowedToGetObject(BasePermission):
    
    @staticmethod
    def get_jwtinstance():
        return JWTAuthentication()

    def has_object_permission(self, request, view, obj):
        jwt_instance = self.get_jwtinstance()
        user_by_token = JWTAuthentication.authenticate(jwt_instance, request)
        user_by_token_id = user_by_token[1]['user_id']
        user_requested_id = obj.id
        
        return bool(user_by_token_id == user_requested_id)
