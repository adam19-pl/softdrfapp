from rest_framework import serializers
from drfapp.models import Project, STATUS, Comment
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=64, min_length=6, write_only=True)
    email = serializers.EmailField(max_length=256, min_length=4)
    first_name = serializers.CharField(max_length=256, min_length=2)
    last_name = serializers.CharField(max_length=256, min_length=2)

    class Meta:
        model = User
        fields = ['id', 'password', 'username', 'first_name', 'last_name', 'email']
        projects = serializers.ReadOnlyField(source='project.id')

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['project', 'autor', 'date_created', 'comment']
        project = serializers.ReadOnlyField(source='project.title')


class ProjectSerializer(serializers.ModelSerializer):
    employers = serializers.PrimaryKeyRelatedField(many=True, queryset=User.objects.all())

    class Meta:
        model = Project
        fields = ['id', 'owner', 'title', 'description', 'started', 'ended', 'status', 'employers', ]
        owner = serializers.ReadOnlyField(source='owner.username')
