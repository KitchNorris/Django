from rest_framework import serializers
from django.contrib.auth.models import User
from polls.models import Topic


class UserSerializer(serializers.ModelSerializer):
    topic = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'topic']


class TopicSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Topic
        fields = ['text', 'pub_date', 'owner', 'id']

