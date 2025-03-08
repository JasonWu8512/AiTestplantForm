"""
测试用例应用配置

作者: AiTestPlantForm团队
创建日期: 2023-06-01
最后修改: 2023-06-10
"""

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class TestcasesConfig(AppConfig):
    """
    测试用例应用配置类
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.testcases'
    verbose_name = _('测试用例管理') 