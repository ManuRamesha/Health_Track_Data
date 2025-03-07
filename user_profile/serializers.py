# these are rest_framework imports
from rest_framework import serializers

# these are local imports
from .models import Profile
from tables.models import Heamophilia

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'
        # There's no `required_fields` attribute directly in `Meta`, so we won't use it here.
        extra_kwargs = {
            'ka_regd_no': {'required': True},
            'heamophilia_type': {'required': True},
            'percentage': {'required': True},
            'factor': {'required': True},
            'inhibitor': {'required': True},
            'target_joints': {'required': True},
        }

    def validate_heamophilia_type(self, value):
        if value is not None:
            try:
                heamophilia = Heamophilia.objects.get(name=value)
                return value  # Returning the value itself after successful validation
            except Heamophilia.DoesNotExist:
                raise serializers.ValidationError(
                    f"Invalid heamophilia type. Valid heamophilia types are: {', '.join(Heamophilia.objects.values_list('name', flat=True))}."
                )
        return value

    def validate_percentage(self, value):
        valid_percentages = ['1-10%', '10-20%', '20-30%', '30-40%', '40-50%', '50-60%', '60-70%', '70-80%', '80-90%', '90-100%', 'less than 1%']
        if value is not None and value not in valid_percentages:
            raise serializers.ValidationError(
                "Invalid percentage. Valid percentages are: " + ", ".join(valid_percentages)
            )
        return value

    def validate_factor(self, value):
        valid_factors = ['vii', 'viii', 'ix', 'xi']
        if value not in valid_factors:
            raise serializers.ValidationError(
                "Invalid factor. Valid factors are: " + ", ".join(valid_factors)
            )
        return value

    def validate_inhibitor(self, value):
        valid_inhibitors = ['yes', 'no']
        if value is not None and value not in valid_inhibitors:
            raise serializers.ValidationError(
                "Invalid inhibitor. Valid inhibitors are: " + ", ".join(valid_inhibitors)
            )
        return value

    def validate_inhibitor_percentage(self, value):
        if value is not None and (value < 0 or value > 100):
            raise serializers.ValidationError("Inhibitor percentage must be between 0 and 100.")
        return value

    def validate(self, data):
        if data.get('inhibitor') == 'yes' and data.get('inhibitor_percentage') is None:
            raise serializers.ValidationError("Inhibitor percentage is required when inhibitor is 'yes'.")
        return data

    def create(self, validated_data):
        profile = Profile(
            user=validated_data['user'],
            ka_regd_no=validated_data['ka_regd_no'],
            heamophilia_type=validated_data['heamophilia_type'],
            percentage=validated_data['percentage'],
            factor=validated_data['factor'],
            inhibitor=validated_data['inhibitor'],
            inhibitor_percentage=validated_data['inhibitor_percentage'],
            target_joints=validated_data['target_joints']
        )
        profile.save()
        return profile
