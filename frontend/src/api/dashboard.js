/**
 * Dashboard API
 * 
 * 提供与Dashboard相关的API调用
 */
import request from '@/utils/request'

/**
 * 获取系统概览数据
 * @returns {Promise} - 返回请求Promise
 */
export function getSummary() {
  return request({
    url: '/dashboard/summary/',
    method: 'get'
  })
}

/**
 * 获取统计数据
 * @param {Object} params - 查询参数，如项目ID
 * @returns {Promise} - 返回请求Promise
 */
export function getStatistics(params) {
  return request({
    url: '/dashboard/statistics/',
    method: 'get',
    params
  })
} 