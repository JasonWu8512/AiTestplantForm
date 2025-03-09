"""
测试执行视图模块

作者: AiTestPlantForm团队
创建日期: 2023-06-01
最后修改: 2023-06-10
"""

from django.db import transaction
from django.utils import timezone
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import TestExecution, TestResult
from .serializers import TestExecutionSerializer, TestResultSerializer
from apps.testplans.models import TestPlan, TestPlanCase
import logging


class TestExecutionViewSet(viewsets.ModelViewSet):
    """
    测试执行视图集
    
    提供测试执行的增删改查功能
    """
    queryset = TestExecution.objects.all()
    serializer_class = TestExecutionSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['plan__name', 'status']
    ordering_fields = ['created_at', 'start_time', 'end_time', 'status']
    ordering = ['-created_at']
    
    def list(self, request, *args, **kwargs):
        """
        获取测试执行列表
        
        Args:
            request: 请求对象
            
        Returns:
            Response: 测试执行列表
        """
        logger = logging.getLogger(__name__)
        
        logger.info("获取测试执行列表，请求参数: %s", request.query_params)
        queryset = self.filter_queryset(self.get_queryset())
        logger.info("过滤后的查询集数量: %d", queryset.count())
        
        # 直接返回所有数据，不使用分页
        serializer = self.get_serializer(queryset, many=True)
        logger.info("所有数据数量: %d", len(serializer.data))
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def start(self, request, pk=None):
        """
        开始测试执行
        
        Args:
            request: 请求对象
            pk: 测试执行ID
            
        Returns:
            Response: 操作结果
        """
        execution = self.get_object()
        
        if execution.status not in ['pending', 'paused']:
            return Response({
                'message': f'无法开始状态为 {execution.get_status_display()} 的测试执行'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        execution.status = 'running'
        if not execution.start_time:
            execution.start_time = timezone.now()
        execution.save()
        
        return Response({
            'message': '测试执行已开始'
        })
    
    @action(detail=True, methods=['post'])
    def pause(self, request, pk=None):
        """
        暂停测试执行
        
        Args:
            request: 请求对象
            pk: 测试执行ID
            
        Returns:
            Response: 操作结果
        """
        execution = self.get_object()
        
        if execution.status != 'running':
            return Response({
                'message': f'无法暂停状态为 {execution.get_status_display()} 的测试执行'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        execution.status = 'paused'
        execution.save()
        
        return Response({
            'message': '测试执行已暂停'
        })
    
    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        """
        完成测试执行
        
        Args:
            request: 请求对象
            pk: 测试执行ID
            
        Returns:
            Response: 操作结果
        """
        execution = self.get_object()
        
        if execution.status not in ['running', 'paused']:
            return Response({
                'message': f'无法完成状态为 {execution.get_status_display()} 的测试执行'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        execution.status = 'completed'
        execution.end_time = timezone.now()
        execution.save()
        
        return Response({
            'message': '测试执行已完成'
        })
    
    @action(detail=True, methods=['post'])
    def abort(self, request, pk=None):
        """
        中止测试执行
        
        Args:
            request: 请求对象
            pk: 测试执行ID
            
        Returns:
            Response: 操作结果
        """
        execution = self.get_object()
        
        if execution.status not in ['pending', 'running', 'paused']:
            return Response({
                'message': f'无法中止状态为 {execution.get_status_display()} 的测试执行'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        execution.status = 'aborted'
        execution.end_time = timezone.now()
        execution.save()
        
        return Response({
            'message': '测试执行已中止'
        })
    
    @action(detail=True, methods=['get'])
    def results(self, request, pk=None):
        """
        获取测试执行的结果列表
        
        Args:
            request: 请求对象
            pk: 测试执行ID
            
        Returns:
            Response: 测试结果列表
        """
        execution = self.get_object()
        results = execution.results.all()
        
        # 过滤
        case_name = request.query_params.get('case_name')
        status = request.query_params.get('status')
        
        if case_name:
            results = results.filter(case__name__icontains=case_name)
        
        if status:
            results = results.filter(status=status)
        
        # 分页
        page = self.paginate_queryset(results)
        if page is not None:
            serializer = TestResultSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = TestResultSerializer(results, many=True)
        
        # 统计数据
        stats = {
            'total': results.count(),
            'passed': results.filter(status='passed').count(),
            'failed': results.filter(status='failed').count(),
            'blocked': results.filter(status='blocked').count(),
            'skipped': results.filter(status='skipped').count(),
            'pending': results.filter(status='pending').count(),
        }
        
        return Response({
            'results': serializer.data,
            'stats': stats
        })


class TestResultViewSet(viewsets.ModelViewSet):
    """
    测试结果视图集
    
    提供测试结果的增删改查功能
    """
    queryset = TestResult.objects.all()
    serializer_class = TestResultSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['case__name', 'status', 'actual_result', 'remarks']
    ordering_fields = ['updated_at', 'execution_time', 'status']
    ordering = ['-updated_at']
    
    @action(detail=False, methods=['post'])
    def batch_update(self, request):
        """
        批量更新测试结果
        
        Args:
            request: 请求对象
            
        Returns:
            Response: 操作结果
        """
        results = request.data.get('results', [])
        
        if not results or not isinstance(results, list):
            return Response({
                'message': '缺少有效的results参数'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        updated_count = 0
        errors = []
        
        with transaction.atomic():
            for result_data in results:
                result_id = result_data.get('id')
                
                try:
                    result = TestResult.objects.get(id=result_id)
                    
                    # 更新状态
                    if 'status' in result_data:
                        result.status = result_data['status']
                    
                    # 更新备注
                    if 'remarks' in result_data:
                        result.remarks = result_data['remarks']
                    
                    # 更新实际结果
                    if 'actual_result' in result_data:
                        result.actual_result = result_data['actual_result']
                    
                    # 设置执行时间和执行者
                    result.execution_time = timezone.now()
                    result.executor = request.user
                    
                    result.save()
                    updated_count += 1
                except TestResult.DoesNotExist:
                    errors.append({
                        'id': result_id,
                        'message': '测试结果不存在'
                    })
                except Exception as e:
                    errors.append({
                        'id': result_id,
                        'message': str(e)
                    })
        
        return Response({
            'message': f'已更新 {updated_count} 个测试结果',
            'errors': errors
        }) 