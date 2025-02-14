# these are rest_framework imports
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.exceptions import PermissionDenied

# these are local imports
from .models import Profile
from .serializers import ProfileSerializer


# Create your views here.
class ProfileCRUDView(APIView):
    """
    APIView to perform CRUD operations on the authenticated user's Profile.

    Allows the authenticated user to:
    - Retrieve their profile via a GET request.
    - Create a new profile via a POST request.
    - Update an existing profile via a PUT request.
    - Partially update an existing profile via a PATCH request.

    Permissions:
    - Requires the user to be authenticated.

    Methods:
    - GET: Fetch the user's profile.
    - POST: Create a new profile for the authenticated user.
    - PUT: Fully update the user's profile.
    - PATCH: Partially update the user's profile.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Retrieve the profile of the authenticated user.

        Returns:
        - 200 OK with the profile data if the profile is found.
        - 404 NOT FOUND if the user's profile does not exist.
        """
        user = request.user
        try:
            profile = Profile.objects.get(user=user)
            serializer = ProfileSerializer(profile)
            return Response(serializer.data)
        except Profile.DoesNotExist:
            return Response({"message": "Profile not found"}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request):

        """
        Create a new profile for the authenticated user.

        Accepts:
        - POST request with profile data.

        Returns:
        - 201 CREATED with the new profile data if successful.
        - 400 BAD REQUEST if the data is invalid.
        """
        user = request.user
        serializer = ProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        """
        Fully update the user's profile.

        Accepts:
        - PUT request with updated profile data.

        Returns:
        - 200 OK with the updated profile data if successful.
        - 400 BAD REQUEST if the data is invalid.
        - 404 NOT FOUND if the user's profile does not exist.
        """

        user = request.user
        try:
            profile = Profile.objects.get(user=user)
            serializer = ProfileSerializer(profile, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Profile.DoesNotExist:
            return Response({"message": "Profile not found"}, status=status.HTTP_404_NOT_FOUND)

    def patch(self, request):

        """
        Partially update the user's profile.

        Accepts:
        - PATCH request with partial profile data.

        Returns:
        - 200 OK with the partially updated profile data if successful.
        - 400 BAD REQUEST if the data is invalid.
        - 404 NOT FOUND if the user's profile does not exist.
        """
        user = request.user
        try:
            profile = Profile.objects.get(user=user)
            serializer = ProfileSerializer(profile, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Profile.DoesNotExist:
            return Response({"message": "Profile not found"}, status=status.HTTP_404_NOT_FOUND)

