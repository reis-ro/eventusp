from rest_framework import serializers

from events.models import Event, Comment


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'author', 'text', 'likes', 'event']


class EventSerializer(serializers.ModelSerializer):
    comment_set = CommentSerializer(many=True)

    class Meta:
        model = Event
        fields = ['id', 'name', 'date', 'time', 'duration', 'place', 
                    'description', 'summary', 'max_participants', 
                    'event_photo_url', 'approved', 'formato', 'tema', 
                    'tipo_organizacao', 'promotor', 'favorito', 'comment_set']