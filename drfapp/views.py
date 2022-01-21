from django.shortcuts import render
from rest_framework import generics, permissions
from drfapp.models import Project, Comment, NewUser
from drfapp.serializers import ProjectSerializer, UserSerializer, CommentSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated, BasePermission
from rest_framework_simplejwt.tokens import RefreshToken
import re


class RegisterView(APIView):
    permission_classes = [AllowAny]
    serializer_class = UserSerializer

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            if NewUser.objects.filter(email=request.data['email']).exists():
                return Response({"Error": "This email is already in use"}, status=status.HTTP_400_BAD_REQUEST)
            if not re.match("^[a-zA-Z]*$", request.data['firstname']) or not re.match("^[a-zA-Z]*$",
                                                                                      request.data['lastname']):
                return Response({"Error": "Firstname and lastname field cannot contain special characters or numbers"},
                                status=status.HTTP_400_BAD_REQUEST)
            if request.data['age'] not in range(1, 101):
                return Response({"Error": "Age must be set between 1-100"}, status=status.HTTP_400_BAD_REQUEST)
            newuser = serializer.save()
            if newuser:
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BlackListTokenView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class UserList(generics.ListAPIView):
    queryset = NewUser.objects.all()
    serializer_class = UserSerializer


class HaveUserPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.id == request.user.id


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    model = NewUser
    queryset = NewUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, HaveUserPermission]

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def put(self, request, pk, *args, **kwargs):
        self.object = self.get_object()
        serializer = UserSerializer(data=request.data)
        if self.object.id != pk:
            return Response({"Error": "You don't have permission to make this action."},
                            status=status.HTTP_400_BAD_REQUEST)
        if serializer.is_valid():
            self.update(request, *args, **kwargs)
            self.object.set_password(request.data['password'])
            self.object.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk, *args, **kwargs):
        self.object = self.get_object()
        if self.object.id != pk:
            return Response({"Error": "You don't have permission to make this action."},
                            status=status.HTTP_400_BAD_REQUEST)
        self.object.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProjectList(APIView):
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        queryset = Project.objects.filter(employers=request.user.id)
        serializer = ProjectSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            if Project.objects.filter(title=request.data['title']).exists():
                return Response(
                    {"Error": "Sorry the title of this project already exists. Please go back and change the title"},
                    status=status.HTTP_400_BAD_REQUEST)
            if str(request.data['owner']) not in request.data['employers']:
                return Response({"Error": "The owner must be selected on the employers list! Please go back."},
                                status=status.HTTP_400_BAD_REQUEST)
            project = serializer.save()
            if project:
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProjectDetail(APIView):
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated, ]

    def get(self, request, pk):
        queryset = Project.objects.filter(id=pk)
        serializer = ProjectSerializer(queryset, many=True)
        if Project.objects.filter(employers=request.user.id):
            return Response(serializer.data)
        return Response({"Error": "You don't have permission to view this project"}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk, *args, **kwargs):
        try:
            project_object = Project.objects.get(pk=pk)
        except Project.DoesNotExist:
            return Response({"Error": "Project not exist"}, status=status.HTTP_400_BAD_REQUEST)
        serializer = ProjectSerializer(project_object, data=request.data)
        if serializer.is_valid():
            if project_object.owner.id != request.user.id:
                return Response({"Error": "You don't have permission to edit this project"},
                                status=status.HTTP_400_BAD_REQUEST)
            if str(request.data['owner']) not in request.data['employers']:
                return Response({"Error": "The owner must be selected on the employers list! Please change this."},
                                status=status.HTTP_400_BAD_REQUEST)
            project = serializer.save()
            if project:
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            project_object = Project.objects.get(pk=pk)
        except Project.DoesNotExist:
            return Response({"Error": "Project not exist"}, status=status.HTTP_400_BAD_REQUEST)
        if project_object.id != pk:
            return Response({"Error": "You don't have permission to make this action1"},
                            status=status.HTTP_400_BAD_REQUEST)
        if project_object.owner.id != request.user.id:
            return Response({"Error": "You don't have permission to make this action"},
                            status=status.HTTP_400_BAD_REQUEST)
        project_object.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CommentList(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(autor=self.request.user)


class IsCommentOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.autor.id == request.user.id


class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsCommentOwner]
