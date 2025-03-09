/**
 * Swagger API生成工具
 * 
 * 从Swagger/OpenAPI文档自动生成API调用代码
 * 支持生成API路径常量和API调用函数
 */

/**
 * 从Swagger/OpenAPI文档生成API路径常量
 * @param {Object} swaggerDoc - Swagger/OpenAPI文档对象
 * @param {Object} options - 配置选项
 * @returns {Object} - 生成的API路径常量对象
 */
export function generateApiPaths(swaggerDoc, options = {}) {
  const {
    groupByTag = true,
    camelCaseKeys = true,
    includeDescription = true
  } = options;
  
  const paths = swaggerDoc.paths || {};
  const apiPaths = {};
  
  // 按标签分组
  if (groupByTag) {
    // 初始化标签组
    const tags = swaggerDoc.tags || [];
    tags.forEach(tag => {
      apiPaths[formatKey(tag.name, camelCaseKeys)] = {
        _description: tag.description || ''
      };
    });
    
    // 处理每个路径
    Object.entries(paths).forEach(([path, methods]) => {
      Object.entries(methods).forEach(([method, operation]) => {
        const tag = operation.tags && operation.tags[0];
        if (tag) {
          const tagKey = formatKey(tag, camelCaseKeys);
          if (!apiPaths[tagKey]) {
            apiPaths[tagKey] = { _description: '' };
          }
          
          const operationId = operation.operationId || `${method}${formatKey(path, true)}`;
          const key = formatKey(operationId, camelCaseKeys);
          
          // 检查是否有路径参数
          const hasPathParams = path.includes('{');
          
          if (hasPathParams) {
            // 创建函数形式的路径
            apiPaths[tagKey][key] = createPathFunction(path);
          } else {
            // 创建静态路径
            apiPaths[tagKey][key] = path;
          }
          
          // 添加描述
          if (includeDescription && operation.summary) {
            apiPaths[tagKey][`${key}_description`] = operation.summary;
          }
        }
      });
    });
  } else {
    // 不按标签分组，直接处理每个路径
    Object.entries(paths).forEach(([path, methods]) => {
      Object.entries(methods).forEach(([method, operation]) => {
        const operationId = operation.operationId || `${method}${formatKey(path, true)}`;
        const key = formatKey(operationId, camelCaseKeys);
        
        // 检查是否有路径参数
        const hasPathParams = path.includes('{');
        
        if (hasPathParams) {
          // 创建函数形式的路径
          apiPaths[key] = createPathFunction(path);
        } else {
          // 创建静态路径
          apiPaths[key] = path;
        }
        
        // 添加描述
        if (includeDescription && operation.summary) {
          apiPaths[`${key}_description`] = operation.summary;
        }
      });
    });
  }
  
  return apiPaths;
}

/**
 * 从Swagger/OpenAPI文档生成API调用函数
 * @param {Object} swaggerDoc - Swagger/OpenAPI文档对象
 * @param {Object} options - 配置选项
 * @returns {Object} - 生成的API调用函数对象
 */
export function generateApiFunctions(swaggerDoc, options = {}) {
  const {
    groupByTag = true,
    camelCaseKeys = true,
    includeComments = true,
    requestModule = 'request',
    apiPathsModule = 'apiPaths',
    useApiPaths = true
  } = options;
  
  const paths = swaggerDoc.paths || {};
  const apiFunctions = {};
  
  // 按标签分组
  if (groupByTag) {
    // 初始化标签组
    const tags = swaggerDoc.tags || [];
    tags.forEach(tag => {
      apiFunctions[formatKey(tag.name, camelCaseKeys)] = {};
    });
    
    // 处理每个路径
    Object.entries(paths).forEach(([path, methods]) => {
      Object.entries(methods).forEach(([method, operation]) => {
        const tag = operation.tags && operation.tags[0];
        if (tag) {
          const tagKey = formatKey(tag, camelCaseKeys);
          if (!apiFunctions[tagKey]) {
            apiFunctions[tagKey] = {};
          }
          
          const operationId = operation.operationId || `${method}${formatKey(path, true)}`;
          const key = formatKey(operationId, camelCaseKeys);
          
          // 生成函数代码
          apiFunctions[tagKey][key] = generateFunctionCode(
            path,
            method,
            operation,
            {
              includeComments,
              requestModule,
              apiPathsModule,
              useApiPaths,
              tagKey,
              operationKey: key
            }
          );
        }
      });
    });
  } else {
    // 不按标签分组，直接处理每个路径
    Object.entries(paths).forEach(([path, methods]) => {
      Object.entries(methods).forEach(([method, operation]) => {
        const operationId = operation.operationId || `${method}${formatKey(path, true)}`;
        const key = formatKey(operationId, camelCaseKeys);
        
        // 生成函数代码
        apiFunctions[key] = generateFunctionCode(
          path,
          method,
          operation,
          {
            includeComments,
            requestModule,
            apiPathsModule,
            useApiPaths
          }
        );
      });
    });
  }
  
  return apiFunctions;
}

