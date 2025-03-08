"""
Django配置包初始化文件

作者: AiTestPlantForm团队
创建日期: 2023-06-01
最后修改: 2023-06-10
"""

# 导入celery应用
from tasks.celery import app as celery_app

__all__ = ['celery_app']
