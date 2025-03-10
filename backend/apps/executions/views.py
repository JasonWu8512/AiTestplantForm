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
from apps.testcases.models import TestCase
from apps.reports.views import generate_report
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
        
        # 获取查询参数
        plan_name = request.query_params.get('plan_name', None)
        status_param = request.query_params.get('status', None)
        
        # 详细记录请求参数
        logger.info(f"获取测试执行列表请求参数: {request.query_params}")
        logger.info(f"解析后的参数 - plan_name: {plan_name}, status: {status_param}")
        
        # 获取初始查询集
        queryset = self.get_queryset()
        logger.info(f"初始查询集数量: {queryset.count()}")
        
        # 根据参数过滤
        if plan_name:
            logger.info(f"根据计划名称过滤: {plan_name}")
            queryset = queryset.filter(plan__name__icontains=plan_name)
            logger.info(f"计划名称过滤后的查询集数量: {queryset.count()}")
        
        if status_param:
            logger.info(f"根据状态过滤: {status_param}")
            queryset = queryset.filter(status=status_param)
            logger.info(f"状态过滤后的查询集数量: {queryset.count()}")
        
        # 应用其他过滤器（排序等）
        queryset = self.filter_queryset(queryset)
        
        logger.info("过滤后的查询集数量: %d", queryset.count())
        
        # 序列化数据
        serializer = self.get_serializer(queryset, many=True)
        logger.info(f"序列化后的数据数量: {len(serializer.data)}")
        
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
        
        # 自动生成测试报告
        auto_generate_report = request.data.get('auto_generate_report', True)
        if auto_generate_report:
            # 默认生成Allure报告
            report_type = request.data.get('report_type', 'allure')
            # 生成默认报告名称
            report_name = f"{execution.plan.name} - 自动生成报告 - {timezone.now().strftime('%Y-%m-%d %H:%M:%S')}"
            # 生成默认描述
            description = f"测试执行 {execution.id} 完成后自动生成的报告"
            
            # 异步生成报告
            generate_report.delay(
                execution_id=execution.id,
                report_type=report_type,
                name=report_name,
                description=description,
                user_id=request.user.id
            )
        
        return Response({
            'message': '测试执行已完成，报告生成任务已提交'
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
        
        # 统计数据 - 在分页前计算，确保统计的是所有符合条件的结果
        stats = {
            'total': results.count(),
            'passed': results.filter(status='passed').count(),
            'failed': results.filter(status='failed').count(),
            'blocked': results.filter(status='blocked').count(),
            'skipped': results.filter(status='skipped').count(),
            'pending': results.filter(status='pending').count(),
        }
        
        # 分页
        page = self.paginate_queryset(results)
        if page is not None:
            serializer = TestResultSerializer(page, many=True)
            paginated_response = self.get_paginated_response(serializer.data)
            # 将统计数据添加到分页响应中
            paginated_response.data['stats'] = stats
            return paginated_response
        
        serializer = TestResultSerializer(results, many=True)
        
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