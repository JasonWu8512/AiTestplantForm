/**
 * 用户反馈服务
 * 
 * 提供统一的用户反馈机制，包括消息提示、加载状态、确认对话框等
 * 基于Element Plus组件库，但提供更一致和增强的用户体验
 */

import { ElMessage, ElMessageBox, ElLoading, ElNotification } from 'element-plus'
import errorMonitor from './error-monitor'

// 消息类型
export const MessageType = {
  SUCCESS: 'success',
  WARNING: 'warning',
  INFO: 'info',
  ERROR: 'error'
}

// 默认配置
const defaultConfig = {
  // 消息显示时间（毫秒）
  messageDuration: 3000,
  // 是否显示关闭按钮
  showClose: true,
  // 加载状态文本
  loadingText: '加载中...',
  // 加载状态背景色
  loadingBackground: 'rgba(0, 0, 0, 0.7)',
  // 确认按钮文本
  confirmButtonText: '确定',
  // 取消按钮文本
  cancelButtonText: '取消',
  // 是否在消息中显示图标
  showIcon: true
}

/**
 * 显示消息提示
 * @param {string} message - 消息内容
 * @param {string} type - 消息类型
 * @param {Object} options - 配置选项
 */
export function showMessage(message, type = MessageType.INFO, options = {}) {
  ElMessage({
    message,
    type,
    duration: options.duration || defaultConfig.messageDuration,
    showClose: options.showClose !== undefined ? options.showClose : defaultConfig.showClose,
    grouping: options.grouping !== undefined ? options.grouping : true,
    ...options
  })
}

/**
 * 显示成功消息
 * @param {string} message - 消息内容
 * @param {Object} options - 配置选项
 */
export function showSuccess(message, options = {}) {
  showMessage(message, MessageType.SUCCESS, options)
}

/**
 * 显示警告消息
 * @param {string} message - 消息内容
 * @param {Object} options - 配置选项
 */
export function showWarning(message, options = {}) {
  showMessage(message, MessageType.WARNING, options)
}

/**
 * 显示信息消息
 * @param {string} message - 消息内容
 * @param {Object} options - 配置选项
 */
export function showInfo(message, options = {}) {
  showMessage(message, MessageType.INFO, options)
}

/**
 * 显示错误消息
 * @param {string} message - 消息内容
 * @param {Object} options - 配置选项
 * @param {Error} error - 错误对象（可选，用于错误监控）
 */
export function showError(message, options = {}, error = null) {
  showMessage(message, MessageType.ERROR, {
    duration: 5000, // 错误消息显示时间更长
    ...options
  })
  
  // 如果提供了错误对象，记录到错误监控
  if (error) {
    errorMonitor.logError(error, errorMonitor.ErrorTypes.CUSTOM_ERROR, errorMonitor.ErrorLevels.ERROR, {
      userMessage: message,
      ...options
    })
  }
}

/**
 * 显示API错误消息
 * @param {Error} error - 错误对象
 * @param {string} defaultMessage - 默认错误消息
 */
export function showApiError(error, defaultMessage = '操作失败') {
  let errorMessage = defaultMessage
  
  if (error.response) {
    const { status, data } = error.response
    
    // 根据状态码和响应数据生成更具体的错误消息
    switch (status) {
      case 400:
        if (typeof data === 'object' && data !== null) {
          const errorMessages = []
          for (const key in data) {
            if (Array.isArray(data[key])) {
              errorMessages.push(`${key}: ${data[key].join(', ')}`)
            } else if (typeof data[key] === 'string') {
              errorMessages.push(`${key}: ${data[key]}`)
            }
          }
          if (errorMessages.length > 0) {
            errorMessage = errorMessages.join('\n')
          }
        } else if (data.detail) {
          errorMessage = `请求参数错误: ${data.detail}`
        } else if (data.message) {
          errorMessage = `请求参数错误: ${data.message}`
        } else {
          errorMessage = '请求参数错误'
        }
        break
      case 401:
        errorMessage = '登录已过期，请重新登录'
        break
      case 403:
        errorMessage = '没有权限执行此操作'
        break
      case 404:
        errorMessage = '请求的资源不存在'
        break
      case 500:
        errorMessage = '服务器内部错误，请稍后重试'
        break
      default:
        errorMessage = `请求失败 (${status}): ${data.message || data.detail || defaultMessage}`
    }
  } else if (error.request) {
    errorMessage = '网络连接失败，请检查您的网络连接'
  } else {
    errorMessage = `操作失败: ${error.message || defaultMessage}`
  }
  
  showError(errorMessage, {}, error)
  
  // 记录API错误
  errorMonitor.logApiError(error, {
    defaultMessage,
    displayedMessage: errorMessage
  })
}

