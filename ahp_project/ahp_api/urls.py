from django.urls import path
from .views import AHPCalculationView, UserProjectsView

urlpatterns = [
    path('calculate/', AHPCalculationView.as_view(), name='ahp-calculate'),
    path('projects/', UserProjectsView.as_view(), name='user-projects'),
]