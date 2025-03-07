"""
中间件模块，定义自定义中间件

作者: AiTestPlantForm团队
创建日期: 2023-06-01
最后修改: 2023-06-10
"""

import time
import json
import logging
from django.utils.deprecation import MiddlewareMixin
from django.http import JsonResponse
from django.conf import settings

logger = logging.getLogger('django')

class RequestLogMiddleware(MiddlewareMixin):
    """
    请求日志中间件，记录请求和响应信息
    """
    
    def process_request(self, request):
        """
        处理请求
        
        Args:
            request: HTTP请求对象
        """
        # 记录请求开始时间
        request.start_time = time.time()
        
        # 记录请求信息
        if settings.DEBUG:
            request_data = None
            if request.method in ['POST', 'PUT', 'PATCH']:
                if request.content_type == 'application/json':
                    try:
                        request_data = json.loads(request.body)
                    except:
                        request_data = 'Invalid JSON body'
                else:
                    request_data = dict(request.POST)
            
            logger.info(f"Request: {request.method} {request.path} - Data: {request_data}")
    
    def process_response(self, request, response):
        """
        处理响应
        
        Args:
            request: HTTP请求对象
            response: HTTP响应对象
            
        Returns:
            response: HTTP响应对象
        """
        # 计算请求处理时间
        if hasattr(request, 'start_time'):
            duration = time.time() - request.start_time
            response['X-Request-Duration'] = str(round(duration * 1000, 2)) + 'ms'
            
            # 记录响应信息
            if settings.DEBUG:
                response_data = None
                if response.get('Content-Type') == 'application/json':
                    try:
                        response_data = json.loads(response.content.decode('utf-8'))
                    except:
                        response_data = 'Invalid JSON response'
                
                logger.info(f"Response: {request.method} {request.path} - Status: {response.status_code} - Duration: {round(duration * 1000, 2)}ms")
        
        return response

class ExceptionMiddleware(MiddlewareMixin):
    """
    异常处理中间件，捕获未处理的异常并返回友好的错误信息
    """
    
    def process_exception(self, request, exception):
        """
        处理异常
        
        Args:
            request: HTTP请求对象
            exception: 异常对象
            
        Returns:
            JsonResponse: 包含错误信息的JSON响应
        """
        # 记录异常信息
        logger.error(f"Unhandled Exception: {request.method} {request.path}", exc_info=exception)
        
        # 在生产环境中返回友好的错误信息
        if not settings.DEBUG:
            return JsonResponse({
                'error': '服务器内部错误，请稍后再试',
                'status_code': 500
            }, status=500)
        
        # 在开发环境中返回详细的错误信息
        return JsonResponse({
            'error': str(exception),
            'type': exception.__class__.__name__,
            'status_code': 500
        }, status=500)

class CorsMiddleware(MiddlewareMixin):
    """
    CORS中间件，处理跨域请求
    """
    
    def process_response(self, request, response):
        """
        处理响应，添加CORS头
        
        Args:
            request: HTTP请求对象
            response: HTTP响应对象
            
        Returns:
            response: HTTP响应对象
        """
        # 添加CORS头
        response['Access-Control-Allow-Origin'] = settings.CORS_ORIGIN_ALLOW_ALL and '*' or settings.CORS_ORIGIN_WHITELIST
        response['Access-Control-Allow-Methods'] = 'GET, POST, PUT, PATCH, DELETE, OPTIONS'
        response['Access-Control-Allow-Headers'] = 'Content-Type, Authorization, X-Requested-With'
        response['Access-Control-Allow-Credentials'] = 'true'
        
        return response 