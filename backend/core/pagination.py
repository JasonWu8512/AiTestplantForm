"""
分页模块，提供自定义分页类

作者: AiTestPlantForm团队
创建日期: 2023-06-01
最后修改: 2023-06-10
"""

from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination

class StandardResultsSetPagination(PageNumberPagination):
    """
    标准分页类，使用页码进行分页
    """
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class LargeResultsSetPagination(PageNumberPagination):
    """
    大结果集分页类，用于处理大量数据
    """
    page_size = 50
    page_size_query_param = 'page_size'
    max_page_size = 500

class CustomLimitOffsetPagination(LimitOffsetPagination):
    """
    自定义限制偏移分页类
    """
    default_limit = 10
    max_limit = 100
    limit_query_param = 'limit'
    offset_query_param = 'offset' 