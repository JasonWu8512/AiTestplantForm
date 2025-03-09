"""
用户视图模块

作者: AiTestPlantForm团队
创建日期: 2023-06-01
最后修改: 2023-06-10
"""

from rest_framework import viewsets, generics, status, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import get_user_model
from .models import User
from .serializers import (
    UserSerializer, 
    UserCreateSerializer, 
    UserUpdateSerializer, 
    ChangePasswordSerializer,
    CustomTokenObtainPairSerializer
)

User = get_user_model()


class CustomTokenObtainPairView(TokenObtainPairView):
    """
    自定义JWT令牌视图
    
    用于用户登录并获取JWT令牌
    """
    serializer_class = CustomTokenObtainPairSerializer


class RegisterView(generics.CreateAPIView):
    """
    用户注册视图
    
    允许任何用户注册新账号
    """
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = [permissions.AllowAny]


class UserViewSet(viewsets.ModelViewSet):
    """
    用户视图集
    
    提供用户的CRUD操作
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    def get_serializer_class(self):
        """根据操作类型返回不同的序列化器"""
        if self.action == 'create':
            return UserCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return UserUpdateSerializer
        return UserSerializer
    
    def get_permissions(self):
        """根据操作类型设置不同的权限"""
        if self.action == 'create':
            permission_classes = [permissions.AllowAny]
        elif self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [permissions.IsAuthenticated]
        elif self.action == 'list':
            permission_classes = [permissions.IsAdminUser]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def me(self, request):
        """获取当前登录用户的信息"""
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)
    
    @action(detail=False, methods=['put'], permission_classes=[permissions.IsAuthenticated])
    def update_me(self, request):
        """
        更新当前登录用户的信息
        
        允许用户更新自己的个人信息，包括基本信息和头像。
        支持通过FormData上传头像文件或使用默认头像。
        
        Args:
            request (Request): 请求对象，包含用户信息数据
            
        Returns:
            Response: 更新后的用户信息
            
        Raises:
            ValidationError: 当提供的数据无效时抛出
        """
        # 处理默认头像
        data = request.data.copy()
        
        # 检查是否使用默认头像
        if 'use_default_avatar' in data:
            default_avatar = data.get('use_default_avatar')
            if default_avatar:
                # 验证是否是有效的默认头像
                if 'male' in default_avatar or 'female' in default_avatar:
                    # 构建完整的头像路径 - 使用完整的URL路径
                    avatar_path = f'/avatars/{default_avatar}'
                    
                    # 将默认头像路径设置为用户的avatar字段
                    user = request.user
                    # 直接设置avatar字段的值，而不是通过ImageField
                    from django.db.models import Value
                    from django.db.models.functions import Concat
                    
                    # 更新用户记录，直接设置avatar字段为字符串路径
                    User.objects.filter(pk=user.pk).update(avatar=avatar_path)
                    
                    # 重新获取用户对象，确保avatar字段已更新
                    user.refresh_from_db()
                    
                    # 记录日志
                    print(f"已设置默认头像: {avatar_path}")
                    print(f"用户头像字段值: {user.avatar}")
                    
                    # 移除use_default_avatar字段，避免序列化器验证错误
                    data.pop('use_default_avatar')
                    
                    # 如果没有其他字段需要更新，直接返回更新后的用户信息
                    if len(data) == 0:
                        serializer = self.get_serializer(user)
                        return Response(serializer.data)
        
        # 处理常规表单数据
        serializer = UserUpdateSerializer(request.user, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['put'], permission_classes=[permissions.IsAuthenticated])
    def change_password(self, request):
        """修改当前登录用户的密码"""
        user = request.user
        serializer = ChangePasswordSerializer(data=request.data)
        
        if serializer.is_valid():
            # 检查旧密码
            if not user.check_password(serializer.validated_data['old_password']):
                return Response({"old_password": ["旧密码不正确"]}, status=status.HTTP_400_BAD_REQUEST)
            
            # 设置新密码
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            return Response({"message": "密码修改成功"}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 