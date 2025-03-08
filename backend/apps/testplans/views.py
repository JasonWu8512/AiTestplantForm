"""
测试计划视图模块

作者: AiTestPlantForm团队
创建日期: 2023-06-01
最后修改: 2023-06-10
"""

from django.db import transaction
from django.db.models import Q
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import TestPlan, TestPlanCase
from .serializers import (
    TestPlanSerializer, 
    TestPlanDetailSerializer,
    TestPlanCaseSerializer,
    TestCaseAddSerializer
)
from apps.testcases.models import TestCase


class TestPlanViewSet(viewsets.ModelViewSet):
    """
    测试计划视图集
    
    提供测试计划的增删改查功能
    """
    queryset = TestPlan.objects.all()
    serializer_class = TestPlanSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'status', 'start_time', 'end_time', 'created_at', 'updated_at']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        """
        获取序列化器类
        
        根据不同的操作返回不同的序列化器
        
        Returns:
            Serializer: 序列化器类
        """
        if self.action == 'retrieve':
            return TestPlanDetailSerializer
        elif self.action == 'add_test_cases':
            return TestCaseAddSerializer
        return TestPlanSerializer
    
    def get_queryset(self):
        """
        获取查询集
        
        根据查询参数过滤测试计划
        
        Returns:
            QuerySet: 过滤后的测试计划查询集
        """
        queryset = super().get_queryset()
        
        # 项目过滤
        project_id = self.request.query_params.get('project')
        if project_id:
            queryset = queryset.filter(project_id=project_id)
        
        # 状态过滤
        status = self.request.query_params.get('status')
        if status:
            queryset = queryset.filter(status=status)
        
        # 关键字搜索
        keyword = self.request.query_params.get('keyword')
        if keyword:
            queryset = queryset.filter(
                Q(name__icontains=keyword) | 
                Q(description__icontains=keyword)
            )
        
        return queryset
    
    @action(detail=True, methods=['post'])
    def add_test_cases(self, request, pk=None):
        """
        向测试计划添加测试用例
        
        Args:
            request: 请求对象
            pk: 测试计划ID
            
        Returns:
            Response: 添加结果
        """
        test_plan = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        case_ids = serializer.validated_data['case_ids']
        
        # 获取测试计划中已有的测试用例ID
        existing_case_ids = set(test_plan.test_cases.values_list('id', flat=True))
        
        # 过滤出需要添加的测试用例ID
        new_case_ids = set(case_ids) - existing_case_ids
        
        if not new_case_ids:
            return Response({
                'message': '所有测试用例已在测试计划中'
            }, status=status.HTTP_200_OK)
        
        # 获取当前测试计划中的最大顺序值
        max_order = TestPlanCase.objects.filter(plan=test_plan).order_by('-order').values_list('order', flat=True).first() or 0
        
        # 添加测试用例到测试计划
        with transaction.atomic():
            for i, case_id in enumerate(new_case_ids):
                TestPlanCase.objects.create(
                    plan=test_plan,
                    case_id=case_id,
                    order=max_order + i + 1
                )
        
        return Response({
            'message': f'成功添加 {len(new_case_ids)} 个测试用例到测试计划'
        }, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['delete'])
    def remove_test_case(self, request, pk=None):
        """
        从测试计划中移除测试用例
        
        Args:
            request: 请求对象
            pk: 测试计划ID
            
        Returns:
            Response: 移除结果
        """
        test_plan = self.get_object()
        case_id = request.query_params.get('case_id')
        
        if not case_id:
            return Response({
                'message': '缺少测试用例ID参数'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # 查找并删除测试计划-用例关联
            plan_case = TestPlanCase.objects.get(plan=test_plan, case_id=case_id)
            plan_case.delete()
            
            return Response({
                'message': '测试用例已从测试计划中移除'
            }, status=status.HTTP_200_OK)
        except TestPlanCase.DoesNotExist:
            return Response({
                'message': '测试用例不在测试计划中'
            }, status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=True, methods=['put'])
    def reorder_test_cases(self, request, pk=None):
        """
        重新排序测试计划中的测试用例
        
        Args:
            request: 请求对象
            pk: 测试计划ID
            
        Returns:
            Response: 排序结果
        """
        test_plan = self.get_object()
        case_orders = request.data.get('case_orders', [])
        
        if not case_orders or not isinstance(case_orders, list):
            return Response({
                'message': '缺少有效的case_orders参数'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # 验证所有测试用例都存在于测试计划中
        case_ids = [item.get('case_id') for item in case_orders if 'case_id' in item]
        existing_plan_cases = TestPlanCase.objects.filter(plan=test_plan, case_id__in=case_ids)
        existing_case_ids = set(existing_plan_cases.values_list('case_id', flat=True))
        
        non_existing_case_ids = set(case_ids) - existing_case_ids
        if non_existing_case_ids:
            return Response({
                'message': f'以下测试用例不在测试计划中: {", ".join(map(str, non_existing_case_ids))}'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # 更新测试用例顺序
        with transaction.atomic():
            for item in case_orders:
                case_id = item.get('case_id')
                order = item.get('order')
                
                if case_id and order is not None:
                    TestPlanCase.objects.filter(plan=test_plan, case_id=case_id).update(order=order)
        
        return Response({
            'message': '测试用例顺序已更新'
        }, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['post'])
    def create_execution(self, request, pk=None):
        """
        从测试计划创建测试执行
        
        Args:
            request: 请求对象
            pk: 测试计划ID
            
        Returns:
            Response: 创建结果
        """
        from apps.executions.models import TestExecution
        from apps.executions.serializers import TestExecutionSerializer
        
        test_plan = self.get_object()
        
        # 检查测试计划状态
        if test_plan.status not in ['ready', 'in_progress']:
            return Response({
                'message': f'无法从状态为 {test_plan.get_status_display()} 的测试计划创建测试执行'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # 检查测试计划是否包含测试用例
        if not test_plan.test_cases.exists():
            return Response({
                'message': '测试计划不包含任何测试用例'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # 创建测试执行
        execution_data = {
            'plan': test_plan.id,
            'status': 'pending'
        }
        
        serializer = TestExecutionSerializer(
            data=execution_data,
            context={'request': request}
        )
        
        if serializer.is_valid():
            execution = serializer.save()
            
            # 如果测试计划状态为ready，更新为in_progress
            if test_plan.status == 'ready':
                test_plan.status = 'in_progress'
                test_plan.save()
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 