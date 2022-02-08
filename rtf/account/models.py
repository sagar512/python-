from django.db import models
import uuid

class Role(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    status = models.BooleanField(blank=True, null=True)
    created_at = models.DateTimeField(db_column='createdAt')  # Field name made lowercase.
    updated_at = models.DateTimeField(db_column='updatedAt', blank=True, null=True)  # Field name made lowercase.
    deleted_at = models.DateTimeField(db_column='deletedAt', blank=True, null=True)  # Field name made lowercase.
    master_id = models.UUIDField(db_column='masterId', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'role'


class Tokens(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    user_id = models.CharField(db_column='userId', max_length=255)  # Field name made lowercase.
    master_id = models.CharField(db_column='masterId', max_length=255, blank=True, null=True)  # Field name made lowercase.
    token = models.CharField(max_length=255)
    refresh_token = models.CharField(db_column='refreshToken', max_length=255, blank=True, null=True)  # Field name made lowercase.
    token_expiry_time = models.CharField(db_column='tokenExpiryTime', max_length=255, blank=True, null=True)  # Field name made lowercase.
    created_at = models.DateTimeField(db_column='createdAt')  # Field name made lowercase.
    updated_at = models.DateTimeField(db_column='updatedAt')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tokens'


class Users(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    first_name = models.CharField(db_column='firstName', max_length=255, blank=True, null=True)  # Field name made lowercase.
    last_name = models.CharField(db_column='lastName', max_length=255, blank=True, null=True)  # Field name made lowercase.
    email = models.CharField(max_length=255, blank=True, null=True)
    alternate_email = models.CharField(db_column='alternateEmail', max_length=255, blank=True, null=True)  # Field name made lowercase.
    phone = models.CharField(max_length=255, blank=True, null=True)
    country = models.CharField(max_length=255, blank=True, null=True)
    state = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    profile_pic_url = models.CharField(db_column='profilePicURL', max_length=255, blank=True, null=True)  # Field name made lowercase.
    short_description = models.TextField(db_column='shortDescription', blank=True, null=True)  # Field name made lowercase.
    brief_description = models.TextField(db_column='briefDescription', blank=True, null=True)  # Field name made lowercase.
    education_details = models.JSONField(db_column='educationDetails', blank=True, null=True)  # Field name made lowercase.
    language_skills = models.JSONField(db_column='languageSkills', blank=True, null=True)  # Field name made lowercase.
    experience = models.JSONField(blank=True, null=True)
    certificate = models.JSONField(blank=True, null=True)
    status = models.BooleanField()
    is_deleted = models.BooleanField(db_column='isDeleted')  # Field name made lowercase.
    is_verified = models.BooleanField(db_column='isVerified')  # Field name made lowercase.
    otp = models.IntegerField(blank=True, null=True)
    otp_expire_on = models.CharField(db_column='otpExpireOn', max_length=255, blank=True, null=True)  # Field name made lowercase.
    password = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(db_column='createdAt')  # Field name made lowercase.
    updated_at = models.DateTimeField(db_column='updatedAt')  # Field name made lowercase.
    master_id = models.UUIDField(db_column='masterId')  # Field name made lowercase.
    account_type = models.CharField(db_column='accountType', max_length=10)  # Field name made lowercase.
    role = models.UUIDField(blank=True, null=True)
    profile_bg_url = models.CharField(db_column='profileBgURL', max_length=255, blank=True, null=True)  # Field name made lowercase.
    available_for = models.JSONField(db_column='availableFor', blank=True, null=True)  # Field name made lowercase.
    my_goal = models.JSONField(db_column='myGoal', blank=True, null=True)  # Field name made lowercase.
    social_media_url = models.JSONField(db_column='socialMediaUrl', blank=True, null=True)  # Field name made lowercase.
    address = models.TextField(blank=True, null=True)
    date_of_birth = models.DateField(db_column='dateOfBirth', blank=True, null=True)  # Field name made lowercase.
    alternate_phone = models.JSONField(db_column='alternatePhone', blank=True, null=True)  # Field name made lowercase.
    is_signup_details_completed = models.BooleanField(db_column='isSignUpDetailsCompleted')  # Field name made lowercase.
    profile_id = models.CharField(db_column='profileId', max_length=64, blank=True, null=True)  # Field name made lowercase.
    website_url = models.JSONField(db_column='websiteURL', blank=True, null=True)  # Field name made lowercase.
    auth_type = models.CharField(db_column='authType', max_length=15)  # Field name made lowercase.
    is_suspended = models.BooleanField(db_column='isSuspended')  # Field name made lowercase.
    suspended_at = models.CharField(db_column='suspendedAt', max_length=15, blank=True, null=True)  # Field name made lowercase.
    password_updated_at = models.CharField(db_column='passwordUpdatedAt', max_length=15, blank=True, null=True)  # Field name made lowercase.
    stripe_customer_id = models.CharField(db_column='stripeCustomerId', max_length=64, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'users'

    def is_authenticated(self):
    	return True