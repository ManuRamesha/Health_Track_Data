# these are rest_framework imports
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.authtoken.models import Token
from rest_framework.pagination import PageNumberPagination

# these are django imports
from django.contrib.auth import authenticate
from django.db.models import Q

# these are local imports
from .serializers import UserSerializer
from .models import User
from user_profile.serializers import ProfileSerializer

# Create your views here.
"""
These RegisterUser class 
"""

class RegisterUser(APIView):

    """
    Handles the user registration process.

    Allows any user to register by providing necessary details. The data is validated using the UserSerializer,
    and the new user is saved into the database. 

    POST request:
        - Accepts user registration data.
        - Returns the user data if successful.
        - Returns errors if the data is invalid.
    """

    permission_classes = [AllowAny]

    """
    Register a new user.

    Accepts:
    - POST request with user data (username, password, email, etc.)

    Returns:
    - 201 CREATED with user data if the registration is successful.
    - 400 BAD REQUEST with validation errors if the data is invalid.
    """

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):

    """
    Login for users to obtain a token.

    Accepts:
    - POST request with 'username' and 'password'.

    Returns:
    - 200 OK with token and user details if login is successful.
    - 400 BAD REQUEST if 'username' or 'password' is missing.
    - 401 UNAUTHORIZED if the credentials are incorrect.
    - 403 FORBIDDEN if the account is deactivated or if the user is an admin.
    """

    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response(
                {"error": "Username and password are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = authenticate(username=username, password=password)
        if user is None:
            return Response(
                {"error": "Invalid username or password."},
                status=status.HTTP_401_UNAUTHORIZED
            )

        if user.role.name == "Admin":
            return Response(
                {"error": "Admin user cannot login from this endpoint."},
                status=status.HTTP_403_FORBIDDEN
            )

        if user is not None:
            if user.is_active:
                token, created = Token.objects.get_or_create(user=user)
                return Response(
                    {
                        "token": token.key,
                        "username": user.username,
                        "email": user.email,
                        "first_name": user.first_name,
                        "last_name": user.last_name
                    },
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {"error": "User account is deactivated."},
                    status=status.HTTP_403_FORBIDDEN
                )
        else:
            return Response(
                {"error": "Invalid username or password."},
                status=status.HTTP_401_UNAUTHORIZED
            )



class AdminRegisterUser(APIView):

    """
    Admin endpoint to register a user.

    Accepts:
    - POST request with user data (username, password, email, etc.)

    Returns:
    - 201 CREATED with user data if the registration is successful.
    - 400 BAD REQUEST with validation errors if the data is invalid.
    """
    permission_classes = [IsAdminUser]

    def post(self, request):

        request.data['role'] = "R01"


        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class AdminLoginView(APIView):

    """
    Admin login endpoint to obtain a token.

    Accepts:
    - POST request with 'username' and 'password'.

    Returns:
    - 200 OK with token and user details if login is successful.
    - 400 BAD REQUEST if 'username' or 'password' is missing.
    - 401 UNAUTHORIZED if the credentials are incorrect.
    """
    permission_classes = [IsAdminUser]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response(
                {"error": "Username and password are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = authenticate(username=username, password=password)
        if user is None:
            return Response(
                {"error": "Invalid username or password."},
                status=status.HTTP_401_UNAUTHORIZED
            )

        if user is not None:
            if user.is_active:
                token, created = Token.objects.get_or_create(user=user)
                return Response(
                    {
                        "token": token.key,
                        "username": user.username,
                        "email": user.email,
                        "first_name": user.first_name,
                        "last_name": user.last_name
                    },
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {"error": "User account is deactivated."},
                    status=status.HTTP_403_FORBIDDEN
                )
        else:
            return Response(
                {"error": "Invalid username or password."},
                status=status.HTTP_401_UNAUTHORIZED
            )
        



class AdminUserCRUDView(APIView):
    """
    Admin view to perform CRUD operations on users.

    Accepts:
    - GET request to fetch all users or a specific user by 'username'.
    - POST request to create a new user.
    - PUT request to update an existing user's details by 'username'.
    - PATCH request to partially update a user's details by 'username'.
    - DELETE request to deactivate a user by 'username'.

    Returns:
    - 200 OK with user data or list of users.
    - 201 CREATED with new user data.
    - 400 BAD REQUEST with validation errors.
    - 404 NOT FOUND if the user is not found.
    - 204 NO CONTENT if the user is successfully deleted or deactivated.
    """
    permission_classes = [IsAdminUser]

    def get(self, request, username = None):
        if username is not None:
            try:
                user = User.objects.get(username = username)
                serializer = UserSerializer(user)
                return Response(serializer.data)
            except User.DoesNotExist:
                return Response({"message":f"User with username {username} does not exist"},status=status.HTTP_404_NOT_FOUND)

        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, username):
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({"message":f"User with username {username} does not exist"}, status=status.HTTP_404_NOT_FOUND)

        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, username):
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({"message":f"User with username {username} does not exist"}, status=status.HTTP_404_NOT_FOUND)

        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, username):
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({"message":f"User with username {username} does not exist"}, status=status.HTTP_404_NOT_FOUND)

        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class UserCRUDView(APIView):

    """
    User view to manage the authenticated user's details.

    Accepts:
    - GET request to fetch the current user's data.
    - PUT request to update the current user's details.
    - PATCH request to partially update the current user's details.
    - DELETE request to deactivate the current user.

    Returns:
    - 200 OK with user data.
    - 400 BAD REQUEST with validation errors.
    - 404 NOT FOUND if the user is not found.
    - 204 NO CONTENT if the user is successfully deactivated.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            user = User.objects.get(username = request.user.username)
            serializer = UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            return Response({"message":f"User with username {request.user.username} does not exist"}, status=status.HTTP_404_NOT_FOUND)
        
    def put(self, request):
        try:
            user = User.objects.get(username=request.user.username)
        except User.DoesNotExist:
            return Response({"message":f"User with username {request.user.username} does not exist"}, status=status.HTTP_404_NOT_FOUND)

        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request):
        try:
            user = User.objects.get(username=request.user.username)
        except User.DoesNotExist:
            return Response({"message":f"User with username {request.user.username} does not exist"}, status=status.HTTP_404_NOT_FOUND)

        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request):
        try:
            user = User.objects.get(username=request.user.username)
        except User.DoesNotExist:
            return Response({"message":f"User with username {request.user.username} does not exist"}, status=status.HTTP_404_NOT_FOUND)

        user.is_active = False
        user.save() 
        Token.objects.filter(user=user).delete()    
        
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class SearchView(APIView):
    """
    Search for users based on query parameters.

    Accepts:
    - GET request with a search query ('q').

    Returns:
    - 200 OK with paginated user search results.
    - 400 BAD REQUEST if no search query is provided.
    - 403 FORBIDDEN if the user is not authorized or deactivated.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):

        if not request.user.is_staff:
            return Response({"message": "You are not authorized to perform this action."}, status=status.HTTP_403_FORBIDDEN)
        
        if not request.user.is_active:
            return Response({"message": "Your account is deactivated."}, status=status.HTTP_403_FORBIDDEN)
        
        search_query = request.GET.get('q', '').strip()


        if not search_query:
            return Response({"message": "Please provide a search query."}, status=status.HTTP_400_BAD_REQUEST)
        
        paginator = PageNumberPagination()
        paginator.page_size = 10
        paginator.page_query_param = 'page_size'
    
        users = User.objects.select_related('profile').filter(
            Q(username__icontains=search_query) |
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(profile__ka_regd_no__icontains=search_query) 
            )
        
        paginated_users = paginator.paginate_queryset(users, request)   

        result = []

        for user in paginated_users:
            user_data = UserSerializer(user).data
            if hasattr(user, 'profile') and user.profile is not None:
                profile_data = ProfileSerializer(user.profile).data
            else:
                profile_data = {}

            user_profile_data = {
                'user': user_data,
                'profile': profile_data
            }

            result.append(user_profile_data)
        
        return paginator.get_paginated_response(result)

    
        
        