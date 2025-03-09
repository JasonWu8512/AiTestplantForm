"""
测试执行序列化器模块

作者: AiTestPlantForm团队
创建日期: 2023-06-01
最后修改: 2023-06-10
"""

from rest_framework import serializers
from .models import TestExecution, TestResult
from apps.testplans.models import TestPlan
from apps.testcases.models import TestCase
from apps.users.serializers import UserSerializer
from django.utils import timezone
from apps.testplans.serializers import TestPlanSerializer


class TestPlanNestedSerializer(serializers.ModelSerializer):
    """
    嵌套的测试计划序列化器
    
    用于在测试执行中嵌套显示测试计划信息
    """
    project_name = serializers.ReadOnlyField(source='project.name')
    
    class Meta:
        model = TestPlan
        fields = ['id', 'name', 'project', 'project_name', 'status', 'start_time', 'end_time']


class TestExecutionSerializer(serializers.ModelSerializer):
    """
    测试执行序列化器
    
    用于测试执行数据的序列化和反序列化
    """
    executor_name = serializers.ReadOnlyField(source='executor.username')
    plan_name = serializers.ReadOnlyField(source='plan.name')
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    results_count = serializers.SerializerMethodField()
    plan_detail = TestPlanNestedSerializer(source='plan', read_only=True)
    
    class Meta:
        model = TestExecution
        fields = ['id', 'plan', 'plan_name', 'plan_detail', 'executor', 'executor_name', 'status', 
                  'status_display', 'start_time', 'end_time', 'results_count', 
                  'created_at', 'updated_at']
        read_only_fields = ['executor', 'created_at', 'updated_at']
    
    def get_results_count(self, obj):
        """
        获取测试执行下的测试结果数量
        
        Args:
            obj: 测试执行对象
            
        Returns:
            int: 测试结果数量
        """
        return obj.results.count()
    
    def create(self, validated_data):
        """
        创建测试执行
        
        Args:
            validated_data: 验证后的数据
            
        Returns:
            TestExecution: 创建的测试执行对象
        """
        # 设置执行者为当前用户
        validated_data['executor'] = self.context['request'].user
        
        # 创建测试执行
        execution = super().create(validated_data)
        
        # 获取测试计划
        plan = execution.plan
        
        # 获取测试计划下的所有测试用例
        plan_cases = plan.testplancase_set.all().order_by('order')
        
        # 为每个测试用例创建测试结果
        for plan_case in plan_cases:
            TestResult.objects.create(
                execution=execution,
                case=plan_case.case,
                status='pending'
            )
        
        return execution


class TestResultSerializer(serializers.ModelSerializer):
    """
    测试结果序列化器
    
    用于测试结果数据的序列化和反序列化
    """
    execution_id = serializers.ReadOnlyField(source='execution.id')
    case_id = serializers.ReadOnlyField(source='case.id')
    case_name = serializers.ReadOnlyField(source='case.name')
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    executor_name = serializers.ReadOnlyField(source='executor.username')
    case = serializers.SerializerMethodField()
    
    class Meta:
        model = TestResult
        fields = ['id', 'execution', 'execution_id', 'case', 'case_id', 'case_name', 
                  'status', 'status_display', 'actual_result', 'remarks', 
                  'executor', 'executor_name', 'execution_time', 
                  'created_at', 'updated_at']
        read_only_fields = ['execution', 'case', 'created_at', 'updated_at']
    
    def get_case(self, obj):
        """
        获取测试用例的简要信息
        
        Args:
            obj: 测试结果对象
            
        Returns:
            dict: 测试用例信息
        """
        return {
            'id': obj.case.id,
            'name': obj.case.name,
            'priority': obj.case.priority,
            'expected_results': obj.case.expected_results
        }
    
    def update(self, instance, validated_data):
        """
        更新测试结果
        
        Args:
            instance: 测试结果对象
            validated_data: 验证后的数据
            
        Returns:
            TestResult: 更新后的测试结果对象
        """
        # 如果状态从pending变为其他状态，设置执行时间和执行者
        if instance.status == 'pending' and validated_data.get('status') != 'pending':
            validated_data['execution_time'] = timezone.now()
            validated_data['executor'] = self.context['request'].user
        
        return super().update(instance, validated_data) 