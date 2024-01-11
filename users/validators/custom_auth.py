from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q


class CustomAuthenticationBackend(ModelBackend):
    @staticmethod
    def __get_user(username):
        UserModel = get_user_model()
        try:
            return UserModel.objects.get(Q(username=username) | Q(email=username))
        except UserModel.DoesNotExist:
            return None

    def authenticate(self, request, username=None, password=None, **kwargs):
        user = self.__get_user(username)
        if user is not None and user.check_password(password):
            return user
