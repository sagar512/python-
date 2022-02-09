from django.urls import path, re_path
from growthmodel.api.v1.views import *

app_name = 'growthmodel_api'

urlpatterns = [
    path('create_growth_model', CreateGrowthModelView.as_view(), name='create_growth_model'),
    path('get_growth_model', GetGrowthModelView.as_view(), name='get_growth_model'),
    path('update_growth_model/<uuid:id>', UpdateGrowthModelView.as_view(), name='update_growth_model'),
    path('get_professions', GetProfessionView.as_view(), name='get_professions'),
]