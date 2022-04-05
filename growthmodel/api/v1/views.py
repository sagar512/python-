from rest_framework.exceptions import APIException
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView

from account.models import Users
from account.authentication import UserTokenAuthentication, AdminUserTokenAuthentication
from growthmodel.models import *
from growthmodel.api.v1.serializers import *
from growthmodel.api.v1.paginations import BasicPagination, PaginationHandlerMixin
from rest_framework import status
from django.shortcuts import get_object_or_404, render
from django.db.models import Q, Count, F, Sum, Avg

from xhtml2pdf import pisa
from io import BytesIO
from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse
from growthmodel.queueservice.process_producer_data import (
	produce_growth_model_data
)

class CreateGrowthModelView(APIView):
    authentication_classes = [UserTokenAuthentication,]
    permission_classes = (IsAuthenticated,)

    def post(self, request):
    	serializer = CreateGrowthModelSerializer(data=request.data)
    	if serializer.is_valid():
    		data = serializer.validated_data
    		try:
    			growth_model_obj, created = GrowthModel.objects.get_or_create(
    				user_id=request.user.id)
    			growth_model_obj.job_type = data['job_type']
    			growth_model_obj.current_step = 1
    			growth_model_obj.save()
    			data.update({'id': str(growth_model_obj.id)})

    			if created:
	    			# Producing GrowthModel data to Kafka Server
	    			growth_model_data = data
	    			growth_model_data.update({'user_id': str(growth_model_obj.user_id)})
	    			produce_growth_model_data('userdbo', b'create',
	    				growth_model_data, 'GrowthModel', str(growth_model_obj.id))
    		except:
    			return Response({
    					"message": "Oops, something went wrong. Please try again."
    				}, status=status.HTTP_400_BAD_REQUEST)

    		return Response({
	    			"message": "GrowthModel created successfully.",
	    			"data": data
    			}, status=status.HTTP_200_OK)
    	else:
    		return Response({
	    			"status": "error",
	    			"data": serializer.errors
	    		}, status=status.HTTP_400_BAD_REQUEST)

class GetGrowthModelView(APIView):
	authentication_classes = [UserTokenAuthentication,]
	permission_classes = (IsAuthenticated,)

	def get(self, request):
		try:
			growthmodel_obj = GrowthModel.objects.get(
				user_id=request.user.id)
		except:
			return Response({
					"message": "No growth model found."
				}, status=status.HTTP_404_NOT_FOUND)

		data = GetGrowthModelSerializer(growthmodel_obj).data
		growthModelActivities = GrowthModelActivity.objects.filter(
			growth_model_id=growthmodel_obj.id)
		data['activities'] = list(GetGrowthModelActivitySerializer(
			growthModelActivities, many=True).data)

		return Response({
				"data": data
			}, status=status.HTTP_200_OK)

class UpdateGrowthModelView(APIView):
    authentication_classes = [UserTokenAuthentication,]
    permission_classes = (IsAuthenticated,)

    def patch(self, request, id=None):
    	try:
    		growthmodel_obj = GrowthModel.objects.get(id=id,
    			user_id=request.user.id)
    	except:
    		return Response({
				"message": "No growth model found."
			}, status=status.HTTP_404_NOT_FOUND)

    	serializer = UpdateGrowthModelSerializer(
    		growthmodel_obj, data=request.data, partial=True)
    	if serializer.is_valid():
    		serializer.save()

    		# Producing GrowthModel data to Kafka Server
    		growth_model_data = serializer.data
    		produce_growth_model_data('userdbo', b'update',
    			growth_model_data, 'GrowthModel', str(growthmodel_obj.id))

    		return Response({
    			"message": "GrowthModel updated successfully.",
    			"data": serializer.data
			}, status=status.HTTP_200_OK)
    	else:
    		return Response({
    			"status": "error",
    			"data": serializer.errors
    		}, status=status.HTTP_400_BAD_REQUEST)

