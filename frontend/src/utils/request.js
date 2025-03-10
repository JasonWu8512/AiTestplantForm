import axios from 'axios'
import { ElMessage } from 'element-plus'
import router from '@/router'
import errorMonitor from './error-monitor'
import feedback from './feedback'

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
    
    // 处理空参数
    if (config.params) {
      // 移除值为空字符串、null或undefined的参数
      Object.keys(config.params).forEach(key => {
        if (config.params[key] === '' || config.params[key] === null || config.params[key] === undefined) {
          delete config.params[key]
        }
      })
      console.log('处理后的请求参数:', config.params)
    }
    
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
    // 记录请求错误
    errorMonitor.logApiError(error, { stage: 'request' })
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
    // 记录API错误
    errorMonitor.logApiError(error, { 
      stage: 'response',
      url: error.config?.url,
      method: error.config?.method
    })
    
    // 使用用户反馈服务处理错误
    if (error.response) {
      const { status } = error.response
      
      // 处理特殊状态码
      if (status === 401) {
        // 清除token并跳转到登录页
        localStorage.removeItem('token')
        localStorage.removeItem('refresh_token')
        localStorage.removeItem('user')
        router.push('/login')
      }
    }
    
    // 显示错误消息
    feedback.showApiError(error)
    
    return Promise.reject(error)
  }
)

export default service 