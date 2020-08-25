from rest_framework.permissions import (
    AllowAny,
    IsAdminUser,
    IsAuthenticated,
)
from .serializers import (
    UserCreateSerializer,
    UserPasswordUpdateSerializer,
    UserUpdateSerializer,
    UserListSerializer,
)
from .models import CustomUser


from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
    DestroyAPIView,
    CreateAPIView,
)
from .permissions import IsAdminOrIsOwner
from rest_framework import status
from rest_framework.response import Response


class UserCreateView(CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = [AllowAny]


class UserListView(ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserListSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]


class UserDetailView(RetrieveAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserListSerializer
    permission_classes = [IsAuthenticated, IsAdminOrIsOwner]


class UserUpdateView(UpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserUpdateSerializer
    permission_classes = [IsAuthenticated, IsAdminOrIsOwner]


class UserDeleteView(DestroyAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserListSerializer
    permission_classes = [IsAuthenticated, IsAdminOrIsOwner]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        data = {"detail": "User deleted successfully."}
        return Response(data=data, status=status.HTTP_204_NO_CONTENT)

    # def delete(self, request, *args, **kwargs):
    #     response = super(CreateUserView, self).create(request, *args, **kwargs)
    #     token, created = Token.objects.get_or_create(user=serializer.instance)
    #     response.status = status.HTTP_200_OK
    #     response.data = {'token': token.key}
    #     return response


class UserPasswordUpdateView(DestroyAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserPasswordUpdateSerializer
    permission_classes = [IsAuthenticated, IsAdminOrIsOwner]

