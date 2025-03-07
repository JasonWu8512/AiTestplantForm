"""
Celery任务定义模块

作者: AiTestPlantForm团队
创建日期: 2023-06-01
最后修改: 2023-06-10
"""

from celery import shared_task

@shared_task
def sample_task(name):
    """
    示例任务
    
    Args:
        name (str): 任务名称
        
    Returns:
        str: 任务完成消息
    """
    return f'Hello {name}! Task completed.' 