/**
 * API路径管理工具
 * 
 * 本文件集中管理所有API路径，确保前端API调用路径与后端路由配置一致
 * 使用常量定义API路径，避免硬编码和路径不一致问题
 */

// 基础路径前缀
export const API_PREFIX = ''

// 用户相关API路径
export const USER_API = {
  LOGIN: '/users/login/',
  LOGOUT: '/users/logout/',
  PROFILE: '/users/profile/',
  LIST: '/users/',
  DETAIL: (id) => `/users/${id}/`,
}

// 项目相关API路径
export const PROJECT_API = {
  LIST: '/projects/',
  DETAIL: (id) => `/projects/${id}/`,
}

// 测试用例相关API路径
export const TESTCASE_API = {
  LIST: '/testcases/',
  DETAIL: (id) => `/testcases/${id}/`,
  IMPORT: '/testcases/import/',
  EXPORT: '/testcases/export/',
  BY_PROJECT: (id) => `/projects/${id}/testcases/`,
  BATCH_UPDATE: '/testcases/batch_update/',
  BATCH_DELETE: '/testcases/batch_delete/',
  COPY: (id) => `/testcases/${id}/copy/`,
  STEPS: (id) => `/testcases/${id}/steps/`,
}

// 测试计划相关API路径
export const TESTPLAN_API = {
  LIST: '/testplans/',
  DETAIL: (id) => `/testplans/${id}/`,
  ADD_CASES: (id) => `/testplans/${id}/add_test_cases/`,
  REMOVE_CASE: (id, caseId) => `/testplans/${id}/remove_test_case/?case_id=${caseId}`,
  REORDER_CASES: (id) => `/testplans/${id}/reorder_test_cases/`,
  CREATE_EXECUTION: (id) => `/testplans/${id}/create_execution/`,
}

// 测试执行相关API路径
export const EXECUTION_API = {
  LIST: '/executions/',
  DETAIL: (id) => `/executions/${id}/`,
  START: (id) => `/executions/${id}/start/`,
  PAUSE: (id) => `/executions/${id}/pause/`,
  COMPLETE: (id) => `/executions/${id}/complete/`,
  ABORT: (id) => `/executions/${id}/abort/`,
  RESULTS: (id) => `/executions/${id}/results/`,
}

// 测试结果相关API路径
export const RESULT_API = {
  LIST: '/results/',
  DETAIL: (id) => `/results/${id}/`,
  BATCH_UPDATE: '/results/batch_update/',
}

// Dashboard相关API路径
export const DASHBOARD_API = {
  SUMMARY: '/dashboard/summary/',
  STATISTICS: '/dashboard/statistics/',
}

/**
 * 获取完整的API路径
 * @param {string} path - API路径
 * @returns {string} - 完整的API路径
 */
export function getFullPath(path) {
  // 直接返回路径，因为axios已经配置了baseURL: '/api'
  return path
}

/**
 * 构建API路径
 * @param {string} basePath - 基础路径
 * @param {Object} pathParams - 路径参数
 * @param {Object} queryParams - 查询参数
 * @returns {string} - 完整的API路径
 */
export function buildApiPath(basePath, pathParams = {}, queryParams = {}) {
  let path = basePath;
  
  // 替换路径参数
  Object.keys(pathParams).forEach(key => {
    path = path.replace(`:${key}`, pathParams[key]);
  });
  
  // 添加查询参数
  if (Object.keys(queryParams).length > 0) {
    const queryString = new URLSearchParams(queryParams).toString();
    path = `${path}?${queryString}`;
  }
  
  return getFullPath(path);
}

export default {
  USER_API,
  PROJECT_API,
  TESTCASE_API,
  TESTPLAN_API,
  EXECUTION_API,
  RESULT_API,
  DASHBOARD_API,
  getFullPath,
  buildApiPath,
} 