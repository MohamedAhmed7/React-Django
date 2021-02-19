from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import generics, status
from .serializers import RoomSerializer, CreateSerializer
from .models import Room
from rest_framework.views import APIView
from rest_framework.response import Response

class RoomView(generics.ListAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

class CreateRoomView(APIView):
    
    serializer_class = CreateSerializer

    def validate(self, votes):
        return isinstance(votes, int)
    def post(self, request, format=None):
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()
        
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            guest_can_pause = serializer.data.get('guest_can_pause')
            votes_to_skip = serializer.data.get('votes_to_skip')
            if not self.validate(votes_to_skip):
                return Response({'msg': 'error params'}, status.HTTP_400_BAD_REQUEST)
            host = self.request.session.session_key
            # check if the user has a asession already
            query_set = Room.objects.filter(host = host)
            if query_set.exists():
                # fetch it and update settings
                room = query_set[0]
                room.guest_can_pause = guest_can_pause
                room.votes_to_skip = votes_to_skip
                room.save(update_fields=['guest_can_pause', 'votes_to_skip'])
            else:
                room = Room(host = host, guest_can_pause = guest_can_pause, votes_to_skip = votes_to_skip) 
                room.save()
            return Response(RoomSerializer(room).data, status=status.HTTP_201_CREATED)

