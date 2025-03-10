"""
测试报告序列化器模块

作者: AiTestPlantForm团队
创建日期: 2023-06-01
最后修改: 2023-06-10
"""

from rest_framework import serializers
from .models import Report


class ReportSerializer(serializers.ModelSerializer):
    """
    测试报告序列化器
    
    用于测试报告数据的序列化和反序列化
    """
    creator_name = serializers.ReadOnlyField(source='creator.username')
    execution_name = serializers.ReadOnlyField(source='execution.plan.name')
    report_type_display = serializers.CharField(source='get_report_type_display', read_only=True)
    
    class Meta:
        model = Report
        fields = ['id', 'name', 'description', 'execution', 'execution_name', 
                  'report_type', 'report_type_display', 'file_path', 'is_public', 
                  'creator', 'creator_name', 'created_at', 'updated_at']
        read_only_fields = ['creator', 'created_at', 'updated_at']
    
    def create(self, validated_data):
        """
        创建测试报告
        
        Args:
            validated_data: 验证后的数据
            
        Returns:
            Report: 创建的测试报告对象
        """
        # 设置创建者为当前用户
        validated_data['creator'] = self.context['request'].user
        return super().create(validated_data)


class ReportListSerializer(serializers.ModelSerializer):
    """
    测试报告列表序列化器
    
    用于测试报告列表数据的序列化，包含较少的字段
    """
    creator_name = serializers.ReadOnlyField(source='creator.username')
    execution_name = serializers.ReadOnlyField(source='execution.plan.name')
    report_type_display = serializers.CharField(source='get_report_type_display', read_only=True)
    
    class Meta:
        model = Report
        fields = ['id', 'name', 'description', 'execution', 'execution_name', 'report_type', 
                  'report_type_display', 'is_public', 'creator_name', 
                  'created_at', 'updated_at'] 