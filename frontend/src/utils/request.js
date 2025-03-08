import axios from 'axios'
import { ElMessage } from 'element-plus'
import router from '@/router'

// 创建axios实例
const service = axios.create({
  baseURL: '/api', // API的基础URL，确保与后端API路径匹配
  timeout: 15000 // 请求超时时间
})

console.log('Axios实例配置:', {
  baseURL: service.defaults.baseURL,
  timeout: service.defaults.timeout
})

// 请求拦截器
service.interceptors.request.use(
  config => {
    // 从localStorage获取token
    const token = localStorage.getItem('token')
    console.log(`请求: ${config.method.toUpperCase()} ${config.url}`)
    console.log('完整请求URL:', `${config.baseURL}${config.url}`)
    console.log('请求配置:', {
      url: config.url,
      method: config.method,
      baseURL: config.baseURL,
      headers: config.headers,
      params: config.params,
      data: config.data
    })
    
    if (token) {
      console.log('添加认证令牌到请求头:', token.substring(0, 15) + '...')
      // 设置请求头
      config.headers['Authorization'] = `Bearer ${token}`
    } else {
      console.log('请求未携带认证令牌')
    }
    return config
  },
  error => {
    console.error('请求错误:', error)
    return Promise.reject(error)
  }
)

// 响应拦截器
service.interceptors.response.use(
  response => {
    console.log('请求成功:', response.config.url)
    console.log('响应数据:', response.data)
    return response.data  // 直接返回响应数据，简化调用
  },
  error => {
    // 处理错误响应
    if (error.response) {
      const { status, data } = error.response
      console.error(`请求失败: ${error.config.url}, 状态码: ${status}`)
      console.error('错误响应数据:', data)
      
      // 处理常见错误
      switch (status) {
        case 400:
          // 显示详细的错误信息
          if (typeof data === 'object' && data !== null) {
            const errorMessages = [];
            for (const key in data) {
              if (Array.isArray(data[key])) {
                errorMessages.push(`${key}: ${data[key].join(', ')}`);
              } else if (typeof data[key] === 'string') {
                errorMessages.push(`${key}: ${data[key]}`);
              }
            }
            if (errorMessages.length > 0) {
              ElMessage.error(errorMessages.join('\n'));
            } else {
              ElMessage.error('请求参数错误');
            }
          } else {
            ElMessage.error(data.detail || '请求参数错误');
          }
          break;
        case 401:
          ElMessage.error('登录已过期，请重新登录')
          // 清除token并跳转到登录页
          localStorage.removeItem('token')
          localStorage.removeItem('refresh_token')
          localStorage.removeItem('user')
          router.push('/login')
          break
        case 403:
          ElMessage.error('没有权限执行此操作')
          break
        case 404:
          ElMessage.error('请求的资源不存在')
          break
        case 500:
          ElMessage.error('服务器内部错误')
          break
        default:
          ElMessage.error(`请求失败: ${error.message}`)
      }
    } else {
      ElMessage.error(`网络错误: ${error.message}`)
    }
    
    console.error('响应错误:', error.response ? error.response.data : error.message)
    return Promise.reject(error)
  }
)

export default service 