/**
 * 生成API调用函数代码
 * @param {string} path - API路径
 * @param {string} method - HTTP方法
 * @param {Object} operation - 操作对象
 * @param {Object} options - 配置选项
 * @returns {string} - 生成的函数代码
 */
function generateFunctionCode(path, method, operation, options) {
  const {
    includeComments = true,
    requestModule = 'request',
    apiPathsModule = 'apiPaths',
    useApiPaths = true,
    tagKey,
    operationKey
  } = options;
  
  // 提取参数
  const pathParams = [];
  const queryParams = [];
  const bodyParam = null;
  
  if (operation.parameters) {
    operation.parameters.forEach(param => {
      if (param.in === 'path') {
        pathParams.push(param);
      } else if (param.in === 'query') {
        queryParams.push(param);
      }
    });
  }
  
  // 检查是否有请求体
  let hasRequestBody = false;
  if (operation.requestBody) {
    hasRequestBody = true;
  }
  
  // 生成函数参数
  const functionParams = [];
  
  // 添加路径参数
  pathParams.forEach(param => {
    functionParams.push(param.name);
  });
  
  // 添加查询参数（如果有多个，合并为一个对象）
  if (queryParams.length > 0) {
    functionParams.push('params');
  }
  
  // 添加请求体参数
  if (hasRequestBody) {
    functionParams.push('data');
  }
  
  // 生成函数注释
  let functionComment = '';
  if (includeComments) {
    functionComment = `/**
 * ${operation.summary || ''}
 * ${operation.description || ''}
${pathParams.map(param => ` * @param {${mapSwaggerTypeToJs(param.schema)}} ${param.name} - ${param.description || ''}`).join('\n')}
${queryParams.length > 0 ? ` * @param {Object} params - 查询参数` : ''}
${hasRequestBody ? ` * @param {Object} data - 请求数据` : ''}
 * @returns {Promise} - 返回请求Promise
 */`;
  }
  
  // 生成请求配置
  let requestConfig = '';
  
  if (useApiPaths && tagKey && operationKey) {
    // 使用API路径常量
    requestConfig = `{
    url: getFullPath(${apiPathsModule}.${tagKey.toUpperCase()}_API.${operationKey.toUpperCase()}${pathParams.length > 0 ? `(${pathParams.join(', ')})` : ''}),
    method: '${method}',
${queryParams.length > 0 ? '    params,\n' : ''}${hasRequestBody ? '    data,\n' : ''}  }`;
  } else {
    // 直接使用路径字符串
    let urlString = path;
    
    // 替换路径参数
    pathParams.forEach(param => {
      urlString = urlString.replace(`{${param.name}}`, `\${${param.name}}`);
    });
    
    requestConfig = `{
    url: \`${urlString}\`,
    method: '${method}',
${queryParams.length > 0 ? '    params,\n' : ''}${hasRequestBody ? '    data,\n' : ''}  }`;
  }
  
  // 生成完整函数代码
  return `${functionComment}
export function ${operationKey}(${functionParams.join(', ')}) {
  return ${requestModule}(${requestConfig});
}`;
}

/**
 * 创建路径函数代码
 * @param {string} path - API路径
 * @returns {Function} - 路径函数
 */
function createPathFunction(path) {
  // 提取路径参数
  const pathParams = [];
  const regex = /{([^}]+)}/g;
  let match;
  
  while ((match = regex.exec(path)) !== null) {
    pathParams.push(match[1]);
  }
  
  // 创建函数
  const fn = new Function(...pathParams, `
    return \`${path.replace(/{([^}]+)}/g, '${$1}')}\`;
  `);
  
  return fn;
}

/**
 * 格式化键名
 * @param {string} key - 原始键名
 * @param {boolean} camelCase - 是否转换为驼峰命名
 * @returns {string} - 格式化后的键名
 */
