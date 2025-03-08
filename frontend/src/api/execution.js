import request from '@/utils/request'

/**
 * 获取测试执行列表
 * @param {Object} params - 查询参数
 * @returns {Promise} - 返回Promise对象
 */
export function getExecutionList(params) {
  return request({
    url: '/executions/',
    method: 'get',
    params
  })
}

/**
 * 获取测试执行详情
 * @param {Number} id - 测试执行ID
 * @returns {Promise} - 返回Promise对象
 */
export function getExecutionDetail(id) {
  return request({
    url: `/executions/${id}/`,
    method: 'get'
  })
}

/**
 * 创建测试执行
 * @param {Object} data - 测试执行数据
 * @returns {Promise} - 返回Promise对象
 */
export function createExecution(data) {
  return request({
    url: '/executions/',
    method: 'post',
    data
  })
}

/**
 * 更新测试执行
 * @param {Number} id - 测试执行ID
 * @param {Object} data - 测试执行数据
 * @returns {Promise} - 返回Promise对象
 */
export function updateExecution(id, data) {
  return request({
    url: `/executions/${id}/`,
    method: 'put',
    data
  })
}

/**
 * 删除测试执行
 * @param {Number} id - 测试执行ID
 * @returns {Promise} - 返回Promise对象
 */
export function deleteExecution(id) {
  return request({
    url: `/executions/${id}/`,
    method: 'delete'
  })
}

/**
 * 开始测试执行
 * @param {Number} id - 测试执行ID
 * @returns {Promise} - 返回Promise对象
 */
export function startExecution(id) {
  return request({
    url: `/executions/${id}/start/`,
    method: 'post'
  })
}

/**
 * 暂停测试执行
 * @param {Number} id - 测试执行ID
 * @returns {Promise} - 返回Promise对象
 */
export function pauseExecution(id) {
  return request({
    url: `/executions/${id}/pause/`,
    method: 'post'
  })
}

/**
 * 完成测试执行
 * @param {Number} id - 测试执行ID
 * @returns {Promise} - 返回Promise对象
 */
export function completeExecution(id) {
  return request({
    url: `/executions/${id}/complete/`,
    method: 'post'
  })
}

/**
 * 中止测试执行
 * @param {Number} id - 测试执行ID
 * @returns {Promise} - 返回Promise对象
 */
export function abortExecution(id) {
  return request({
    url: `/executions/${id}/abort/`,
    method: 'post'
  })
}

/**
 * 获取测试结果列表
 * @param {Object} params - 查询参数
 * @returns {Promise} - 返回Promise对象
 */
export function getResultList(params) {
  return request({
    url: '/results/',
    method: 'get',
    params
  })
}

/**
 * 获取测试执行的测试结果列表
 * @param {Number} executionId - 测试执行ID
 * @param {Object} params - 查询参数
 * @returns {Promise} - 返回Promise对象
 */
export function getExecutionResults(executionId, params) {
  return request({
    url: `/executions/${executionId}/results/`,
    method: 'get',
    params
  })
}

/**
 * 获取测试结果详情
 * @param {Number} id - 测试结果ID
 * @returns {Promise} - 返回Promise对象
 */
export function getResultDetail(id) {
  return request({
    url: `/results/${id}/`,
    method: 'get'
  })
}

/**
 * 更新测试结果
 * @param {Number} id - 测试结果ID
 * @param {Object} data - 测试结果数据
 * @returns {Promise} - 返回Promise对象
 */
export function updateResult(id, data) {
  return request({
    url: `/results/${id}/`,
    method: 'put',
    data
  })
}

/**
 * 批量更新测试结果
 * @param {Array} results - 测试结果数组
 * @returns {Promise} - 返回Promise对象
 */
export function batchUpdateResults(results) {
  return request({
    url: '/results/batch_update/',
    method: 'post',
    data: { results }
  })
}

/**
 * 从测试计划创建测试执行
 * @param {Number} planId - 测试计划ID
 * @param {Object} data - 附加数据
 * @returns {Promise} - 返回Promise对象
 */
export function createExecutionFromPlan(planId, data) {
  return request({
    url: `/testplans/${planId}/create_execution/`,
    method: 'post',
    data
  })
} 