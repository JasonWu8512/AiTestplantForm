"""
Celery任务包初始化

作者: AiTestPlantForm团队
创建日期: 2023-06-01
最后修改: 2023-06-10
"""

from .celery import app as celery_app

__all__ = ('celery_app',)