// 加载实例
let loadingInstance = null

/**
 * 显示全屏加载状态
 * @param {string} text - 加载文本
 * @param {Object} options - 配置选项
 * @returns {Object} - 加载实例
 */
export function showLoading(text = defaultConfig.loadingText, options = {}) {
  // 如果已经有加载实例，先关闭
  if (loadingInstance) {
    loadingInstance.close()
  }
  
  loadingInstance = ElLoading.service({
    lock: true,
    text: text,
    background: options.background || defaultConfig.loadingBackground,
    ...options
  })
  
  return loadingInstance
}

/**
 * 隐藏全屏加载状态
 */
export function hideLoading() {
  if (loadingInstance) {
    loadingInstance.close()
    loadingInstance = null
  }
}

/**
 * 显示确认对话框
 * @param {string} message - 消息内容
 * @param {string} title - 标题
 * @param {Object} options - 配置选项
 * @returns {Promise} - 确认结果
 */
export function showConfirm(message, title = '确认', options = {}) {
  return ElMessageBox.confirm(
    message,
    title,
    {
      confirmButtonText: options.confirmButtonText || defaultConfig.confirmButtonText,
      cancelButtonText: options.cancelButtonText || defaultConfig.cancelButtonText,
      type: options.type || 'warning',
      distinguishCancelAndClose: true,
      ...options
    }
  )
}

/**
 * 显示提示对话框
 * @param {string} message - 消息内容
 * @param {string} title - 标题
 * @param {Object} options - 配置选项
 * @returns {Promise} - 确认结果
 */
export function showAlert(message, title = '提示', options = {}) {
  return ElMessageBox.alert(
    message,
    title,
    {
      confirmButtonText: options.confirmButtonText || defaultConfig.confirmButtonText,
      type: options.type || 'info',
      ...options
    }
  )
}

/**
 * 显示输入对话框
 * @param {string} message - 消息内容
 * @param {string} title - 标题
 * @param {Object} options - 配置选项
 * @returns {Promise} - 输入结果
 */
export function showPrompt(message, title = '请输入', options = {}) {
  return ElMessageBox.prompt(
    message,
    title,
    {
      confirmButtonText: options.confirmButtonText || defaultConfig.confirmButtonText,
      cancelButtonText: options.cancelButtonText || defaultConfig.cancelButtonText,
      inputPattern: options.inputPattern,
      inputErrorMessage: options.inputErrorMessage || '输入格式不正确',
      ...options
    }
  )
}

/**
 * 显示通知
 * @param {string} title - 标题
 * @param {string} message - 消息内容
 * @param {string} type - 通知类型
 * @param {Object} options - 配置选项
 */
export function showNotification(title, message, type = MessageType.INFO, options = {}) {
  ElNotification({
    title,
    message,
    type,
    duration: options.duration || 4500,
    showClose: options.showClose !== undefined ? options.showClose : true,
    ...options
  })
}

/**
 * 显示操作反馈
 * @param {boolean} success - 是否成功
 * @param {string} successMessage - 成功消息
 * @param {string|Error} errorOrMessage - 错误对象或错误消息
 * @param {Object} options - 配置选项
 */
export function showOperationFeedback(success, successMessage, errorOrMessage, options = {}) {
  if (success) {
    showSuccess(successMessage, options)
  } else {
    if (errorOrMessage instanceof Error) {
      showApiError(errorOrMessage, options.defaultErrorMessage || '操作失败')
    } else {
      showError(errorOrMessage || options.defaultErrorMessage || '操作失败', options)
    }
  }
}

/**
 * 更新默认配置
 * @param {Object} newConfig - 新配置
 */
export function updateConfig(newConfig) {
  Object.assign(defaultConfig, newConfig)
}

// 导出用户反馈服务
export default {
  showMessage,
  showSuccess,
  showWarning,
  showInfo,
  showError,
  showApiError,
  showLoading,
  hideLoading,
  showConfirm,
  showAlert,
  showPrompt,
  showNotification,
  showOperationFeedback,
  updateConfig,
  MessageType
} 