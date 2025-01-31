
# these are rest_framework imports
from rest_framework import serializers

# these are the local imports
from .models import Role, Gender, Heamophilia

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'

class GenderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gender
        fields = '__all__'

class HeamophiliaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Heamophilia
        fields = '__all__'