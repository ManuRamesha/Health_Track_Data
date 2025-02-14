# these are rest_framework imports
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.exceptions import NotFound


#These are the local imports
from .models import Role, Gender, Heamophilia
from .serializers import RoleSerializer, GenderSerializer, HeamophiliaSerializer

# Create your views here.

"""
These views  are used to handle the CRUD opertions for the Role, Gender and Heamophilia models.
They user RoleSerializer, GenderSerializer and HeamophiliaSerializer to serialize  and deserialize the data.
The views are accessed using the APIView class and the appropriate HTTP methods (GET, POST, PUT, PATCH, DELETE).
The views are protected by the IsAuthenticated permission class, which ensures that only authenticated users can access the views.
"""
class RoleCRUDView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request, role_id=None):
        if role_id is not None:
            try:
                role = Role.objects.get(role_id=role_id)
                serializer = RoleSerializer(role)
                return Response(serializer.data)
            except Role.DoesNotExist:
                return Response({"message":f"Role with id {role_id} does not exist"}, status=status.HTTP_404_NOT_FOUND)
            
        roles = Role.objects.all()
        serializer = RoleSerializer(roles, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = RoleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, role_id):
        try:
            role = Role.objects.get(role_id=role_id)
        except Role.DoesNotExist:
            return Response({"message":f"Role with id {role_id} does not exist"}, status=status.HTTP_404_NOT_FOUND)

        serializer = RoleSerializer(role, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, role_id):
        try:
            role = Role.objects.get(role_id=role_id)
        except Role.DoesNotExist:
            return Response({"message":f"Role with id {role_id} does not exist"}, status=status.HTTP_404_NOT_FOUND)

        serializer = RoleSerializer(role, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    def delete(self, request, role_id):
        try:
            role = Role.objects.get(role_id=role_id)
        except Role.DoesNotExist:
            return Response({"message":f"Role with id {role_id} does not exist"}, status=status.HTTP_404_NOT_FOUND)

        role.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class GenderCRUDView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request, gender_id=None):
        if gender_id is not None:
            try:
                gender = Gender.objects.get(gender_id=gender_id)
                serializer = GenderSerializer(gender)
                return Response(serializer.data)
            except Gender.DoesNotExist:
                return Response({"message":f"Gender with id {gender_id} does not exist"},status=status.HTTP_404_NOT_FOUND)

        genders = Gender.objects.all()
        serializer = GenderSerializer(genders, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = GenderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, gender_id):
        try:
            gender = Gender.objects.get(gender_id=gender_id)
        except Gender.DoesNotExist:
            return Response({"message":f"Gender with id {gender_id} does not exist"}, status=status.HTTP_404_NOT_FOUND)

        serializer = GenderSerializer(gender, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, gender_id):
        try:
            gender = Gender.objects.get(gender_id=gender_id)
        except Gender.DoesNotExist:
            return Response({"message":f"Gender with id {gender_id} does not exist"}, status=status.HTTP_404_NOT_FOUND)

        serializer = GenderSerializer(gender, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, gender_id):
        try:
            gender = Gender.objects.get(gender_id=gender_id)
        except Gender.DoesNotExist:
            return Response({"message":f"Gender with id {gender_id} does not exist"}, status=status.HTTP_404_NOT_FOUND)

        gender.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class HeamophiliaCRUDView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request, heamophilia_id=None):
        if heamophilia_id is not None:
            try:
                heamophilia = Heamophilia.objects.get(heamophilia_id=heamophilia_id)
                serializer = HeamophiliaSerializer(heamophilia)
                return Response(serializer.data)
            except Heamophilia.DoesNotExist:
                return Response({"message":f"Heamophilia with id {heamophilia_id} does not exist"}, status=status.HTTP_404_NOT_FOUND)

        heamophilias = Heamophilia.objects.all()
        serializer = HeamophiliaSerializer(heamophilias, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = HeamophiliaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, heamophilia_id):
        try:
            heamophilia = Heamophilia.objects.get(heamophilia_id=heamophilia_id)
        except Heamophilia.DoesNotExist:
            return Response({"message":f"Heamophilia with id {heamophilia_id} does not exist"}, status=status.HTTP_404_NOT_FOUND)

        serializer = HeamophiliaSerializer(heamophilia, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, heamophilia_id):
        try:
            heamophilia = Heamophilia.objects.get(heamophilia_id=heamophilia_id)
        except Heamophilia.DoesNotExist:
            return Response({"message":f"Heamophilia with id {heamophilia_id} does not exist"}, status=status.HTTP_404_NOT_FOUND)

        serializer = HeamophiliaSerializer(heamophilia, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, heamophilia_id):
        try:
            heamophilia = Heamophilia.objects.get(heamophilia_id=heamophilia_id)
        except Heamophilia.DoesNotExist:
            return Response({"message":f"Heamophilia with id {heamophilia_id} does not exist"}, status=status.HTTP_404_NOT_FOUND)

        heamophilia.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)