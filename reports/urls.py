from django.urls import path
from . import views

urlpatterns = [
    path('branch-summary/', views.branch_report, name='branch_report'),
]