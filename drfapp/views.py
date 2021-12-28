from django.shortcuts import render
from rest_framework import generics
from drfapp.models import Project, Comment
from drfapp.serializers import ProjectSerializer, UserSerializer, CommentSerializer
from django.contrib.auth.models import User
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status


class RegisterView(generics.GenericAPIView):
    serializer_class = UserSerializer

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class HaveUserPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.id == request.user.id


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, HaveUserPermission]

    def put(self, request, *args, **kwargs):
        return self.update(request,*args,**kwargs)


class ProjectList(generics.ListCreateAPIView):
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        queryset = Project.objects.filter(owner=self.request.user.id)
        return queryset


class IsProjectOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.owner.id == request.user.id


class ProjectDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated, IsProjectOwner]


class CommentList(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(autor=self.request.user)


class IsCommentOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.autor.id == request.user.id


class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated, IsCommentOwner]
