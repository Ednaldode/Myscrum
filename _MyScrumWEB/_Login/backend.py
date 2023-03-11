from django.conf import settings
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User

class MyBackend():

    # Verifica se o usuario é valido
    @staticmethod
    def checkUser(username):
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return False
        if user is not None:
            return True

    # Verifica se a senha está correta para um certo usuario
    @staticmethod
    def checkPassword(username, password):
        user = User.objects.get(username=username)

        if check_password(password, user.password):
            return True
        else:
            return False

    # Busca o usuario no banco caso o checkUser e checkPassword retornem True
    def authenticate(username, password):
        if MyBackend.checkUser(username) and MyBackend.checkPassword(username, password):
            user = User.objects.get(username=username)
            return user
        else:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None