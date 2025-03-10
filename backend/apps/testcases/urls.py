"""
测试用例URL配置模块

作者: AiTestPlantForm团队
创建日期: 2023-06-01
最后修改: 2023-06-10
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProjectViewSet, TestCaseViewSet, export_testcases, simple_export

# 创建项目路由器 - 用于/api/projects/路径
project_router = DefaultRouter()
project_router.register(r'', ProjectViewSet, basename='project')

# 创建测试用例路由器 - 用于/api/testcases/路径
testcase_router = DefaultRouter()
testcase_router.register(r'', TestCaseViewSet, basename='testcase')

# 项目URL模式
project_urlpatterns = [
    path('', include(project_router.urls)),
]

# 测试用例URL模式
testcase_urlpatterns = [
    path('', include(testcase_router.urls)),
    # 添加自定义路由
    path('export/', export_testcases, name='export-testcases'),
    path('simple-export/', simple_export, name='simple-export'),
] 