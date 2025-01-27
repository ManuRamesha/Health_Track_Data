from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.authtoken.models import Token
from rest_framework.pagination import PageNumberPagination


from django.contrib.auth import authenticate


from .serializers import UserSerializer
from .models import User

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