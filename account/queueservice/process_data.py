import json
import re
from account.models import Users, Role, Tokens


class ProcessGrowthdboData:

	def __init__(self, action, payload):
		self.action = action
		self.payload = payload
		self.payload_data = payload.get('data')
		self.master_id = None
		if self.action.lower() in ['update', 'delete']:
			self.master_id = payload.get('query').get('where').get('masterId')

	def get_django_db_column_name(self, column, keep_contiguous=True):
		string_length = len(column)
		is_lower_around = (lambda: column[i-1].islower() or 
			string_length > (i + 1) and column[i + 1].islower())

		start = 0
		parts = []
		for i in range(1, string_length):
			if column[i].isupper() and (not keep_contiguous or is_lower_around()):
				parts.append(column[start: i].lower())
				start = i
		parts.append(column[start:].lower())

		return "_".join(parts)

	def get_processed_payload_data(self, payload_data):
		updated_user_dict = {}
		payload_data.pop('id', '')
		payload_data.pop('accessToken', '')
		for key, value in payload_data.items():
			column_name = self.get_django_db_column_name(key)
			updated_user_dict.update({ column_name: value })
		return updated_user_dict

	def create_user(self, payload_data):
		processed_data = self.get_processed_payload_data(payload_data)
		Users.objects.create(**processed_data)
		return True

	def update_user(self, master_id, payload_data):
		processed_data = self.get_processed_payload_data(payload_data)
		Users.objects.filter(master_id=master_id).update(
			**processed_data)
		return True

	def delete_user(self, master_id):
		Users.objects.filter(master_id=master_id).delete()
		return True

	def create_role(self, payload_data):
		processed_data = self.get_processed_payload_data(payload_data)
		Role.objects.create(**processed_data)
		return True

	def update_role(self, master_id, payload_data):
		processed_data = self.get_processed_payload_data(payload_data)
		Role.objects.filter(master_id=master_id).update(
			**processed_data)
		return True

	def delete_role(self, master_id):
		Role.objects.filter(master_id=master_id).delete()
		return True

	def create_token(self, payload_data):
		processed_data = self.get_processed_payload_data(payload_data)
		Tokens.objects.create(**processed_data)
		return True

	def update_token(self, master_id, payload_data):
		processed_data = self.get_processed_payload_data(payload_data)
		Tokens.objects.filter(master_id=master_id).update(
			**processed_data)
		return True

	def delete_token(self, master_id):
		Tokens.objects.filter(master_id=master_id).delete()
		return True

	def process_growth_model_dbo(self):
		if self.action.lower() == 'create' and \
			self.payload.get('model', '').lower() == 'user':
			self.create_user(self.payload_data)
		elif self.action.lower() == 'update' and \
			self.payload.get('model', '').lower() == 'user':
			self.update_user(self.master_id, self.payload_data)
		elif self.action.lower() == 'destroy' and \
			self.payload.get('model', '').lower() == 'user':
			self.delete_user(self.master_id)
		elif self.action.lower() == 'create' and \
			self.payload.get('model', '').lower() == 'role':
			self.create_role(self.payload_data)
		elif self.action.lower() == 'update' and \
			self.payload.get('model', '').lower() == 'role':
			self.update_role(self.master_id, self.payload_data)
		elif self.action.lower() == 'destroy' and \
			self.payload.get('model', '').lower() == 'role':
			self.delete_role(self.master_id)
		elif self.action.lower() == 'create' and \
			self.payload.get('model', '').lower() == 'token':
			self.create_token(self.payload_data)
		elif self.action.lower() == 'update' and \
			self.payload.get('model', '').lower() == 'token':
			self.update_token(self.master_id, self.payload_data)
		elif self.action.lower() == 'destroy' and \
			self.payload.get('model', '').lower() == 'token':
			self.delete_token(self.master_id)
		else:
			return True