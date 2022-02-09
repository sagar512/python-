from rest_framework.response import Response
from rest_framework import serializers
from rest_framework.exceptions import ValidationError, APIException

from growthmodel.models import *
from account.models import *

class GetGrowthModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = GrowthModel
        fields = '__all__'

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
        fields = '__all__'

class AddGrowthModelActivitySerializer(serializers.Serializer):
    pass

class UpdateGrowthModelActivitySerializer(serializers.Serializer):
    start_date = serializers.CharField(error_messages={
        'required': "profession field is required", 'blank': "profession field can't be blank"})
    end_date = serializers.CharField(error_messages={
        'required': "profession is required", 'blank': "profession can't be blank"})
    compilation_method = serializers.CharField(error_messages={
        'required': "compilation method is required", 'blank': "compilation method can't be blank"})
    current_step = serializers.IntegerField(error_messages={
        'required': "step is required", 'blank': "step can't be blank"})

    class Meta:
        model = GrowthModelActivity
        fields = '__all__'

    def validate(self, attrs):
        compilation_method = attrs['compilation_method']
        current_step = attrs['current_step']

        if compilation_method.lower() not in ['manual', 'automatic']:
            raise ValidationError({"message": "Please provide valid compilation method."})

        if current_step not in [0,1,2,3,4]:
            raise ValidationError({"message": "Please provide valid step."})

        return attrs

class DeleteGrowthModelActivitySerializer(serializers.Serializer):

    class Meta:
        model = GrowthModelActivity
        fields = '__all__'