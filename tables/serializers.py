# these are rest_framework imports
from rest_framework import serializers

# these are the local imports
from .models import Role, Gender, Heamophilia

"""
These serializers are used to serialize the data from Role, Gender and Heamophilia models.
They define the fields that should be included in the serializer data.
The Meta class specifies the model and the fields to be included in the serialized data.
The serializers are used in the views to convert the model instances to JSON data and vice versa.
"""

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