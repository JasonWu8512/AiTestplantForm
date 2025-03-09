/**
 * 错误监控服务
 * 
 * 用于收集和处理前端错误，包括JS运行时错误、API请求错误、Vue组件错误等
 * 支持错误日志记录、错误上报和错误分析
 */

// 错误类型枚举
export const ErrorTypes = {
  JS_ERROR: 'js_error',         // JavaScript运行时错误
  API_ERROR: 'api_error',       // API请求错误
  VUE_ERROR: 'vue_error',       // Vue组件错误
  RESOURCE_ERROR: 'resource_error', // 资源加载错误
  PROMISE_ERROR: 'promise_error',   // Promise未捕获错误
  CUSTOM_ERROR: 'custom_error'      // 自定义错误
}

// 错误级别枚举
export const ErrorLevels = {
  INFO: 'info',       // 信息
  WARNING: 'warning', // 警告
  ERROR: 'error',     // 错误
  FATAL: 'fatal'      // 致命错误
}

// 错误监控配置
const config = {
  // 是否启用错误监控
  enabled: true,
  // 是否在控制台输出错误信息
  consoleOutput: true,
  // 是否上报错误到服务器
  reportToServer: true,
  // 错误上报的URL
  reportUrl: '/api/logs/error',
  // 错误上报的批量大小
  batchSize: 10,
  // 错误上报的时间间隔（毫秒）
  reportInterval: 5000,
  // 是否忽略相同错误
  ignoreDuplicates: true,
  // 最大错误存储数量
  maxErrorCount: 100,
  // 采样率（0-1之间的数值，1表示100%采集）
  samplingRate: 1
}

// 错误缓存
let errorCache = []
// 错误上报定时器
let reportTimer = null
// 错误哈希表（用于去重）
const errorHashMap = new Map()

/**
 * 生成错误唯一标识
 * @param {Object} error - 错误对象
 * @returns {string} - 错误唯一标识
 */
function generateErrorId(error) {
  const { type, message, url, line, column } = error
  return `${type}:${message}:${url}:${line}:${column}`
}

/**
 * 格式化错误信息
 * @param {Error|Object} error - 错误对象
 * @param {string} type - 错误类型
 * @param {string} level - 错误级别
 * @param {Object} extra - 额外信息
 * @returns {Object} - 格式化后的错误信息
 */
function formatError(error, type = ErrorTypes.JS_ERROR, level = ErrorLevels.ERROR, extra = {}) {
  const now = new Date()
  const baseInfo = {
    type,
    level,
    timestamp: now.toISOString(),
    url: window.location.href,
    userAgent: navigator.userAgent,
    ...extra
  }

  // 处理不同类型的错误
  if (error instanceof Error) {
    return {
      ...baseInfo,
      name: error.name,
      message: error.message,
      stack: error.stack,
      line: error.lineNumber,
      column: error.columnNumber
    }
  } else if (typeof error === 'string') {
    return {
      ...baseInfo,
      message: error
    }
  } else {
    return {
      ...baseInfo,
      ...error
    }
  }
}

/**
 * 记录错误
 * @param {Error|Object|string} error - 错误对象或错误信息
 * @param {string} type - 错误类型
 * @param {string} level - 错误级别
 * @param {Object} extra - 额外信息
 */
export function logError(error, type = ErrorTypes.JS_ERROR, level = ErrorLevels.ERROR, extra = {}) {
  if (!config.enabled) return

  const formattedError = formatError(error, type, level, extra)
  
  // 控制台输出
  if (config.consoleOutput) {
    console.group(`[错误监控] ${formattedError.type} - ${formattedError.level}`)
    console.error(formattedError.message)
    console.info('详细信息:', formattedError)
    console.groupEnd()
  }

  // 采样处理
  if (Math.random() > config.samplingRate) return

  // 错误去重
  if (config.ignoreDuplicates) {
    const errorId = generateErrorId(formattedError)
    if (errorHashMap.has(errorId)) {
      const existing = errorHashMap.get(errorId)
      existing.count = (existing.count || 1) + 1
      existing.lastOccurrence = formattedError.timestamp
      return
    }
    errorHashMap.set(generateErrorId(formattedError), { ...formattedError, count: 1 })
  }

  // 添加到错误缓存
  errorCache.push(formattedError)
  
  // 限制错误缓存大小
  if (errorCache.length > config.maxErrorCount) {
    errorCache = errorCache.slice(-config.maxErrorCount)
  }

  // 触发错误上报
  if (config.reportToServer) {
    scheduleErrorReport()
  }
}

