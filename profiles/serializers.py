import os

from django.contrib.auth.models import User
from rest_framework import serializers

from config.serializers import SkillSerializer, StateSerializer, TrainingSerializer

from .models import Comment, Profile, ProfileFile, FollowUp


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']  # Adjust the fields as needed


class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Comment
        fields = ['id', 'text', 'user', 'creation_date']

        extra_kwargs = {
            'creation_date': {'format': '%d/%m/%Y %H:%M:%S'}
        }


class FollowUpSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = FollowUp
        fields = ['id', 'text', 'user', 'creation_date']

        extra_kwargs = {
            'creation_date': {'format': '%d/%m/%Y %H:%M:%S'}
        }


class ProfileFileSerializer(serializers.ModelSerializer):
    file_name = serializers.SerializerMethodField()

    class Meta:
        model = ProfileFile
        fields = ['id', 'file', 'file_name']

    def get_file_name(self, obj):
        return os.path.basename(obj.file.name)


class ProfileSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True)
    followups = FollowUpSerializer(many=True)
    skills = SkillSerializer(many=True)
    trainings = TrainingSerializer(many=True)
    # Include if you have files related to profiles
    files = ProfileFileSerializer(many=True)
    state = StateSerializer()

    class Meta:
        model = Profile
        fields = ['id', 'name', 'surname', 'email', 'state', 'number', 'town', 'creation_date',
                  'update_date', 'comments', 'followups', 'birthday', 'diplomas', 'skills', 'trainings', 'files']
        extra_kwargs = {
            'creation_date': {'format': '%d/%m/%Y'},
            'update_date': {'format': '%d/%m/%Y %H:%M:%S'},
        }
