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