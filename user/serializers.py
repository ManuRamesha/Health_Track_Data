from rest_framework import serializers


from  .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'date_of_birth', 'phone_number', 'first_name', 'last_name',
                  'parent_name', 'parent_phone_number', 'address', 'city', 'state', 'zip_code', 'country', 'role', 'gender')
        extra_kwargs = {'password': {'write_only': True}}
        read_only_fields = ('id',)
        required_fields = ('username', 'email', 'password', 'first_name', 'last_name', 'date_of_birth', 'phone_number',
                           'parent_name', 'parent_phone_number', 'address', 'city', 'state', 'zip_code', 'country', 'gender')

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            date_of_birth=validated_data['date_of_birth'],
            phone_number=validated_data['phone_number'],
            parent_name=validated_data['parent_name'],
            parent_phone_number=validated_data['parent_phone_number'],
            address=validated_data['address'],
            city=validated_data['city'],
            state=validated_data['state'],
            zip_code=validated_data['zip_code'],
            # country=validated_data['country']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
    
    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.username = validated_data.get('username', instance.username)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.date_of_birth = validated_data.get('date_of_birth', instance.date_of_birth)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.parent_name = validated_data.get('parent_name', instance.parent_name)
        instance.parent_phone_number = validated_data.get('parent_phone_number', instance.parent_phone_number)
        instance.address = validated_data.get('address', instance.address)
        instance.city = validated_data.get('city', instance.city)
        instance.state = validated_data.get('state', instance.state)
        instance.zip_code = validated_data.get('zip_code', instance.zip_code)
        # instance.country = validated_data.get('country', instance.country)
        instance.save()
        return instance