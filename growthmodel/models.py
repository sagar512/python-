from django.db import models
import uuid

# Create your models here.

JOB_TYPE = (
	('employee', 'Employee'),
	('professional', 'Professional')
)

COMPILATION_METHOD = (
	('manual', 'Manual'),
	('automatic', 'Automatic')
)

ACTIVITY_STATUS = (
	('pending', 'Pending'),
	('inProgress', 'In Progress'),
	('lost', 'Lost'),
	('completed', 'Completed')
)

ACTIVITY_CATEGORY = (
	('course', 'Course'),
	('post', 'Post'),
	('blog', 'Blog'),
	('room', 'Room')
)

class GrowthModel(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
	user_id = models.UUIDField(db_column='userId')
	job_type = models.CharField(db_column='jobType', max_length=30, choices=JOB_TYPE,
		null=True, blank=True)
	profession_field = models.CharField(db_column='professionField', max_length=255,
		null=True, blank=True)
	profession = models.CharField(max_length=255, null=True, blank=True)
	compilation_method = models.CharField(db_column='compilationMethod', max_length=255,
		choices=COMPILATION_METHOD, null=True, blank=True)
	current_step = models.IntegerField(db_column='currentStep', default=0)
	created_at = models.DateTimeField(db_column='createdAt', auto_now_add=True)
	updated_at = models.DateTimeField(db_column='updatedAt', auto_now=True)

	def __str__(self):
		return str(self.id)

class GrowthModelActivity(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
	growth_model_id = models.UUIDField(db_column='growthModelId')
	skill_area = models.CharField(db_column='skillArea', max_length=255)
	activity_category = models.CharField(db_column='activityCategory',
		default='course', max_length=255, choices=ACTIVITY_CATEGORY)
	activity_type = models.CharField(db_column='activityType', max_length=255)
	activity_id = models.UUIDField(db_column='activityId', null=True, blank=True)
	activity_link = models.TextField(db_column='activityLink', null=True, blank=True)
	activity_title = models.CharField(db_column='activityTitle', max_length=255)
	start_date = models.DateField(db_column='startDate', blank=True, null=True)
	end_date = models.DateField(db_column='endDate', blank=True, null=True)
	alert = models.BooleanField(default=True)
	activity_status = models.CharField(db_column='activityStatus', max_length=30, choices=ACTIVITY_STATUS)
	created_at = models.DateTimeField(db_column='createdAt', auto_now_add=True)
	updated_at = models.DateTimeField(db_column='updatedAt', auto_now=True)

	def __str__(self):
		return "{0} - {1}".format(self.growth_model_id, self.skill_area)