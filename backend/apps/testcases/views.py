"""
测试用例视图模块

作者: AiTestPlantForm团队
创建日期: 2023-06-01
最后修改: 2023-06-10
"""

import csv
import io
# import pandas as pd  # 暂时注释掉pandas导入
from django.http import HttpResponse
from django.db.models import Q
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Project, TestCase
from .serializers import (
    ProjectSerializer, 
    TestCaseSerializer, 
    TestCaseListSerializer,
    TestCaseImportSerializer
)


class ProjectViewSet(viewsets.ModelViewSet):
    """
    项目视图集
    
    提供项目的增删改查功能
    """
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_at', 'updated_at']
    ordering = ['-created_at']
    
    def get_queryset(self):
        """
        获取查询集
        
        根据查询参数过滤项目
        
        Returns:
            QuerySet: 过滤后的项目查询集
        """
        queryset = super().get_queryset()
        status = self.request.query_params.get('status')
        if status:
            queryset = queryset.filter(status=status)
        return queryset
    
    @action(detail=True, methods=['get'])
    def test_cases(self, request, pk=None):
        """
        获取项目下的测试用例
        
        Args:
            request: 请求对象
            pk: 项目ID
            
        Returns:
            Response: 测试用例列表
        """
        project = self.get_object()
        test_cases = project.test_cases.all()
        serializer = TestCaseListSerializer(test_cases, many=True)
        return Response(serializer.data)


class TestCaseViewSet(viewsets.ModelViewSet):
    """
    测试用例视图集
    
    提供测试用例的增删改查功能
    """
    queryset = TestCase.objects.all()
    serializer_class = TestCaseSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description', 'steps', 'expected_results']
    ordering_fields = ['name', 'priority', 'status', 'created_at', 'updated_at']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        """
        获取序列化器类
        
        根据不同的操作返回不同的序列化器
        
        Returns:
            Serializer: 序列化器类
        """
        if self.action == 'list':
            return TestCaseListSerializer
        elif self.action == 'import_cases':
            return TestCaseImportSerializer
        return TestCaseSerializer
    
    def get_queryset(self):
        """
        获取查询集
        
        根据查询参数过滤测试用例
        
        Returns:
            QuerySet: 过滤后的测试用例查询集
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
        
        # 优先级过滤
        priority = self.request.query_params.get('priority')
        if priority:
            queryset = queryset.filter(priority=priority)
        
        # 关键字搜索
        keyword = self.request.query_params.get('keyword')
        if keyword:
            queryset = queryset.filter(
                Q(name__icontains=keyword) | 
                Q(description__icontains=keyword) | 
                Q(steps__icontains=keyword) | 
                Q(expected_results__icontains=keyword)
            )
        
        return queryset
    
    @action(detail=False, methods=['post'])
    def import_cases(self, request):
        """
        导入测试用例
        
        支持CSV格式的测试用例导入（暂时禁用Excel导入）
        
        Args:
            request: 请求对象
            
        Returns:
            Response: 导入结果
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        file = serializer.validated_data['file']
        project = serializer.validated_data['project']
        
        # 获取文件扩展名
        ext = file.name.split('.')[-1].lower()
        
        try:
            # 根据文件类型读取数据
            if ext == 'csv':
                # 读取CSV文件
                csv_data = file.read().decode('utf-8')
                reader = csv.DictReader(io.StringIO(csv_data))
                rows = list(reader)
            else:
                # 暂时不支持Excel导入
                return Response({
                    'message': '暂时不支持Excel格式导入，请使用CSV格式',
                    'errors': ['不支持的文件格式']
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # 导入测试用例
            created_count = 0
            error_count = 0
            errors = []
            
            for row in rows:
                try:
                    # 创建测试用例
                    TestCase.objects.create(
                        name=row.get('name', ''),
                        description=row.get('description', ''),
                        priority=row.get('priority', 'P2'),
                        status=row.get('status', 'draft'),
                        steps=row.get('steps', ''),
                        expected_results=row.get('expected_results', ''),
                        project=project,
                        creator=request.user
                    )
                    created_count += 1
                except Exception as e:
                    error_count += 1
                    errors.append(f"行 {rows.index(row) + 2}: {str(e)}")
            
            return Response({
                'message': f'导入完成，成功导入 {created_count} 条测试用例，失败 {error_count} 条',
                'created_count': created_count,
                'error_count': error_count,
                'errors': errors
            }, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            return Response({
                'message': f'导入失败: {str(e)}',
                'errors': [str(e)]
            }, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'])
    def export_cases(self, request):
        """
        导出测试用例
        
        支持CSV格式的测试用例导出
        
        Args:
            request: 请求对象
            
        Returns:
            HttpResponse: 包含测试用例数据的CSV文件
        """
        # 获取要导出的测试用例
        queryset = self.filter_queryset(self.get_queryset())
        
        # 创建CSV响应
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="test_cases.csv"'
        
        # 写入CSV头
        writer = csv.writer(response)
        writer.writerow(['ID', '用例名称', '描述', '优先级', '状态', '测试步骤', '预期结果', '项目', '创建者', '创建时间', '更新时间'])
        
        # 写入测试用例数据
        for case in queryset:
            writer.writerow([
                case.id,
                case.name,
                case.description,
                case.get_priority_display(),
                case.get_status_display(),
                case.steps,
                case.expected_results,
                case.project.name,
                case.creator.username,
                case.created_at,
                case.updated_at
            ])
        
        return response 