class AddGrowthModelActivityView(ListCreateAPIView):
	authentication_classes = [UserTokenAuthentication,]
	permission_classes = (IsAuthenticated,)
	serializer_class = AddGrowthModelActivitySerializer
	queryset = GrowthModelActivity.objects.all()

	def create(self, request, *args, **kwargs):
		activities = request.data.get('activities')
		growthmodel_obj, created = GrowthModel.objects.get_or_create(
			user_id=request.user.id)

		current_step = growthmodel_obj.current_step
		if created:
			current_step = 0
			# Producing GrowthModel data to Kafka Server
			growth_model_data = {
				'id': str(growthmodel_obj.id),
				'user_id': str(growthmodel_obj.user_id),
				'current_step': current_step
			}
			produce_growth_model_data('userdbo', b'create',
				growth_model_data, 'GrowthModel', str(growthmodel_obj.id))
		elif growthmodel_obj.job_type and growthmodel_obj.profession_field \
			and growthmodel_obj.profession and growthmodel_obj.compilation_method:
			current_step = 4

		activity_data = []
		for activity in activities:
			skillArea = activity['skillArea']
			for skill in activity['skillTypes']:
				skillType = skill['typeName']
				for dt in skill['data']:
					activity_data_dict = {
						'growth_model_id': growthmodel_obj.id,
						'skill_area' : skillArea,
						'activity_type' : skillType,
						'activity_title' : dt['activityTitle'],
						'activity_status': 'inProgress'
					}
					if 'activityId' in dt:
						activity_data_dict.update({
							'activity_id' : dt['activityId']
						})
					if 'activityLink' in dt:
						activity_data_dict.update({
							'activity_link' : dt['activityLink']
						})
					if 'activityCategory' in dt:
						activity_data_dict.update({
							'activity_category' : dt['activityCategory']
						})

					activity_data.append(activity_data_dict)

		serializer = self.get_serializer(data=activity_data, many=True)
		serializer.is_valid(raise_exception=True)
		self.perform_create(serializer)
		headers = self.get_success_headers(serializer.data)

		growth_model_activity_data = serializer.data
		for growth_model_activity in growth_model_activity_data:
			# Producing GrowthModelActivity data to Kafka Server
			produce_growth_model_data('userdbo', b'create',
				growth_model_activity, 'GrowthModelActivity',
				str(growth_model_activity.get('id'))
			)

		# After successful activities creation, updating current_step
		growthmodel_obj.current_step = current_step
		growthmodel_obj.save()

		# Producing GrowthModel data to Kafka Server
		produce_growth_model_data('userdbo', b'update',
			{'current_step': current_step}, 'GrowthModel', str(growthmodel_obj.id))

		return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class GetGrowthModelActivityView(APIView, PaginationHandlerMixin):
	authentication_classes = [UserTokenAuthentication,]
	permission_classes = (IsAuthenticated,)
	serializer_class = GetGrowthModelActivitySerializer
	pagination_class = BasicPagination

	def get(self, request):
		growthmodel_id = request.GET.get('growthmodel_id')
		try:
			growthmodel_obj = GrowthModel.objects.get(user_id=request.user.id,
				id=growthmodel_id)
		except:
			return Response({
				"message": "No growth model found."
			}, status=status.HTTP_404_NOT_FOUND)

		skill_area = request.GET.get('skill_area', '')
		activity_type = request.GET.get('activity_type', '')
		activity_status = request.GET.get('activity_status', '')
		keyword = request.GET.get('keyword', '')

		q_filter = Q(growth_model_id=growthmodel_id)
		if skill_area:
			q_filter &= Q(skill_area__iexact=skill_area)
		if activity_type:
			q_filter &= Q(activity_type__iexact=activity_type)
		if activity_status:
			q_filter &= Q(activity_status__iexact=activity_status)
		if keyword:
			q_filter &= Q(
				Q(skill_area__icontains=keyword) |
				Q(activity_type__icontains=keyword) |
				Q(activity_status__icontains=keyword) |
				Q(activity_title__icontains=keyword)
			)

		growthmodel_activities = GrowthModelActivity.objects.filter(
			q_filter).order_by('id')

		page = self.paginate_queryset(growthmodel_activities)
		if page is not None:
			serializer = self.get_paginated_response(
				self.serializer_class(page, many=True).data)
		else:
			serializer = self.serializer_class(growthmodel_activities, many=True)

		return Response({
			"data": serializer.data
		}, status=status.HTTP_200_OK)

class UpdateGrowthModelActivityView(APIView):
    authentication_classes = [UserTokenAuthentication,]
    permission_classes = (IsAuthenticated,)

    def patch(self, request, id=None):
    	try:
    		growthmodelactivity_obj = GrowthModelActivity.objects.get(id=id)
    	except:
    		return Response({
				"message": "No growth model activity found."
			}, status=status.HTTP_404_NOT_FOUND)

    	serializer = UpdateGrowthModelActivitySerializer(growthmodelactivity_obj,
    		data=request.data, partial=True)
    	if serializer.is_valid():
    		serializer.save()

    		# Producing GrowthModel data to Kafka Server
    		growth_model_activity_data = serializer.data
    		produce_growth_model_data('userdbo', b'update', growth_model_activity_data,
    			'GrowthModelActivity', str(growthmodelactivity_obj.id))

    		return Response({
	    			"message": "Growth Model Activity updated successfully.",
	    			"data": serializer.data
    			}, status=status.HTTP_200_OK)
    	else:
    		return Response({
	    			"status": "error",
	    			"data": serializer.errors
	    		}, status=status.HTTP_400_BAD_REQUEST)

class DeleteGrowthModelActivityView(APIView):
	authentication_classes = [UserTokenAuthentication,]
	permission_classes = (IsAuthenticated,)

	def delete(self, request, id=None):
		item = get_object_or_404(GrowthModelActivity, id=id)
		item.delete()

		# Producing GrowthModel data to Kafka Server
		produce_growth_model_data('userdbo', b'delete', '',
			'GrowthModelActivity', str(id))

		return Response({
			"status": "success",
			"message": "Growth Model Activity Deleted"
		})

