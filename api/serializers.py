from rest_framework import serializers
from .models import Room


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['id', 'code', 'host', 'guest_can_pause', 'votes_to_skip', 'created_at']
        #fields = '__all__'

class CreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['guest_can_pause', 'votes_to_skip']


class UpdateSerializer(serializers.ModelSerializer):
    code = serializers.CharField(validators=[])

    class Meta:
        model = Room
        fields = ['guest_can_pause', 'votes_to_skip', 'code']