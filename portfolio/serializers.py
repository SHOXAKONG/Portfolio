from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from portfolio.models import User, Feedback, Contact, Project, Portfolio, ProjectContributor, Files, ProjectUser, \
    Category, CategoryProject


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add custom claims if needed
        token['email'] = user.email
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)
        return data


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email']


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(max_length=200, write_only=True)


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password_confirm = serializers.CharField(write_only=True)  # Add confirmation field

    class Meta:
        model = User
        fields = ['email', 'password', 'password_confirm', 'first_name', 'last_name']

    def validate(self, data):
        """Validate that password and password_confirm match."""
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError(
                {"password": "Passwords do not match."}
            )
        return data

    def create(self, validated_data):
        # Remove password_confirm since it’s not needed for user creation
        validated_data.pop('password_confirm')

        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        return user


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
    project = serializers.PrimaryKeyRelatedField(queryset=Project.objects.all())
    contributor = serializers.PrimaryKeyRelatedField(queryset=ProjectContributor.objects.all())

    class Meta:
        model = ProjectUser
        fields = ['id', 'project', 'contributor', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class ProjectSerializer(serializers.ModelSerializer):
    contributors = ProjectUserSerializer(many=True)

    class Meta:
        model = Project
        fields = ['id','title', 'description', 'start_time', 'end_time', 'git_hub', 'deploy_link', 'contributors']


class PortfolioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Portfolio
        fields = ['id','title', 'description']


class FilesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Files
        fields = ['project', 'name', 'downloaded_date']


class ModeratorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'password', 'first_name', 'last_name']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class CategoryProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryProject
        fields = '__all__'