class GetGrowthModelActivityStatsView(APIView):
	authentication_classes = [UserTokenAuthentication,]
	permission_classes = (IsAuthenticated,)

	def get(self, request):
		growthmodel_id = request.GET.get('growthmodel_id')
		try:
			growthmodel_obj = GrowthModel.objects.get(user_id=request.user.id,
				id=growthmodel_id)
		except:
			return Response({
				"message": "No growth model found."
			}, status=status.HTTP_404_NOT_FOUND)

		growthModelActObjs = GrowthModelActivity.objects.filter(growth_model_id=growthmodel_id)
		skill_total_dict = dict(growthModelActObjs.values('skill_area').annotate(
			skill_total=Count('skill_area')).values_list('skill_area', 'skill_total'))
		status_total_dict = growthModelActObjs.values('skill_area', 'activity_status').annotate(
			total=Count('skill_area'))

		data = {}
		for skill in status_total_dict:
			if skill['skill_area'] not in data.keys():
				data[skill['skill_area']] = {
					skill['activity_status']: \
						round(float(skill['total'] / skill_total_dict.get(skill['skill_area']) * 100), 2)
				}
			elif skill['activity_status'] not in data[skill['skill_area']].keys():
				data[skill['skill_area']][skill['activity_status']] = \
					round(float(skill['total'] / skill_total_dict.get(skill['skill_area']) * 100), 2)

		return Response({
				"data": data
			}, status=status.HTTP_200_OK)


class GetGrowthModelActivityPdfView(APIView):
	# authentication_classes = [UserTokenAuthentication,]
	permission_classes = (AllowAny,)

	def get(self, request):
		growthmodel_id = request.GET.get('growthmodel_id')
		try:
			growthmodel_obj = GrowthModel.objects.get(
				id=growthmodel_id)
		except:
			return Response({
				"message": "No growth model found."
			}, status=status.HTTP_404_NOT_FOUND)

		activity_list = list(GrowthModelActivity.objects.filter(growth_model_id=growthmodel_id).values(
			'skill_area', 'activity_type', 'activity_title', 'start_date', 'end_date', 'activity_status'))

		if len(activity_list) > 0:
			template = get_template("growthmodel/growth_model_activity.html")
			template_html = template.render({
				'activity_list': activity_list
			})

			result = BytesIO()
			pdf = pisa.pisaDocument(BytesIO(template_html.encode("ISO-8859-1")), result)
			if not pdf.err:
				response = HttpResponse(result.getvalue(), content_type='application/pdf')
				response['Content-Disposition'] = 'attachment; filename="growth_model_activity.pdf"'
				return response
			else:
				return HttpResponse('Something went wrong. Please try again.')
		else:
			return Response({
				"message": "No growth model activities found."
			}, status=status.HTTP_404_NOT_FOUND)


class GetUserGrowthModelActivityForAdminView(APIView, PaginationHandlerMixin):
	# authentication_classes = [AdminUserTokenAuthentication,]
	permission_classes = (AllowAny,)
	serializer_class = GetGrowthModelActivitySerializer
	pagination_class = BasicPagination

	def get(self, request):
		user_id = request.GET.get('user_id')
		try:
			growthmodel_obj = GrowthModel.objects.get(user_id=user_id)
		except:
			return Response({
				"message": "No growth model found."
			}, status=status.HTTP_404_NOT_FOUND)

		growthmodel_activities = GrowthModelActivity.objects.filter(
			growth_model_id=growthmodel_obj.id).order_by('id')

		page = self.paginate_queryset(growthmodel_activities)
		if page is not None:
			serializer = self.get_paginated_response(
				self.serializer_class(page, many=True).data)
		else:
			serializer = self.serializer_class(growthmodel_activities, many=True)

		return Response({
			"data": serializer.data
		}, status=status.HTTP_200_OK)


class GetUserGrowthModelActivityStatsForAdminView(APIView):
	# authentication_classes = [AdminUserTokenAuthentication,]
	permission_classes = (AllowAny,)

	def get(self, request):
		user_id = request.GET.get('user_id')
		try:
			growthmodel_obj = GrowthModel.objects.get(user_id=user_id)
		except:
			return Response({
				"message": "No growth model found."
			}, status=status.HTTP_404_NOT_FOUND)

		growthModelActObjs = GrowthModelActivity.objects.filter(
			growth_model_id=growthmodel_obj.id)
		skill_total_dict = dict(growthModelActObjs.values('skill_area').annotate(
			skill_total=Count('skill_area')).values_list('skill_area', 'skill_total'))
		status_total_dict = growthModelActObjs.values('skill_area', 'activity_status').annotate(
			total=Count('skill_area'))

		data = {}
		for skill in status_total_dict:
			if skill['skill_area'] not in data.keys():
				data[skill['skill_area']] = {
					skill['activity_status']: \
						round(float(skill['total'] / skill_total_dict.get(skill['skill_area']) * 100), 2)
				}
			elif skill['activity_status'] not in data[skill['skill_area']].keys():
				data[skill['skill_area']][skill['activity_status']] = \
					round(float(skill['total'] / skill_total_dict.get(skill['skill_area']) * 100), 2)

		return Response({
			"data": data
		}, status=status.HTTP_200_OK)
