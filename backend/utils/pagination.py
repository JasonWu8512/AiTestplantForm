"""
分页模块，定义自定义分页类

作者: AiTestPlantForm团队
创建日期: 2023-06-01
最后修改: 2023-06-10
"""

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

class StandardResultsSetPagination(PageNumberPagination):
    """
    标准分页类，提供默认分页功能
    """
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100
    
    def get_paginated_response(self, data):
        """
        自定义分页响应格式
        
        Args:
            data: 分页后的数据
            
        Returns:
            Response: 包含分页信息的响应
        """
        return Response({
            'count': self.page.paginator.count,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'current_page': self.page.number,
            'total_pages': self.page.paginator.num_pages,
            'page_size': self.page_size,
            'results': data
        })

class LargeResultsSetPagination(PageNumberPagination):
    """
    大结果集分页类，用于需要显示更多数据的场景
    """
    page_size = 50
    page_size_query_param = 'page_size'
    max_page_size = 500
    
    def get_paginated_response(self, data):
        """
        自定义分页响应格式
        
        Args:
            data: 分页后的数据
            
        Returns:
            Response: 包含分页信息的响应
        """
        return Response({
            'count': self.page.paginator.count,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'current_page': self.page.number,
            'total_pages': self.page.paginator.num_pages,
            'page_size': self.page_size,
            'results': data
        })

class SmallResultsSetPagination(PageNumberPagination):
    """
    小结果集分页类，用于需要显示较少数据的场景
    """
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 20
    
    def get_paginated_response(self, data):
        """
        自定义分页响应格式
        
        Args:
            data: 分页后的数据
            
        Returns:
            Response: 包含分页信息的响应
        """
        return Response({
            'count': self.page.paginator.count,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'current_page': self.page.number,
            'total_pages': self.page.paginator.num_pages,
            'page_size': self.page_size,
            'results': data
        }) 