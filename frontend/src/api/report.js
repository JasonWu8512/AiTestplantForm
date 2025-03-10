/**
 * 测试报告API
 * 
 * 提供与测试报告相关的API调用
 */
import request from '@/utils/request'
import { REPORT_API, getFullPath } from '@/utils/api-paths'

/**
 * 获取测试报告列表
 * @param {Object} params - 查询参数
 * @returns {Promise} - 返回请求Promise
 */
export function getReports(params) {
  return request({
    url: getFullPath(REPORT_API.LIST),
    method: 'get',
    params
  })
}

/**
 * 获取测试报告详情
 * @param {Number} id - 报告ID
 * @returns {Promise} - 返回请求Promise
 */
export function getReportDetail(id) {
  return request({
    url: getFullPath(REPORT_API.DETAIL(id)),
    method: 'get'
  })
}

/**
 * 生成测试报告
 * @param {Object} data - 报告数据
 * @returns {Promise} - 返回请求Promise
 */
export function generateReport(data) {
  return request({
    url: getFullPath(REPORT_API.GENERATE),
    method: 'post',
    data
  })
}

/**
 * 下载测试报告
 * @param {Number} id - 报告ID
 * @returns {Promise} - 返回请求Promise
 */
export function downloadReport(id) {
  return request({
    url: getFullPath(REPORT_API.DOWNLOAD(id)),
    method: 'get',
    responseType: 'blob'
  })
}

/**
 * 查看测试报告
 * @param {Number} id - 报告ID
 * @returns {Promise} - 返回请求Promise
 */
export function viewReport(id) {
  return request({
    url: getFullPath(REPORT_API.VIEW(id)),
    method: 'get'
  })
}

/**
 * 删除测试报告
 * @param {Number} id - 报告ID
 * @returns {Promise} - 返回请求Promise
 */
export function deleteReport(id) {
  return request({
    url: getFullPath(REPORT_API.DETAIL(id)),
    method: 'delete'
  })
} 