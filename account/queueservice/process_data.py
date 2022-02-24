import json
from account.models import Users, Role

class ProcessGrowthdboData:

	def __init__(self, action, payload):
		self.action = action
		self.payload_data = payload.get('data')
		self.master_id = payload.get(
			'query').get('where').get('masterId')

	def create_user(self, payload_data):
		Users.objects.create(**payload_data)
		return True

	def update_user(self, master_id, payload_data):
		Users.objects.filter(master_id=master_id).create(
			**payload_data)
		return True

	def delete_user(self, master_id):
		Users.objects.filter(master_id=master_id).delete()
		return True

	def create_role(self, payload_data):
		Role.objects.create(**payload_data)
		return True

	def update_role(self, master_id, payload_data):
		Role.objects.filter(master_id=master_id).create(
			**payload_data)
		return True

	def delete_role(self, master_id):
		Role.objects.filter(master_id=master_id).delete()
		return True

	def process_growth_model_dbo(self):
		if self.action.lower() = 'create' and \
			payload.get('model', '').lower() == 'user':
			self.create_user(self.payload_data)
		elif self.action.lower() = 'update' and \
			payload.get('model', '').lower() == 'user':
			self.update_user(self.master_id, self.payload_data)
		elif self.action.lower() = 'destroy' and \
			payload.get('model', '').lower() == 'user':
			self.delete_user(self.master_id)
		elif self.action.lower() = 'create' and \
			payload.get('model', '').lower() == 'role':
			self.create_role(self.payload_data)
		elif self.action.lower() = 'update' and \
			payload.get('model', '').lower() == 'role':
			self.update_role(self.master_id, self.payload_data)
		elif self.action.lower() = 'destroy' and \
			payload.get('model', '').lower() == 'role':
			self.delete_role(self.master_id)
		else:
			return True