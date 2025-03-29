from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework.exceptions import ValidationError
from portfolio.models import User, Feedback, Contact, Project, Portfolio, ProjectContributor, Files, ProjectUser


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=200)
    password = serializers.CharField(max_length=200)

    def validate(self, data):
        username = data.get("username")
        password = data.get("password")

        user = authenticate(username=username, password=password)

        if not user:
            raise ValidationError("User not found")
        if not user.is_active:
            raise ValidationError("User not found")

        return {"user": user}


class RegisterSerializer(serializers.ModelSerializer):
    re_password = serializers.CharField(max_length=200)

    class Meta:
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "password",
            "re_password")

    def validate(self, data):
        re_password = data.pop("re_password")
        password = data.get("password")
        if re_password != password:
            raise ValidationError("Password do not match")
        return data

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = ['author_name', 'feedback', 'rating', 'project']


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'message']


class ProjectContributerSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectContributor
        fields = ['full_name', 'email', 'github_link', 'linkedin_link', 'position']


class ProjectUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectUser
        fields = ['project', 'contributor']


class ProjectSerializer(serializers.ModelSerializer):
    contributors = ProjectUserSerializer(many=True)

    class Meta:
        model = Project
        fields = ['title', 'description', 'start_time', 'end_time', 'git_hub', 'deploy_link', 'contributors']


class PortfolioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Portfolio
        fields = ['title', 'description']


class FilesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Files
        fields = ['project', 'name', 'downloaded_date']


class ModeratorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'first_name', 'last_name']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
