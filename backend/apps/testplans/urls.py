"""
测试计划URL配置模块

作者: AiTestPlantForm团队
创建日期: 2023-06-01
最后修改: 2023-06-10
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TestPlanViewSet

# 创建路由器
router = DefaultRouter()
router.register(r'', TestPlanViewSet, basename='testplan')

# URL模式
urlpatterns = [
    path('', include(router.urls)),
]