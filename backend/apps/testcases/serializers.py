"""
测试用例序列化器模块

作者: AiTestPlantForm团队
创建日期: 2023-06-01
最后修改: 2023-06-10
"""

from rest_framework import serializers
from .models import Project, TestCase


class ProjectSerializer(serializers.ModelSerializer):
    """
    项目序列化器
    
    用于项目数据的序列化和反序列化
    """
    creator_name = serializers.ReadOnlyField(source='creator.username')
    test_cases_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'status', 'creator', 'creator_name', 
                  'test_cases_count', 'created_at', 'updated_at']
        read_only_fields = ['creator', 'created_at', 'updated_at']
    
    def get_test_cases_count(self, obj):
        """
        获取项目下的测试用例数量
        
        Args:
            obj: 项目对象
            
        Returns:
            int: 测试用例数量
        """
        return obj.test_cases.count()
    
    def create(self, validated_data):
        """
        创建项目
        
        Args:
            validated_data: 验证后的数据
            
        Returns:
            Project: 创建的项目对象
        """
        # 设置创建者为当前用户
        validated_data['creator'] = self.context['request'].user
        return super().create(validated_data)


class TestCaseSerializer(serializers.ModelSerializer):
    """
    测试用例序列化器
    
    用于测试用例数据的序列化和反序列化
    """
    creator_name = serializers.ReadOnlyField(source='creator.username')
    project_name = serializers.ReadOnlyField(source='project.name')
    priority_display = serializers.CharField(source='get_priority_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = TestCase
        fields = ['id', 'name', 'description', 'priority', 'priority_display', 'status', 
                  'status_display', 'steps', 'expected_results', 'project', 'project_name', 
                  'creator', 'creator_name', 'created_at', 'updated_at']
        read_only_fields = ['creator', 'created_at', 'updated_at']
    
    def create(self, validated_data):
        """
        创建测试用例
        
        Args:
            validated_data: 验证后的数据
            
        Returns:
            TestCase: 创建的测试用例对象
        """
        # 设置创建者为当前用户
        validated_data['creator'] = self.context['request'].user
        return super().create(validated_data)


class TestCaseListSerializer(serializers.ModelSerializer):
    """
    测试用例列表序列化器
    
    用于测试用例列表数据的序列化，包含较少的字段
    """
    creator_name = serializers.ReadOnlyField(source='creator.username')
    project_name = serializers.ReadOnlyField(source='project.name')
    priority_display = serializers.CharField(source='get_priority_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = TestCase
        fields = ['id', 'name', 'priority', 'priority_display', 'status', 'status_display', 
                  'project', 'project_name', 'creator_name', 'created_at', 'updated_at']


class TestCaseImportSerializer(serializers.Serializer):
    """
    测试用例导入序列化器
    
    用于测试用例导入数据的验证
    """
    file = serializers.FileField(help_text='CSV或Excel文件')
    project = serializers.PrimaryKeyRelatedField(queryset=Project.objects.all(), help_text='项目ID')
    
    def validate_file(self, value):
        """
        验证文件格式
        
        Args:
            value: 文件对象
            
        Returns:
            FileField: 验证后的文件对象
            
        Raises:
            serializers.ValidationError: 当文件格式不支持时抛出
        """
        # 获取文件扩展名
        ext = value.name.split('.')[-1].lower()
        if ext not in ['csv', 'xlsx', 'xls']:
            raise serializers.ValidationError('仅支持CSV和Excel文件格式')
        return value 