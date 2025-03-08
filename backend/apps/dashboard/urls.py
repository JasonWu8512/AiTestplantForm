"""
Dashboard URL配置模块

作者: AiTestPlantForm团队
创建日期: 2023-06-01
最后修改: 2023-06-10
"""

from django.urls import path
from .views import DashboardSummaryView, DashboardStatisticsView

urlpatterns = [
    path('summary/', DashboardSummaryView.as_view(), name='dashboard-summary'),
    path('statistics/', DashboardStatisticsView.as_view(), name='dashboard-statistics'),
] 