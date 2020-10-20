from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_jwt.serializers import JSONWebTokenSerializer

from accounting.serializers import UserSerializer


class CreateAccountAPIView(APIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        password = self.request.data.get("password")
        token_serializer = JSONWebTokenSerializer(data={"username": user.username, "password": password})
        token_serializer.is_valid(raise_exception=True)
        res = {
            "token": token_serializer.validated_data.get("token"),
        }
        return Response(res, status=status.HTTP_201_CREATED)


class GetUserDataAPIView(RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()

    def get_object(self):
        return self.request.user
