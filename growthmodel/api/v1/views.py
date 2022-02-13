from rest_framework.exceptions import APIException
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView

from account.authentication import UserTokenAuthentication
from growthmodel.models import *
from growthmodel.api.v1.serializers import *
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.db.models import Q, Count, F, Sum, Avg


class CreateGrowthModelView(APIView):
    authentication_classes = [UserTokenAuthentication,]
    permission_classes = (IsAuthenticated,)

    def post(self, request):
    	serializer = CreateGrowthModelSerializer(data=request.data)
    	if serializer.is_valid():
    		data = serializer.validated_data
    		job_type = data['job_type']
    		try:
    			growth_model_obj, created = GrowthModel.objects.get_or_create(
    				user_id=request.user.id)
    			growth_model_obj.job_type = job_type
    			growth_model_obj.current_step = 1
    			growth_model_obj.save()
    		except:
    			return Response({
    					"message": "Oops, something went wrong. Please try again."
    				}, status=status.HTTP_400_BAD_REQUEST)

    		return Response({
	    			"message": "GrowthModel created successfully.",
	    			"data": serializer.data
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
    		return Response({
	    			"message": "GrowthModel updated successfully.",
	    			"data": serializer.data
    			}, status=status.HTTP_204_NO_CONTENT)
    	else:
    		return Response({
	    			"status": "error",
	    			"data": serializer.errors
	    		}, status=status.HTTP_400_BAD_REQUEST)

class GetProfessionView(APIView):
	authentication_classes = [UserTokenAuthentication,]
	permission_classes = (IsAuthenticated,)

	def get(self, request):
		data = GetProfessionSerializer(
			Profession.objects.all()).data
		return Response({
				"data": data
			}, status=status.HTTP_200_OK)

class AddGrowthModelActivityView(ListCreateAPIView):
	authentication_classes = [UserTokenAuthentication,]
	permission_classes = (IsAuthenticated,)
	serializer_class = AddGrowthModelActivitySerializer
	queryset = GrowthModelActivity.objects.all()

	def create(self, request, *args, **kwargs):
		growthmodel_id = request.data.get('growthmodel_id')
		activities = request.data.get('activities')

		try:
			growthmodel_obj = GrowthModel.objects.get(id=growthmodel_id,
				user_id=request.user.id)
		except:
			return Response({
				"message": "No growth model found."
			}, status=status.HTTP_404_NOT_FOUND)

		activity_data = []
		for activity in activities:
			skillArea = activity['skillArea']
			for skill in activity['skillTypes']:
				skillType = skill['typeName']
				for dt in skill['data']:
					activity_data.append({
						'growthmodel_id': growthmodel_id,
						'skill_area' : skillArea,
						'activity_type' : skillType,
						'activity_id' : dt['activityId'],
						'activity_title' : dt['activityTitle'],
						'activity_status': 'inProgress'
					})

		serializer = self.get_serializer(data=activity_data, many=True)
		serializer.is_valid(raise_exception=True)
		self.perform_create(serializer)
		headers = self.get_success_headers(serializer.data)
		return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class GetGrowthModelActivityView(APIView):
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

		skill_area = request.GET.get('skill_area', '')
		activity_type = request.GET.get('activity_type', '')
		activity_status = request.GET.get('activity_status', '')

		q_filter = Q(growthmodel_id=growthmodel_id)
		if skill_area:
			q_filter &= Q(skill_area__iexact=skill_area)
		if activity_type:
			q_filter &= Q(activity_type__iexact=activity_type)
		if activity_status:
			q_filter &= Q(activity_status__iexact=activity_status)

		growthmodel_activities = GrowthModelActivity.objects.filter(
			q_filter)

		data = []
		if growthmodel_activities.count() > 0:
			data = GetGrowthModelActivitySerializer(growthmodel_activities, many=True).data

		return Response({
				"data": data
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
    		return Response({
	    			"message": "Growth Model Activity updated successfully.",
	    			"data": serializer.data
    			}, status=status.HTTP_204_NO_CONTENT)
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
		return Response({
			"status": "success",
			"data": "Growth Model Activity Deleted"
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

		growthModelActObjs = GrowthModelActivity.objects.filter(growthmodel_id=growthmodel_id)
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