/**
 * 记录API错误
 * @param {Object} error - 错误对象
 * @param {Object} requestInfo - 请求信息
 */
export function logApiError(error, requestInfo = {}) {
  const { config, response, message } = error
  const apiInfo = {
    url: config?.url,
    method: config?.method,
    params: config?.params,
    data: config?.data,
    status: response?.status,
    statusText: response?.statusText,
    responseData: response?.data,
    message
  }
  
  logError(error, ErrorTypes.API_ERROR, ErrorLevels.ERROR, { 
    ...requestInfo,
    apiInfo
  })
}

/**
 * 记录Vue组件错误
 * @param {Error} error - 错误对象
 * @param {Object} vm - Vue实例
 * @param {string} info - 错误信息
 */
export function logVueError(error, vm, info) {
  const componentInfo = {
    componentName: vm?.$options?.name || 'AnonymousComponent',
    propsData: vm?.$options?.propsData,
    info
  }
  
  logError(error, ErrorTypes.VUE_ERROR, ErrorLevels.ERROR, componentInfo)
}

/**
 * 记录资源加载错误
 * @param {Event} event - 错误事件
 */
export function logResourceError(event) {
  const target = event.target || event.srcElement
  const resourceInfo = {
    tagName: target.tagName,
    src: target.src || target.href,
    type: target.type,
    id: target.id
  }
  
  logError(
    { message: `资源加载失败: ${resourceInfo.src}` },
    ErrorTypes.RESOURCE_ERROR,
    ErrorLevels.ERROR,
    resourceInfo
  )
}

/**
 * 安排错误上报
 */
function scheduleErrorReport() {
  if (reportTimer) return
  
  reportTimer = setTimeout(() => {
    reportErrors()
    reportTimer = null
  }, config.reportInterval)
}

/**
 * 上报错误到服务器
 */
async function reportErrors() {
  if (errorCache.length === 0) return
  
  // 批量上报
  const batch = errorCache.splice(0, config.batchSize)
  
  try {
    // 这里可以替换为实际的上报API
    const response = await fetch(config.reportUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        errors: batch,
        timestamp: new Date().toISOString(),
        url: window.location.href,
        userAgent: navigator.userAgent
      })
    })
    
    if (!response.ok) {
      console.error('[错误监控] 错误上报失败:', response.statusText)
      // 失败时将错误放回缓存
      errorCache = [...batch, ...errorCache]
    }
  } catch (e) {
    console.error('[错误监控] 错误上报异常:', e)
    // 异常时将错误放回缓存
    errorCache = [...batch, ...errorCache]
  }
  
  // 如果还有错误，继续安排上报
  if (errorCache.length > 0) {
    scheduleErrorReport()
  }
}

/**
 * 获取当前缓存的错误
 * @returns {Array} - 错误缓存
 */
export function getErrorCache() {
  return [...errorCache]
}

/**
 * 清空错误缓存
 */
export function clearErrorCache() {
  errorCache = []
  errorHashMap.clear()
}

/**
 * 更新错误监控配置
 * @param {Object} newConfig - 新配置
 */
export function updateConfig(newConfig) {
  Object.assign(config, newConfig)
}

/**
 * 初始化全局错误监听
 */
export function initErrorMonitor() {
  if (!config.enabled) return
  
  // 监听全局JavaScript错误
  window.addEventListener('error', (event) => {
    // 区分资源加载错误和JavaScript运行时错误
    if (event.target && (event.target.tagName === 'SCRIPT' || 
                         event.target.tagName === 'LINK' || 
                         event.target.tagName === 'IMG')) {
      logResourceError(event)
    } else {
      logError({
        message: event.message,
        filename: event.filename,
        line: event.lineno,
        column: event.colno,
        stack: event.error?.stack
      }, ErrorTypes.JS_ERROR, ErrorLevels.ERROR)
    }
    
    // 不阻止默认行为
    return false
  }, true)
  
  // 监听未捕获的Promise错误
  window.addEventListener('unhandledrejection', (event) => {
    logError({
      message: event.reason?.message || '未处理的Promise拒绝',
      stack: event.reason?.stack,
      reason: event.reason
    }, ErrorTypes.PROMISE_ERROR, ErrorLevels.ERROR)
    
    // 不阻止默认行为
    return false
  })
  
  console.info('[错误监控] 已初始化全局错误监听')
}

// 导出错误监控服务
export default {
  logError,
  logApiError,
  logVueError,
  logResourceError,
  getErrorCache,
  clearErrorCache,
  updateConfig,
  initErrorMonitor,
  ErrorTypes,
  ErrorLevels
} 