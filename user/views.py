from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.authtoken.models import Token
from rest_framework.pagination import PageNumberPagination




from django.contrib.auth import authenticate
from django.db.models import Q


from .serializers import UserSerializer
from .models import User
from user_profile.serializers import ProfileSerializer

# Create your views here.
class RegisterUser(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
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
    permission_classes = [IsAdminUser]

    def post(self, request):

        request.data['role'] = "R01"


        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class AdminLoginView(APIView):
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

    
        
        