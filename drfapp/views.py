from django.shortcuts import render
from rest_framework import generics
from drfapp.models import Project, Comment, NewUser
from drfapp.serializers import ProjectSerializer, UserSerializer, CommentSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated, BasePermission
from rest_framework_simplejwt.tokens import RefreshToken


class RegisterView(APIView):
    permission_classes = [AllowAny]
    serializer_class = UserSerializer

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            if NewUser.objects.filter(email=request.data['email']).exists():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
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
    queryset = NewUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, HaveUserPermission]

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)


class ProjectList(generics.ListCreateAPIView):
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated, AllowAny]

    def perform_create(self, request):

        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            if Project.objects.filter(title=request.data['title']).exists():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            project = serializer.save()
            if project:
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_queryset(self):
        queryset = Project.objects.filter(employers=self.request.user.id)
        return queryset


class IsProjectOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.owner.id == request.user.id


class ProjectDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]


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
