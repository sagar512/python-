# Generated by Django 4.0.1 on 2022-02-08 05:43

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('title', models.CharField(blank=True, max_length=255, null=True)),
                ('status', models.BooleanField(blank=True, null=True)),
                ('created_at', models.DateTimeField(db_column='createdAt')),
                ('updated_at', models.DateTimeField(blank=True, db_column='updatedAt', null=True)),
                ('deleted_at', models.DateTimeField(blank=True, db_column='deletedAt', null=True)),
                ('master_id', models.UUIDField(blank=True, db_column='masterId', null=True)),
            ],
            options={
                'db_table': 'role',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Tokens',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('user_id', models.CharField(db_column='userId', max_length=255)),
                ('master_id', models.CharField(blank=True, db_column='masterId', max_length=255, null=True)),
                ('token', models.CharField(max_length=255)),
                ('refresh_token', models.CharField(blank=True, db_column='refreshToken', max_length=255, null=True)),
                ('token_expiry_time', models.CharField(blank=True, db_column='tokenExpiryTime', max_length=255, null=True)),
                ('created_at', models.DateTimeField(db_column='createdAt')),
                ('updated_at', models.DateTimeField(db_column='updatedAt')),
            ],
            options={
                'db_table': 'tokens',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('first_name', models.CharField(blank=True, db_column='firstName', max_length=255, null=True)),
                ('last_name', models.CharField(blank=True, db_column='lastName', max_length=255, null=True)),
                ('email', models.CharField(blank=True, max_length=255, null=True)),
                ('alternate_email', models.CharField(blank=True, db_column='alternateEmail', max_length=255, null=True)),
                ('phone', models.CharField(blank=True, max_length=255, null=True)),
                ('country', models.CharField(blank=True, max_length=255, null=True)),
                ('state', models.CharField(blank=True, max_length=255, null=True)),
                ('city', models.CharField(blank=True, max_length=255, null=True)),
                ('profile_pic_url', models.CharField(blank=True, db_column='profilePicURL', max_length=255, null=True)),
                ('short_description', models.TextField(blank=True, db_column='shortDescription', null=True)),
                ('brief_description', models.TextField(blank=True, db_column='briefDescription', null=True)),
                ('education_details', models.JSONField(blank=True, db_column='educationDetails', null=True)),
                ('language_skills', models.JSONField(blank=True, db_column='languageSkills', null=True)),
                ('experience', models.JSONField(blank=True, null=True)),
                ('certificate', models.JSONField(blank=True, null=True)),
                ('status', models.BooleanField()),
                ('is_deleted', models.BooleanField(db_column='isDeleted')),
                ('is_verified', models.BooleanField(db_column='isVerified')),
                ('otp', models.IntegerField(blank=True, null=True)),
                ('otp_expire_on', models.CharField(blank=True, db_column='otpExpireOn', max_length=255, null=True)),
                ('password', models.CharField(blank=True, max_length=255, null=True)),
                ('created_at', models.DateTimeField(db_column='createdAt')),
                ('updated_at', models.DateTimeField(db_column='updatedAt')),
                ('master_id', models.UUIDField(db_column='masterId')),
                ('account_type', models.CharField(db_column='accountType', max_length=10)),
                ('role', models.UUIDField(blank=True, null=True)),
                ('profile_bg_url', models.CharField(blank=True, db_column='profileBgURL', max_length=255, null=True)),
                ('available_for', models.JSONField(blank=True, db_column='availableFor', null=True)),
                ('my_goal', models.JSONField(blank=True, db_column='myGoal', null=True)),
                ('social_media_url', models.JSONField(blank=True, db_column='socialMediaUrl', null=True)),
                ('address', models.TextField(blank=True, null=True)),
                ('date_of_birth', models.DateField(blank=True, db_column='dateOfBirth', null=True)),
                ('alternate_phone', models.JSONField(blank=True, db_column='alternatePhone', null=True)),
                ('is_signup_details_completed', models.BooleanField(db_column='isSignUpDetailsCompleted')),
                ('profile_id', models.CharField(blank=True, db_column='profileId', max_length=64, null=True)),
                ('website_url', models.JSONField(blank=True, db_column='websiteURL', null=True)),
                ('auth_type', models.CharField(db_column='authType', max_length=15)),
                ('is_suspended', models.BooleanField(db_column='isSuspended')),
                ('suspended_at', models.CharField(blank=True, db_column='suspendedAt', max_length=15, null=True)),
                ('password_updated_at', models.CharField(blank=True, db_column='passwordUpdatedAt', max_length=15, null=True)),
                ('stripe_customer_id', models.CharField(blank=True, db_column='stripeCustomerId', max_length=64, null=True)),
            ],
            options={
                'db_table': 'users',
                'managed': False,
            },
        ),
    ]
