from rest_framework.exceptions import APIException
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from account.authentication import UserTokenAuthentication
from growthmodel.models import *
from growthmodel.api.v1.serializers import *
from rest_framework import status

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
			}, status=404)

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

class GetGrowthModelActivityView(APIView):
	authentication_classes = [UserTokenAuthentication,]
	permission_classes = (IsAuthenticated,)

	def get(self, request):
		try:
			growthmodel_obj = GrowthModel.objects.get(user_id=request.user.id)
		except:
			return Response({
				"message": "No growth model found."
			}, status=404)

		growthmodel_activities = GrowthModelActivity.objects.filter(
			growth_model=growthmodel_obj.id)

		data = []
		if growthmodel_activities.count() > 0:
			data = GetGrowthModelActivitySerializer(growthmodel_activities, many=True).data

		return Response({
				"data": data
			}, status=status.HTTP_200_OK)

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