function formatKey(key, camelCase = true) {
  // 移除非法字符
  let formattedKey = key.replace(/[^\w\s-]/g, '');
  
  // 替换空格和连字符
  formattedKey = formattedKey.replace(/[-\s]+(.)?/g, (_, c) => c ? c.toUpperCase() : '');
  
  // 转换为驼峰命名
  if (camelCase) {
    formattedKey = formattedKey.charAt(0).toLowerCase() + formattedKey.slice(1);
  }
  
  return formattedKey;
}

/**
 * 将Swagger类型映射为JavaScript类型
 * @param {Object} schema - Swagger类型模式
 * @returns {string} - JavaScript类型
 */
function mapSwaggerTypeToJs(schema) {
  if (!schema) return 'any';
  
  switch (schema.type) {
    case 'integer':
    case 'number':
      return 'Number';
    case 'string':
      if (schema.format === 'date' || schema.format === 'date-time') {
        return 'Date';
      }
      return 'String';
    case 'boolean':
      return 'Boolean';
    case 'array':
      return 'Array';
    case 'object':
      return 'Object';
    default:
      return 'any';
  }
}

/**
 * 从Swagger/OpenAPI URL获取文档并生成API代码
 * @param {string} url - Swagger/OpenAPI文档URL
 * @param {Object} options - 配置选项
 * @returns {Promise<Object>} - 生成的API代码
 */
export async function generateApiFromUrl(url, options = {}) {
  try {
    const response = await fetch(url);
    const swaggerDoc = await response.json();
    
    return {
      paths: generateApiPaths(swaggerDoc, options),
      functions: generateApiFunctions(swaggerDoc, options)
    };
  } catch (error) {
    console.error('获取Swagger文档失败:', error);
    throw error;
  }
}

/**
 * 生成完整的API模块代码
 * @param {Object} swaggerDoc - Swagger/OpenAPI文档对象
 * @param {Object} options - 配置选项
 * @returns {string} - 生成的API模块代码
 */
export function generateApiModuleCode(swaggerDoc, options = {}) {
  const {
    moduleName = 'api',
    requestImport = "import request from '@/utils/request'",
    apiPathsImport = "import { getFullPath } from '@/utils/api-paths'",
    includeComments = true
  } = options;
  
  // 生成API路径常量
  const apiPaths = generateApiPaths(swaggerDoc, options);
  
  // 生成API函数
  const apiFunctions = generateApiFunctions(swaggerDoc, {
    ...options,
    apiPathsModule: moduleName
  });
  
  // 生成API路径常量代码
  let apiPathsCode = '';
  Object.entries(apiPaths).forEach(([tagKey, paths]) => {
    if (includeComments && paths._description) {
      apiPathsCode += `// ${paths._description}\n`;
    }
    
    apiPathsCode += `export const ${tagKey.toUpperCase()}_API = {\n`;
    
    Object.entries(paths).forEach(([key, value]) => {
      if (key === '_description') return;
      
      if (key.endsWith('_description')) return;
      
      const description = paths[`${key}_description`];
      if (includeComments && description) {
        apiPathsCode += `  // ${description}\n`;
      }
      
      if (typeof value === 'function') {
        // 函数形式的路径
        const params = value.toString()
          .match(/\(([^)]*)\)/)[1]
          .split(',')
          .map(p => p.trim())
          .filter(p => p);
        
        apiPathsCode += `  ${key.toUpperCase()}: (${params.join(', ')}) => \`${value.toString().match(/return `([^`]+)`/)[1]}\`,\n`;
      } else {
        // 静态路径
        apiPathsCode += `  ${key.toUpperCase()}: '${value}',\n`;
      }
    });
    
    apiPathsCode += `};\n\n`;
  });
  
  // 生成API函数代码
  let apiFunctionsCode = '';
  Object.entries(apiFunctions).forEach(([tagKey, functions]) => {
    Object.entries(functions).forEach(([key, code]) => {
      apiFunctionsCode += `${code}\n\n`;
    });
  });
  
  // 生成导出代码
  let exportsCode = 'export default {\n';
  Object.entries(apiFunctions).forEach(([tagKey, functions]) => {
    Object.keys(functions).forEach(key => {
      exportsCode += `  ${key},\n`;
    });
  });
  exportsCode += '};\n';
  
  // 生成完整模块代码
  return `/**
 * ${moduleName} API
 * 
 * 自动生成的API模块
 * 生成时间: ${new Date().toISOString()}
 */

${requestImport}
${apiPathsImport}

// API路径常量
${apiPathsCode}

// API函数
${apiFunctionsCode}

// 导出所有函数
${exportsCode}`;
}

export default {
  generateApiPaths,
  generateApiFunctions,
  generateApiFromUrl,
  generateApiModuleCode
}; 