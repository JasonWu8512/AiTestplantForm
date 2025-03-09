/**
 * 测试用例API
 * 
 * 提供与测试用例和项目相关的API调用
 */
import request from '@/utils/request'
import { TESTCASE_API, PROJECT_API, getFullPath, buildApiPath } from '@/utils/api-paths'

/**
 * 获取项目列表
 * @param {Object} params - 查询参数
 * @returns {Promise} - 返回请求Promise
 */
export function getProjects(params) {
  console.log('获取项目列表，参数:', params)
  return request({
    url: getFullPath(PROJECT_API.LIST),
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
    url: getFullPath(PROJECT_API.LIST),
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
    url: getFullPath(PROJECT_API.DETAIL(id)),
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
    url: getFullPath(PROJECT_API.DETAIL(id)),
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
    url: getFullPath(PROJECT_API.DETAIL(id)),
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
    url: getFullPath(TESTCASE_API.BY_PROJECT(id)),
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
    url: getFullPath(TESTCASE_API.LIST),
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
    url: getFullPath(TESTCASE_API.LIST),
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
    url: getFullPath(TESTCASE_API.DETAIL(id)),
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
    url: getFullPath(TESTCASE_API.DETAIL(id)),
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
    url: getFullPath(TESTCASE_API.DETAIL(id)),
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
    url: getFullPath(TESTCASE_API.IMPORT),
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
    url: getFullPath(TESTCASE_API.EXPORT),
    method: 'get',
    params,
    responseType: 'blob' // 指定响应类型为blob
  })
}

/**
 * 批量更新测试用例
 * @param {Array} testcases - 测试用例数组
 * @returns {Promise} - 返回请求Promise
 */
export function batchUpdateTestCases(testcases) {
  return request({
    url: getFullPath(TESTCASE_API.BATCH_UPDATE),
    method: 'post',
    data: { testcases }
  })
}

/**
 * 批量删除测试用例
 * @param {Array} ids - 测试用例ID数组
 * @returns {Promise} - 返回请求Promise
 */
export function batchDeleteTestCases(ids) {
  return request({
    url: getFullPath(TESTCASE_API.BATCH_DELETE),
    method: 'post',
    data: { ids }
  })
}

/**
 * 复制测试用例
 * @param {Number} id - 测试用例ID
 * @param {Object} data - 复制选项
 * @returns {Promise} - 返回请求Promise
 */
export function copyTestCase(id, data) {
  return request({
    url: getFullPath(TESTCASE_API.COPY(id)),
    method: 'post',
    data
  })
}

/**
 * 获取测试用例步骤
 * @param {Number} id - 测试用例ID
 * @returns {Promise} - 返回请求Promise
 */
export function getTestCaseSteps(id) {
  return request({
    url: getFullPath(TESTCASE_API.STEPS(id)),
    method: 'get'
  })
}

/**
 * 更新测试用例步骤
 * @param {Number} id - 测试用例ID
 * @param {Array} steps - 步骤数组
 * @returns {Promise} - 返回请求Promise
 */
export function updateTestCaseSteps(id, steps) {
  return request({
    url: getFullPath(TESTCASE_API.STEPS(id)),
    method: 'put',
    data: { steps }
  })
}

/**
 * 获取测试用例附件
 * @param {Number} id - 测试用例ID
 * @returns {Promise} - 返回请求Promise
 */
export function getTestCaseAttachments(id) {
  return request({
    url: getFullPath(TESTCASE_API.ATTACHMENTS(id)),
    method: 'get'
  })
}

/**
 * 添加测试用例附件
 * @param {Number} id - 测试用例ID
 * @param {FormData} formData - 包含文件的表单数据
 * @returns {Promise} - 返回请求Promise
 */
export function addTestCaseAttachment(id, formData) {
  return request({
    url: getFullPath(TESTCASE_API.ADD_ATTACHMENT(id)),
    method: 'post',
    data: formData,
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  })
}

/**
 * 删除测试用例附件
 * @param {Number} id - 测试用例ID
 * @param {Number} attachmentId - 附件ID
 * @returns {Promise} - 返回请求Promise
 */
export function removeTestCaseAttachment(id, attachmentId) {
  return request({
    url: getFullPath(TESTCASE_API.REMOVE_ATTACHMENT(id, attachmentId)),
    method: 'delete'
  })
} 