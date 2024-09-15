from rest_framework import serializers

from profileFile.serializers import ProfileFileSerializer
from skills.serializers import SkillSerializer
from .models import Profile, Comment
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']  # Adjust the fields as needed


class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer() 
    class Meta:
        model = Comment
        fields = ['id', 'text', 'user', 'creation_date']


class ProfileSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True)
    skills = SkillSerializer(many=True)
    # Include if you have files related to profiles
    files = ProfileFileSerializer(many=True)

    class Meta:
        model = Profile
        fields = ['id', 'name', 'surname', 'email', 'number', 'town', 'creation_date',
                  'update_date', 'comments', 'state', 'diplomas', 'skills', 'files']
        extra_kwargs = {
            'creation_date': {'format': '%d/%m/%Y'},
            'update_date': {'format': '%d/%m/%Y %H:%M:%S'},
        }
