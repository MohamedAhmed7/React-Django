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
                self.request.session['room_code'] = room.code

            else:
                room = Room(host = host, guest_can_pause = guest_can_pause, votes_to_skip = votes_to_skip) 
                room.save()
                self.request.session['room_code'] = room.code

            return Response(RoomSerializer(room).data, status=status.HTTP_201_CREATED)
    
class GetRoom(APIView):
    serializer_class = RoomSerializer
    lookup_url_kwarg = 'code'

    def get(self, request, format=None):
        code = request.GET.get(self.lookup_url_kwarg)

        if code != None:
            room = Room.objects.filter(code = code)

            if len(room) > 0: 
                data = RoomSerializer(room[0]).data
                data['is_host'] = self.request.session.session_key == room[0].host
                return Response(data, status=status.HTTP_200_OK)

            return Response({'Room not found': 'invalid room code'}, status=status.HTTP_404_NOT_FOUND)
        
        return Response({'Bad Request': 'Code Room Not found in URL'}, status=status.HTTP_404_NOT_FOUND)

class JoinRoom(APIView):
    lookup_url_kwarg = 'code'
    
    
    def post(self, request, format=None):
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()
        
        try: 
            code = request.data.get(self.lookup_url_kwarg)
        except:
            return Response({'Bad Request': "invalid input data"}, status=status.HTTP_400_BAD_REQUEST)

        if code != None:
            room_result = Room.objects.filter(code = code)
            
            if len(room_result) > 0:
                room = room_result[0]
                self.request.session['room_code'] = room.code
                return Response({"message": "user joined Room Successfully"}, status=status.HTTP_200_OK)
            
            return Response({'Bad Request': "room not found"}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({'Bad Request': "room code not found in url"}, status=status.HTTP_400_BAD_REQUEST)