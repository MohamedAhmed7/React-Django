from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import generics, status
from .serializers import RoomSerializer, CreateSerializer, UpdateSerializer
from .models import Room
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse

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

class UserInRoom(APIView):
    
    def get(self, request, format=None):
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()

        data = {
            'code': self.request.session.get('room_code')
        }

        return JsonResponse(data, status=status.HTTP_200_OK)

class LeaveRoom(APIView):

    def post(self, request, format=None):
        if 'room_code' in self.request.session:
            self.request.session.pop('room_code')
            host_id = self.request.session.session_key
            query = Room.objects.filter(host = host_id)
            if len(query) > 0 :
                room = query[0]
                room.delete()

        return Response({"message": "room dystroied"}, status=status.HTTP_200_OK)

class UpdateRoom(APIView):

    serializer_class = UpdateSerializer

    def patch(self, request, format=None):

        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()

        serializer = self.serializer_class(data= request.data)
        if serializer.is_valid():
            guest_can_pause = serializer.data.get('guest_can_pause')
            votes_to_skip = serializer.data.get('votes_to_skip')
            code = serializer.data.get('code')

            query_set = Room.objects.filter(code = code)
            if not query_set.exists():
                return Response({"message": "Room Not Found"}, status=status.HTTP_404_NOT_FOUND)

            room = query_set[0]

            # check user is host or not 
            user_id = self.request.session.session_key
            if user_id != room.host:
                return Response({"message": "Not Allowed"}, status=status.HTTP_401_UNAUTHORIZED)
            
            room.guest_can_pause = guest_can_pause
            room.votes_to_skip = votes_to_skip
            room.save(update_fields=['guest_can_pause', 'votes_to_skip'])
            return Response(RoomSerializer(room).data, status=status.HTTP_200_OK)
        
        return Response({"Bad Request", "Invalid Data..."}, status=status.HTTP_400_BAD_REQUEST)
