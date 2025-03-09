/**
 * 测试计划API
 * 
 * 提供与测试计划相关的API调用
 */
import request from '@/utils/request'
import { TESTPLAN_API, getFullPath } from '@/utils/api-paths'

/**
 * 获取测试计划列表
 * @param {Object} params - 查询参数
 * @returns {Promise} - 返回请求Promise
 */
export function getTestPlans(params) {
  return request({
    url: getFullPath(TESTPLAN_API.LIST),
    method: 'get',
    params
  })
}

/**
 * 创建测试计划
 * @param {Object} data - 测试计划数据
 * @returns {Promise} - 返回请求Promise
 */
export function createTestPlan(data) {
  return request({
    url: getFullPath(TESTPLAN_API.LIST),
    method: 'post',
    data
  })
}

/**
 * 更新测试计划
 * @param {Number} id - 测试计划ID
 * @param {Object} data - 测试计划数据
 * @returns {Promise} - 返回请求Promise
 */
export function updateTestPlan(id, data) {
  return request({
    url: getFullPath(TESTPLAN_API.DETAIL(id)),
    method: 'put',
    data
  })
}

/**
 * 删除测试计划
 * @param {Number} id - 测试计划ID
 * @returns {Promise} - 返回请求Promise
 */
export function deleteTestPlan(id) {
  return request({
    url: getFullPath(TESTPLAN_API.DETAIL(id)),
    method: 'delete'
  })
}

/**
 * 获取测试计划详情
 * @param {Number} id - 测试计划ID
 * @returns {Promise} - 返回请求Promise
 */
export function getTestPlanById(id) {
  return request({
    url: getFullPath(TESTPLAN_API.DETAIL(id)),
    method: 'get'
  })
}

/**
 * 获取测试计划关联的测试用例
 * @param {Number} id - 测试计划ID
 * @param {Object} params - 分页参数
 * @returns {Promise} - 返回请求Promise
 */
export function getTestPlanCases(id, params) {
  return request({
    url: getFullPath(TESTPLAN_API.DETAIL(id)),
    method: 'get',
    params
  })
}

/**
 * 向测试计划添加测试用例
 * @param {Number} id - 测试计划ID
 * @param {Object} data - 包含case_ids数组的对象
 * @returns {Promise} - 返回请求Promise
 */
export function addCasesToTestPlan(id, data) {
  return request({
    url: getFullPath(TESTPLAN_API.ADD_CASES(id)),
    method: 'post',
    data
  })
}

/**
 * 从测试计划中移除测试用例
 * @param {Number} planId - 测试计划ID
 * @param {Number} caseId - 测试用例ID
 * @returns {Promise} - 返回请求Promise
 */
export function removeCaseFromTestPlan(planId, caseId) {
  return request({
    url: getFullPath(TESTPLAN_API.REMOVE_CASE(planId, caseId)),
    method: 'delete'
  })
}

/**
 * 重新排序测试计划中的测试用例
 * @param {Number} planId - 测试计划ID
 * @param {Array} caseOrders - 测试用例顺序数组，每个元素包含case_id和order
 * @returns {Promise} - 返回请求Promise
 */
export function reorderTestCases(planId, caseOrders) {
  return request({
    url: getFullPath(TESTPLAN_API.REORDER_CASES(planId)),
    method: 'put',
    data: {
      case_orders: caseOrders
    }
  })
} 