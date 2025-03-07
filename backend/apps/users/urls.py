"""
用户URL配置模块

作者: AiTestPlantForm团队
创建日期: 2023-06-01
最后修改: 2023-06-10
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from .views import UserViewSet, RegisterView, CustomTokenObtainPairView

# 创建路由器
router = DefaultRouter()
router.register(r'', UserViewSet)

urlpatterns = [
    # JWT认证
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # 用户注册
    path('register/', RegisterView.as_view(), name='register'),
    
    # 用户管理
    path('', include(router.urls)),
] 