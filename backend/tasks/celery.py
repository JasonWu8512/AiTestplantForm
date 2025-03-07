"""
Celery配置模块

作者: AiTestPlantForm团队
创建日期: 2023-06-01
最后修改: 2023-06-10
"""

import os
from celery import Celery

# 设置Django设置模块
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# 创建Celery应用
app = Celery('aitestplantform')

# 使用Django设置模块配置Celery
app.config_from_object('django.conf:settings', namespace='CELERY')

# 自动发现任务
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    """
    调试任务，用于测试Celery是否正常工作
    
    Returns:
        str: 包含请求ID的调试信息
    """
    print(f'Request: {self.request!r}')
    return f'Request: {self.request!r}' 