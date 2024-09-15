from rest_framework import serializers
from .models import ProfileFile
import os

class ProfileFileSerializer(serializers.ModelSerializer):
    file_name = serializers.SerializerMethodField()

    class Meta:
        model = ProfileFile
        fields = ['id', 'file', 'file_name']

    def get_file_name(self, obj):
        return os.path.basename(obj.file.name)
