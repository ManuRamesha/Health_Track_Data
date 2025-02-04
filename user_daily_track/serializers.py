from rest_framework import serializers
from .models import DailyTrack

class DailyTrackSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyTrack
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')

    def validate(self, data):
        # Check if a DailyTrack entry already exists for the given user and date
        user = data.get('user')
        date = data.get('date')

        if DailyTrack.objects.filter(user=user, date=date).exists():
            raise serializers.ValidationError("A record already exists for this user on the given date.")

        # Custom validation for 'Yes' or 'No' choices
        if data['break_through_bleed'] not in ['Yes', 'No']:
            raise serializers.ValidationError("Valid choice. Must be 'Yes' or 'No'.")
        if data['inj_hemilibra'] not in ['Yes', 'No']:
            raise serializers.ValidationError("Valid choice. Must be 'Yes' or 'No'.")
        if data['physiotherapy'] not in ['Yes', 'No']:
            raise serializers.ValidationError("Valid choice. Must be 'Yes' or 'No'.")

        # Custom validation for 'break_through_bleed_details' and 'treatment_for_bleed' when 'break_through_bleed' is 'Yes'
        if data['break_through_bleed'] == 'Yes' and (data.get('break_through_bleed_details') is None or data.get('treatment_for_bleed') is None):
            raise serializers.ValidationError("Both break_through_bleed_details and treatment_for_bleed are required when break_through_bleed is 'Yes'.")
        
        if data['break_through_bleed'] == 'No' and (data.get('break_through_bleed_details') not in [None, "None"] or data.get('treatment_for_bleed') not in [None, "None"]):
            raise serializers.ValidationError("break_through_bleed_details and treatment_for_bleed should be None when break_through_bleed is 'No'.")
        
        return data

    def create(self, validated_data):
        return DailyTrack.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.break_through_bleed = validated_data.get('break_through_bleed', instance.break_through_bleed)
        instance.break_through_bleed_details = validated_data.get('break_through_bleed_details', instance.break_through_bleed_details)
        instance.treatment_for_bleed = validated_data.get('treatment_for_bleed', instance.treatment_for_bleed)
        instance.inj_hemilibra = validated_data.get('inj_hemilibra', instance.inj_hemilibra)
        instance.physiotherapy = validated_data.get('physiotherapy', instance.physiotherapy)
        instance.save()
        return instance
