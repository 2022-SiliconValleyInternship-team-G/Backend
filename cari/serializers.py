from rest_framework import serializers
from .models import User, Result


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['user_id']


class ResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = Result
        fields = ('result_id', 'result_img_url', 'user_id', 'result_emotion', 'created_at')