"""
测试报告视图模块

作者: AiTestPlantForm团队
创建日期: 2023-06-01
最后修改: 2023-06-10
"""

import os
import json
import logging
import tempfile
import zipfile
import shutil
from django.conf import settings
from django.http import FileResponse, HttpResponse
from django.utils import timezone
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Report
from .serializers import ReportSerializer, ReportListSerializer
from apps.executions.models import TestExecution, TestResult
from celery import shared_task


class ReportViewSet(viewsets.ModelViewSet):
    """
    测试报告视图集
    
    提供测试报告的增删改查功能
    """
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'execution__plan__name']
    ordering_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        """
        根据不同的操作返回不同的序列化器
        
        Returns:
            Serializer: 序列化器类
        """
        if self.action == 'list':
            return ReportListSerializer
        return ReportSerializer
    
    @action(detail=False, methods=['post'])
    def generate(self, request):
        """
        生成测试报告
        
        Args:
            request: 请求对象，包含测试执行ID和报告类型
            
        Returns:
            Response: 操作结果
        """
        execution_id = request.data.get('execution_id')
        report_type = request.data.get('report_type', 'allure')
        name = request.data.get('name')
        description = request.data.get('description', '')
        
        if not execution_id:
            return Response({
                'message': '缺少测试执行ID'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            execution = TestExecution.objects.get(id=execution_id)
        except TestExecution.DoesNotExist:
            return Response({
                'message': '测试执行不存在'
            }, status=status.HTTP_404_NOT_FOUND)
        
        # 如果没有提供报告名称，则使用默认名称
        if not name:
            name = f"{execution.plan.name} - 测试报告 - {timezone.now().strftime('%Y-%m-%d %H:%M:%S')}"
        
        # 异步生成报告
        task = generate_report.delay(
            execution_id=execution_id,
            report_type=report_type,
            name=name,
            description=description,
            user_id=request.user.id
        )
        
        return Response({
            'message': '测试报告生成任务已提交',
            'task_id': task.id
        })
    
    @action(detail=True, methods=['get'])
    def download(self, request, pk=None):
        """
        下载测试报告
        
        Args:
            request: 请求对象
            pk: 测试报告ID
            
        Returns:
            FileResponse: 文件响应
        """
        report = self.get_object()
        file_path = report.file_path
        
        if not os.path.exists(file_path):
            return Response({
                'message': '报告文件不存在'
            }, status=status.HTTP_404_NOT_FOUND)
        
        # 如果是目录，则需要先打包
        if os.path.isdir(file_path):
            # 创建临时文件
            with tempfile.NamedTemporaryFile(delete=False, suffix='.zip') as temp_file:
                temp_path = temp_file.name
            
            # 打包目录
            with zipfile.ZipFile(temp_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for root, dirs, files in os.walk(file_path):
                    for file in files:
                        file_path = os.path.join(root, file)
                        arcname = os.path.relpath(file_path, os.path.dirname(file_path))
                        zipf.write(file_path, arcname)
            
            # 返回打包后的文件
            response = FileResponse(open(temp_path, 'rb'))
            response['Content-Disposition'] = f'attachment; filename="{report.name}.zip"'
            response['Content-Type'] = 'application/zip'
            return response
        else:
            # 返回单个文件
            response = FileResponse(open(file_path, 'rb'))
            response['Content-Disposition'] = f'attachment; filename="{os.path.basename(file_path)}"'
            return response
    
    @action(detail=True, methods=['get'])
    def view(self, request, pk=None):
        """
        查看测试报告
        
        Args:
            request: 请求对象
            pk: 测试报告ID
            
        Returns:
            HttpResponse: HTML响应
        """
        report = self.get_object()
        file_path = report.file_path
        
        if not os.path.exists(file_path):
            return Response({
                'message': '报告文件不存在'
            }, status=status.HTTP_404_NOT_FOUND)
        
        # 如果是Allure报告，返回index.html
        if report.report_type == 'allure' and os.path.isdir(file_path):
            index_path = os.path.join(file_path, 'index.html')
            if os.path.exists(index_path):
                with open(index_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                return HttpResponse(content, content_type='text/html')
        
        # 如果是HTML报告，直接返回
        if report.report_type == 'html' and file_path.endswith('.html'):
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            return HttpResponse(content, content_type='text/html')
        
        # 其他情况，返回文件下载
        return self.download(request, pk)


@shared_task
def generate_report(execution_id, report_type, name, description, user_id):
    """
    异步生成测试报告
    
    Args:
        execution_id: 测试执行ID
        report_type: 报告类型
        name: 报告名称
        description: 报告描述
        user_id: 用户ID
        
    Returns:
        dict: 操作结果
    """
    logger = logging.getLogger(__name__)
    logger.info(f"开始生成测试报告: execution_id={execution_id}, report_type={report_type}")
    
    try:
        from apps.users.models import User
        
        execution = TestExecution.objects.get(id=execution_id)
        user = User.objects.get(id=user_id)
        
        # 创建报告目录
        reports_dir = os.path.join(settings.MEDIA_ROOT, 'reports')
        os.makedirs(reports_dir, exist_ok=True)
        
        report_dir = os.path.join(reports_dir, f"report_{execution_id}_{timezone.now().strftime('%Y%m%d%H%M%S')}")
        os.makedirs(report_dir, exist_ok=True)
        
        # 获取测试结果
        results = TestResult.objects.filter(execution=execution)
        
        if report_type == 'allure':
            # 生成Allure报告所需的JSON文件
            allure_results_dir = os.path.join(report_dir, 'allure-results')
            os.makedirs(allure_results_dir, exist_ok=True)
            
            for i, result in enumerate(results):
                # 创建Allure测试结果JSON
                test_result = {
                    "name": result.case.name,
                    "status": result.status,
                    "statusDetails": {
                        "message": result.actual_result or "",
                        "trace": result.remarks or ""
                    },
                    "stage": "finished",
                    "steps": [],
                    "attachments": [],
                    "parameters": [],
                    "start": int(result.execution_time.timestamp() * 1000) if result.execution_time else int(timezone.now().timestamp() * 1000),
                    "stop": int(result.updated_at.timestamp() * 1000),
                    "labels": [
                        {
                            "name": "suite",
                            "value": execution.plan.name
                        },
                        {
                            "name": "testcase",
                            "value": result.case.name
                        }
                    ]
                }
                
                # 保存测试结果JSON
                with open(os.path.join(allure_results_dir, f"result_{i}.json"), 'w', encoding='utf-8') as f:
                    json.dump(test_result, f, ensure_ascii=False, indent=2)
            
            # 生成测试套件JSON
            test_suite = {
                "name": execution.plan.name,
                "children": [],
                "befores": [],
                "afters": []
            }
            
            # 保存测试套件JSON
            with open(os.path.join(allure_results_dir, "suite.json"), 'w', encoding='utf-8') as f:
                json.dump(test_suite, f, ensure_ascii=False, indent=2)
            
            # 调用Allure命令生成报告
            import subprocess
            allure_report_dir = os.path.join(report_dir, 'allure-report')
            try:
                subprocess.run(['allure', 'generate', allure_results_dir, '-o', allure_report_dir], check=True)
                file_path = allure_report_dir
            except (subprocess.SubprocessError, FileNotFoundError) as e:
                logger.error(f"生成Allure报告失败: {str(e)}")
                # 如果Allure命令失败，创建一个简单的HTML报告
                file_path = os.path.join(report_dir, 'report.html')
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(generate_html_report(execution, results))
                report_type = 'html'
        else:
            # 生成HTML报告
            file_path = os.path.join(report_dir, 'report.html')
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(generate_html_report(execution, results))
        
        # 创建报告记录
        report = Report.objects.create(
            name=name,
            description=description,
            execution=execution,
            report_type=report_type,
            file_path=file_path,
            creator=user
        )
        
        logger.info(f"测试报告生成成功: report_id={report.id}")
        return {
            'status': 'success',
            'report_id': report.id
        }
    except Exception as e:
        logger.error(f"生成测试报告失败: {str(e)}")
        return {
            'status': 'error',
            'message': str(e)
        }


def generate_html_report(execution, results):
    """
    生成HTML格式的测试报告
    
    Args:
        execution: 测试执行对象
        results: 测试结果列表
        
    Returns:
        str: HTML报告内容
    """
    # 统计数据
    total = results.count()
    passed = results.filter(status='passed').count()
    failed = results.filter(status='failed').count()
    blocked = results.filter(status='blocked').count()
    skipped = results.filter(status='skipped').count()
    pending = results.filter(status='pending').count()
    
    # 计算通过率
    pass_rate = round(passed / total * 100, 2) if total > 0 else 0
    
    # 生成HTML
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{execution.plan.name} - 测试报告</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                line-height: 1.6;
                margin: 0;
                padding: 20px;
                color: #333;
            }}
            .container {{
                max-width: 1200px;
                margin: 0 auto;
            }}
            h1, h2, h3 {{
                color: #2c3e50;
            }}
            .summary {{
                display: flex;
                flex-wrap: wrap;
                margin-bottom: 30px;
                background-color: #f8f9fa;
                padding: 20px;
                border-radius: 5px;
            }}
            .summary-item {{
                flex: 1;
                min-width: 150px;
                margin: 10px;
                text-align: center;
            }}
            .summary-value {{
                font-size: 24px;
                font-weight: bold;
                margin-bottom: 5px;
            }}
            .summary-label {{
                font-size: 14px;
                color: #666;
            }}
            .passed {{
                color: #28a745;
            }}
            .failed {{
                color: #dc3545;
            }}
            .blocked {{
                color: #fd7e14;
            }}
            .skipped {{
                color: #6c757d;
            }}
            .pending {{
                color: #17a2b8;
            }}
            table {{
                width: 100%;
                border-collapse: collapse;
                margin-bottom: 30px;
            }}
            th, td {{
                padding: 12px 15px;
                text-align: left;
                border-bottom: 1px solid #ddd;
            }}
            th {{
                background-color: #f8f9fa;
                font-weight: bold;
            }}
            tr:hover {{
                background-color: #f5f5f5;
            }}
            .status-badge {{
                display: inline-block;
                padding: 5px 10px;
                border-radius: 3px;
                font-size: 12px;
                font-weight: bold;
                text-transform: uppercase;
            }}
            .status-passed {{
                background-color: #d4edda;
                color: #155724;
            }}
            .status-failed {{
                background-color: #f8d7da;
                color: #721c24;
            }}
            .status-blocked {{
                background-color: #fff3cd;
                color: #856404;
            }}
            .status-skipped {{
                background-color: #e2e3e5;
                color: #383d41;
            }}
            .status-pending {{
                background-color: #d1ecf1;
                color: #0c5460;
            }}
            .info-section {{
                margin-bottom: 30px;
            }}
            .info-item {{
                display: flex;
                margin-bottom: 10px;
            }}
            .info-label {{
                font-weight: bold;
                width: 150px;
            }}
            .progress-bar {{
                height: 20px;
                background-color: #e9ecef;
                border-radius: 5px;
                margin-bottom: 20px;
                overflow: hidden;
            }}
            .progress {{
                height: 100%;
                background-color: #28a745;
                border-radius: 5px;
                width: {pass_rate}%;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>{execution.plan.name} - 测试报告</h1>
            
            <div class="info-section">
                <div class="info-item">
                    <div class="info-label">测试计划:</div>
                    <div>{execution.plan.name}</div>
                </div>
                <div class="info-item">
                    <div class="info-label">执行者:</div>
                    <div>{execution.executor.username if execution.executor else '-'}</div>
                </div>
                <div class="info-item">
                    <div class="info-label">开始时间:</div>
                    <div>{execution.start_time.strftime('%Y-%m-%d %H:%M:%S') if execution.start_time else '-'}</div>
                </div>
                <div class="info-item">
                    <div class="info-label">结束时间:</div>
                    <div>{execution.end_time.strftime('%Y-%m-%d %H:%M:%S') if execution.end_time else '-'}</div>
                </div>
                <div class="info-item">
                    <div class="info-label">状态:</div>
                    <div>{execution.get_status_display()}</div>
                </div>
            </div>
            
            <h2>测试结果统计</h2>
            
            <div class="progress-bar">
                <div class="progress"></div>
            </div>
            
            <div class="summary">
                <div class="summary-item">
                    <div class="summary-value">{total}</div>
                    <div class="summary-label">总用例数</div>
                </div>
                <div class="summary-item">
                    <div class="summary-value passed">{passed}</div>
                    <div class="summary-label">通过</div>
                </div>
                <div class="summary-item">
                    <div class="summary-value failed">{failed}</div>
                    <div class="summary-label">失败</div>
                </div>
                <div class="summary-item">
                    <div class="summary-value blocked">{blocked}</div>
                    <div class="summary-label">阻塞</div>
                </div>
                <div class="summary-item">
                    <div class="summary-value skipped">{skipped}</div>
                    <div class="summary-label">跳过</div>
                </div>
                <div class="summary-item">
                    <div class="summary-value pending">{pending}</div>
                    <div class="summary-label">待执行</div>
                </div>
                <div class="summary-item">
                    <div class="summary-value">{pass_rate}%</div>
                    <div class="summary-label">通过率</div>
                </div>
            </div>
            
            <h2>测试结果详情</h2>
            
            <table>
                <thead>
                    <tr>
                        <th>用例ID</th>
                        <th>用例名称</th>
                        <th>状态</th>
                        <th>实际结果</th>
                        <th>备注</th>
                        <th>执行时间</th>
                    </tr>
                </thead>
                <tbody>
    """
    
    # 添加测试结果行
    for result in results:
        status_class = f"status-{result.status}"
        status_display = result.get_status_display()
        execution_time = result.execution_time.strftime('%Y-%m-%d %H:%M:%S') if result.execution_time else '-'
        
        html += f"""
                    <tr>
                        <td>{result.case.id}</td>
                        <td>{result.case.name}</td>
                        <td><span class="status-badge {status_class}">{status_display}</span></td>
                        <td>{result.actual_result or '-'}</td>
                        <td>{result.remarks or '-'}</td>
                        <td>{execution_time}</td>
                    </tr>
        """
    
    # 完成HTML
    html += """
                </tbody>
            </table>
            
            <div style="text-align: center; margin-top: 50px; color: #777; font-size: 12px;">
                <p>由AiTestPlantForm自动生成</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    return html 