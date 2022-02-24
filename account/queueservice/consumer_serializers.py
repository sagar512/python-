import re
import configparser
import traceback

from rest_framework.serializers import ModelSerializer, ValidationError
from rest_framework import status

from account.models import Users

config = configparser.ConfigParser()
config.read('config.ini')


# User DBO Serializer
class KafkaUserSerializer(ModelSerializer):
	MESSAGE_TYPE = 'growthdbo'
	VERSION = config['KAFKA']['VERSION']
	KEY_FIELD = 'id'

	class Meta:
		model = Users
		fields = ['id', 'first_name', 'last_name']

	@classmethod
	def lookup_instance(cls, id, **kwargs):
		try:
			return Users.objects.get(id=id)
		except models.Users.DoesNotExist:
			pass

   	# @classmethod
	# def lookup_instance(cls, id, **validated_data):
	# 	try:
	# 		response = {}
			
	# 		# Get data from validated_data
	# 		email = validated_data.get('email')
	# 		mobile = validated_data.get('mobile')
	# 		username = validated_data.get('username')
	# 		first_name = validated_data.get('first_name')
	# 		last_name = validated_data.get('last_name')
	# 		country_code = validated_data.get('country_code')
	# 		device_type = validated_data.get('device_type')
	# 		device_token = validated_data.get('device_token')
	# 		auth_provider = validated_data.get('auth_provider')
	# 		artist_status = validated_data.get('artist_status')

	# 		if len(first_name) == 0:
	# 			response['status'] = status.HTTP_400_BAD_REQUEST
	# 			response['message'] = "First name cannot be blank."
	# 			raise ValidationError(response)
			
	# 		if len(last_name) == 0:
	# 			response['status'] = status.HTTP_400_BAD_REQUEST
	# 			response['message'] = "Last name cannot be blank."
	# 			raise ValidationError(response)

	# 		user = Users.objects.filter(id=id).first()
	# 		if user:
	# 			return None

	# 		if Users.objects.filter(username = username).first():
	# 			return None

	# 		user = Users.objects.create(
	# 			id = id,
	# 			username = username,
	# 			email = email,
	# 			mobile = mobile,
	# 			first_name = first_name,
	# 			last_name = last_name,
	# 			device_type = device_type, 
	# 			device_token = device_token,
	# 			artist_status=artist_status
	# 		)
	# 		user.save()

	# 		return user
		
	# 	except Exception as e:
	# 		response['status'] = status.HTTP_400_BAD_REQUEST
	# 		response['message'] = "Error while creating user."
	# 		raise ValidationError(response)