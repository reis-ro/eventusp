from rest_framework import serializers

from events.models import Event, Comment


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'author', 'text', 'event']


class EventSerializer(serializers.ModelSerializer):
    #comment_set = CommentSerializer(many=True)

    class Meta:
        model = Event
        fields = ['id', 'name', 'date', 'event_photo_url']