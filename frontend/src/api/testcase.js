/**
 * 测试用例API
 * 
 * 提供与测试用例和项目相关的API调用
 */
import request from '@/utils/request'

/**
 * 获取项目列表
 * @param {Object} params - 查询参数
 * @returns {Promise} - 返回请求Promise
 */
export function getProjects(params) {
  console.log('获取项目列表，参数:', params)
  return request({
    url: '/testcases/projects/',
    method: 'get',
    params
  })
}

/**
 * 创建项目
 * @param {Object} data - 项目数据
 * @returns {Promise} - 返回请求Promise
 */
export function createProject(data) {
  return request({
    url: '/testcases/projects/',
    method: 'post',
    data
  })
}

/**
 * 更新项目
 * @param {Number} id - 项目ID
 * @param {Object} data - 项目数据
 * @returns {Promise} - 返回请求Promise
 */
export function updateProject(id, data) {
  return request({
    url: `/testcases/projects/${id}/`,
    method: 'put',
    data
  })
}

/**
 * 删除项目
 * @param {Number} id - 项目ID
 * @returns {Promise} - 返回请求Promise
 */
export function deleteProject(id) {
  return request({
    url: `/testcases/projects/${id}/`,
    method: 'delete'
  })
}

/**
 * 获取项目详情
 * @param {Number} id - 项目ID
 * @returns {Promise} - 返回请求Promise
 */
export function getProject(id) {
  return request({
    url: `/testcases/projects/${id}/`,
    method: 'get'
  })
}

/**
 * 获取项目下的测试用例
 * @param {Number} id - 项目ID
 * @returns {Promise} - 返回请求Promise
 */
export function getProjectTestCases(id) {
  return request({
    url: `/testcases/projects/${id}/test_cases/`,
    method: 'get'
  })
}

/**
 * 获取测试用例列表
 * @param {Object} params - 查询参数
 * @returns {Promise} - 返回请求Promise
 */
export function getTestCases(params) {
  return request({
    url: '/testcases/testcases/',
    method: 'get',
    params
  })
}

/**
 * 创建测试用例
 * @param {Object} data - 测试用例数据
 * @returns {Promise} - 返回请求Promise
 */
export function createTestCase(data) {
  return request({
    url: '/testcases/testcases/',
    method: 'post',
    data
  })
}

/**
 * 更新测试用例
 * @param {Number} id - 测试用例ID
 * @param {Object} data - 测试用例数据
 * @returns {Promise} - 返回请求Promise
 */
export function updateTestCase(id, data) {
  return request({
    url: `/testcases/testcases/${id}/`,
    method: 'put',
    data
  })
}

/**
 * 删除测试用例
 * @param {Number} id - 测试用例ID
 * @returns {Promise} - 返回请求Promise
 */
export function deleteTestCase(id) {
  return request({
    url: `/testcases/testcases/${id}/`,
    method: 'delete'
  })
}

/**
 * 获取测试用例详情
 * @param {Number} id - 测试用例ID
 * @returns {Promise} - 返回请求Promise
 */
export function getTestCase(id) {
  return request({
    url: `/testcases/testcases/${id}/`,
    method: 'get'
  })
}

/**
 * 导入测试用例
 * @param {Object} data - 包含文件和项目ID的FormData对象
 * @returns {Promise} - 返回请求Promise
 */
export function importTestCases(data) {
  return request({
    url: '/testcases/testcases/import_cases/',
    method: 'post',
    data,
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  })
}

/**
 * 导出测试用例
 * @param {Object} params - 查询参数，用于过滤要导出的测试用例
 * @returns {Promise} - 返回请求Promise
 */
export function exportTestCases(params) {
  return request({
    url: '/testcases/testcases/export_cases/',
    method: 'get',
    params,
    responseType: 'blob' // 指定响应类型为blob
  })
} 