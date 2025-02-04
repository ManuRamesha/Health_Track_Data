from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import DailyTrack
from .serializers import DailyTrackSerializer

# Create your views here.
class DailyTrackViewCRUDView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        daily_tracks = DailyTrack.objects.filter(user=request.user)
        serializer = DailyTrackSerializer(daily_tracks, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = DailyTrackSerializer(data=request.data)
        request.data['user'] = request.user.id
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        user = request.user
        daily_track = DailyTrack.objects.get(user=user)
        serializer = DailyTrackSerializer(daily_track, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request):
        user = request.user
        daily_track = DailyTrack.objects.get(user=user)
        serializer = DailyTrackSerializer(daily_track, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    