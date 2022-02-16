from rest_framework.response import Response
from rest_framework import serializers
from rest_framework.exceptions import ValidationError, APIException

from growthmodel.models import *
from account.models import *
from django.utils import timezone
from datetime import date

class GetGrowthModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = GrowthModel
        exclude = ('created_at', 'updated_at')

class CreateGrowthModelSerializer(serializers.Serializer):
    job_type = serializers.CharField(error_messages={
    	'required': "job type is required", 'blank': "job type can't be blank"})

    def validate(self, attrs):
        return attrs

class UpdateGrowthModelSerializer(serializers.ModelSerializer):
    profession_field = serializers.CharField(error_messages={
    	'required': "profession field is required", 'blank': "profession field can't be blank"})
    profession = serializers.CharField(error_messages={
    	'required': "profession is required", 'blank': "profession can't be blank"})
    compilation_method = serializers.CharField(error_messages={
    	'required': "compilation method is required", 'blank': "compilation method can't be blank"})

    class Meta:
        model = GrowthModel
        fields = '__all__'
    
    def validate(self, attrs):
        compilation_method = attrs['compilation_method']
        attrs['current_step'] = 2

        if compilation_method.lower() not in ['manual', 'automatic']:
            raise ValidationError({"message": "Please provide valid compilation method."})

        return attrs

class GetProfessionSerializer(serializers.ModelSerializer):

	class Meta:
		model = Profession
		fields = '__all__'

class GetGrowthModelActivitySerializer(serializers.ModelSerializer):

    class Meta:
        model = GrowthModelActivity
        exclude = ('created_at', 'updated_at')

class BulkCreateGrowthModelActivitiesListSerializer(serializers.ListSerializer):

    def create(self, validated_data):
        activities = [GrowthModelActivity(**activity) for activity in validated_data]
        return GrowthModelActivity.objects.bulk_create(activities)

class AddGrowthModelActivitySerializer(serializers.ModelSerializer):

    class Meta:
        model = GrowthModelActivity
        fields = '__all__'
        list_serializer_class = BulkCreateGrowthModelActivitiesListSerializer

class UpdateGrowthModelActivitySerializer(serializers.ModelSerializer):

    def validate(self, attrs):
        start_date = None
        end_date = None

        if 'start_date' in attrs:
            start_date = attrs['start_date']
            if start_date and start_date < date.today():
                raise ValidationError({"message": "Start date should be more than now."})

        if 'end_date' in attrs:
            end_date = attrs['end_date']
            if end_date and end_date < date.today():
                raise ValidationError({"message": "End date should be more than now."})

        if start_date and end_date and (end_date < start_date):
            raise ValidationError({"message": "End date must be after start date."})

        return attrs

    class Meta:
        model = GrowthModelActivity
        fields = '__all__'

class DeleteGrowthModelActivitySerializer(serializers.Serializer):

    class Meta:
        model = GrowthModelActivity
        fields = '__all__'