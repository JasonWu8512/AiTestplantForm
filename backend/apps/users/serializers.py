"""
用户序列化器模块

作者: AiTestPlantForm团队
创建日期: 2023-06-01
最后修改: 2023-06-10
"""

from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """
    用户序列化器
    
    用于用户信息的序列化和反序列化
    """
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 
                 'phone', 'department', 'position', 'avatar', 'is_active', 
                 'date_joined', 'created_at', 'updated_at']
        read_only_fields = ['id', 'date_joined', 'created_at', 'updated_at']


class UserCreateSerializer(serializers.ModelSerializer):
    """
    用户创建序列化器
    
    用于用户注册，包含密码验证逻辑
    """
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'password2', 'email', 'first_name', 'last_name', 
                 'phone', 'department', 'position']

    def validate(self, attrs):
        """验证两次输入的密码是否一致"""
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "两次密码输入不一致"})
        return attrs

    def create(self, validated_data):
        """创建用户并设置密码"""
        validated_data.pop('password2')
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            phone=validated_data.get('phone', ''),
            department=validated_data.get('department', ''),
            position=validated_data.get('position', '')
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class UserUpdateSerializer(serializers.ModelSerializer):
    """
    用户更新序列化器
    
    用于用户信息更新，不包含密码字段
    """
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'phone', 'department', 'position', 'avatar']


class ChangePasswordSerializer(serializers.Serializer):
    """
    密码修改序列化器
    
    用于用户密码修改
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, validators=[validate_password])
    new_password2 = serializers.CharField(required=True)

    def validate(self, attrs):
        """验证两次输入的新密码是否一致"""
        if attrs['new_password'] != attrs['new_password2']:
            raise serializers.ValidationError({"new_password": "两次密码输入不一致"})
        return attrs


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    自定义JWT令牌序列化器
    
    扩展默认的JWT令牌序列化器，添加额外的用户信息
    """
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # 添加自定义声明
        token['username'] = user.username
        token['email'] = user.email
        token['is_staff'] = user.is_staff
        return token 