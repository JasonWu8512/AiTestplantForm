"""
URL配置模块

作者: AiTestPlantForm团队
创建日期: 2023-06-01
最后修改: 2023-06-10
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Swagger文档配置
schema_view = get_schema_view(
    openapi.Info(
        title="AiTestPlantForm API",
        default_version='v1',
        description="AiTestPlantForm测试平台API文档",
        terms_of_service="https://www.example.com/terms/",
        contact=openapi.Contact(email="contact@example.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

# API URL模式
api_patterns = [
    # 各模块的URL配置
    path('users/', include('apps.users.urls')),
    # path('testcases/', include('apps.testcases.urls')),
    # path('testplans/', include('apps.testplans.urls')),
    # path('executions/', include('apps.executions.urls')),
    # path('reports/', include('apps.reports.urls')),
    # path('dashboard/', include('apps.dashboard.urls')),
]

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # API路由
    path('api/', include(api_patterns)),
    
    # Swagger文档
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

# 在开发环境中提供媒体文件服务
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
