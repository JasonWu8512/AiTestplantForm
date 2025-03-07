"""
异常处理模块，定义自定义异常和异常处理器

作者: AiTestPlantForm团队
创建日期: 2023-06-01
最后修改: 2023-06-10
"""

from rest_framework.views import exception_handler
from rest_framework.exceptions import APIException
from rest_framework import status

class ServiceUnavailable(APIException):
    """
    服务不可用异常
    """
    status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    default_detail = '服务暂时不可用，请稍后再试。'
    default_code = 'service_unavailable'

class ResourceNotFound(APIException):
    """
    资源未找到异常
    """
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = '请求的资源不存在。'
    default_code = 'resource_not_found'

class InvalidOperation(APIException):
    """
    无效操作异常
    """
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = '无效的操作。'
    default_code = 'invalid_operation'

def custom_exception_handler(exc, context):
    """
    自定义异常处理器
    
    Args:
        exc: 异常对象
        context: 异常上下文
        
    Returns:
        Response: 包含错误详情的响应对象
    """
    # 调用DRF默认的异常处理器
    response = exception_handler(exc, context)
    
    # 如果响应已经由DRF处理，则添加自定义信息
    if response is not None:
        # 添加更多错误信息
        response.data['status_code'] = response.status_code
        
        # 如果有错误代码，则添加
        if hasattr(exc, 'default_code'):
            response.data['code'] = exc.default_code
            
        # 添加请求信息
        request = context.get('request')
        if request:
            response.data['path'] = request.path
    
    return response 