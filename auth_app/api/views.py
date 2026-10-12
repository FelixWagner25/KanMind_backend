from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from .serializers import UserRegistrationSerializer


class RegistrationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            new_user = serializer.save()
            new_user_token = Token.objects.get(user=new_user).key
            return Response({"token": new_user_token, "fullname": new_user.username, "email": new_user.email, "user_id": new_user.id})
        return Response(serializer.errors)
