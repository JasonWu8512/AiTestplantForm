"""
测试计划序列化器模块

作者: AiTestPlantForm团队
创建日期: 2023-06-01
最后修改: 2023-06-10
"""

from rest_framework import serializers
from .models import TestPlan, TestPlanCase
from apps.testcases.models import TestCase
from apps.testcases.serializers import TestCaseListSerializer


class TestPlanCaseSerializer(serializers.ModelSerializer):
    """
    测试计划-用例关联序列化器
    
    用于测试计划-用例关联数据的序列化和反序列化
    """
    case_detail = TestCaseListSerializer(source='case', read_only=True)
    
    class Meta:
        model = TestPlanCase
        fields = ['id', 'plan', 'case', 'case_detail', 'order']
        read_only_fields = ['plan']


class TestPlanSerializer(serializers.ModelSerializer):
    """
    测试计划序列化器
    
    用于测试计划数据的序列化和反序列化
    """
    creator_name = serializers.ReadOnlyField(source='creator.username')
    project_name = serializers.ReadOnlyField(source='project.name')
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    test_cases_count = serializers.SerializerMethodField()
    
    class Meta:
        model = TestPlan
        fields = ['id', 'name', 'description', 'status', 'status_display', 'start_time', 
                  'end_time', 'project', 'project_name', 'creator', 'creator_name', 
                  'test_cases_count', 'created_at', 'updated_at']
        read_only_fields = ['creator', 'created_at', 'updated_at']
    
    def get_test_cases_count(self, obj):
        """
        获取测试计划下的测试用例数量
        
        Args:
            obj: 测试计划对象
            
        Returns:
            int: 测试用例数量
        """
        return obj.test_cases.count()
    
    def create(self, validated_data):
        """
        创建测试计划
        
        Args:
            validated_data: 验证后的数据
            
        Returns:
            TestPlan: 创建的测试计划对象
        """
        # 设置创建者为当前用户
        validated_data['creator'] = self.context['request'].user
        return super().create(validated_data)


class TestPlanDetailSerializer(TestPlanSerializer):
    """
    测试计划详情序列化器
    
    用于测试计划详情数据的序列化，包含测试用例列表
    """
    test_cases = serializers.SerializerMethodField()
    
    class Meta(TestPlanSerializer.Meta):
        fields = TestPlanSerializer.Meta.fields + ['test_cases']
    
    def get_test_cases(self, obj):
        """
        获取测试计划下的测试用例列表
        
        Args:
            obj: 测试计划对象
            
        Returns:
            list: 测试用例列表
        """
        # 获取测试计划-用例关联对象，并按执行顺序排序
        plan_cases = TestPlanCase.objects.filter(plan=obj).order_by('order')
        
        # 序列化测试计划-用例关联对象
        serializer = TestPlanCaseSerializer(plan_cases, many=True)
        return serializer.data


class TestCaseAddSerializer(serializers.Serializer):
    """
    测试用例添加序列化器
    
    用于向测试计划添加测试用例的数据验证
    """
    case_ids = serializers.ListField(
        child=serializers.IntegerField(),
        help_text='测试用例ID列表'
    )
    
    def validate_case_ids(self, value):
        """
        验证测试用例ID列表
        
        Args:
            value: 测试用例ID列表
            
        Returns:
            list: 验证后的测试用例ID列表
            
        Raises:
            serializers.ValidationError: 当测试用例不存在时抛出
        """
        # 检查测试用例是否存在
        existing_ids = set(TestCase.objects.filter(id__in=value).values_list('id', flat=True))
        non_existing_ids = set(value) - existing_ids
        
        if non_existing_ids:
            raise serializers.ValidationError(f"以下测试用例不存在: {', '.join(map(str, non_existing_ids))}")
        
        return value