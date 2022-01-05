from rest_framework import serializers
from drfapp.models import Project, STATUS, Comment, NewUser, GENDER


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=64, min_length=6, write_only=True)
    email = serializers.EmailField(max_length=256, min_length=4)
    firstname = serializers.CharField(max_length=256, min_length=2)
    lastname = serializers.CharField(max_length=256, min_length=2)
    gender = serializers.ChoiceField(choices=GENDER)
    phone = serializers.CharField(max_length=12, allow_blank=True)
    age = serializers.IntegerField(min_value=1, max_value=100)

    class Meta:
        model = NewUser
        fields = ['id', 'password', 'firstname', 'lastname', 'email', 'age', 'phone', 'gender']
        projects = serializers.ReadOnlyField(source='project.id')

    def create(self, validated_data):
        return NewUser.objects.create_user(**validated_data)


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id','project', 'autor', 'date_created', 'comment']
        project = serializers.ReadOnlyField(source='project.title')


class ProjectSerializer(serializers.ModelSerializer):
    employers = serializers.PrimaryKeyRelatedField(many=True, queryset=NewUser.objects.all())

    class Meta:
        model = Project
        fields = ['id', 'owner', 'title', 'description', 'started', 'ended', 'status', 'employers', ]
        owner = serializers.ReadOnlyField(source='owner.username')
