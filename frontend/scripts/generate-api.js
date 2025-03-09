#!/usr/bin/env node

/**
 * API代码生成工具
 * 
 * 从Swagger/OpenAPI文档生成API代码
 * 使用方法: node generate-api.js [options]
 */

const fs = require('fs');
const path = require('path');
const https = require('https');
const http = require('http');
const { URL } = require('url');

// 命令行参数
const args = process.argv.slice(2);
const options = parseArgs(args);

// 默认配置
const config = {
  swaggerUrl: options.url || 'http://localhost:8000/swagger/?format=json',
  outputDir: options.output || path.resolve(__dirname, '../src/api'),
  apiPathsFile: options.paths || path.resolve(__dirname, '../src/utils/api-paths.js'),
  groupByTag: options.groupByTag !== 'false',
  camelCaseKeys: options.camelCase !== 'false',
  includeComments: options.comments !== 'false',
  overwrite: options.overwrite === 'true',
  modules: options.modules ? options.modules.split(',') : [],
  excludeModules: options.exclude ? options.exclude.split(',') : [],
  requestModule: options.requestModule || '@/utils/request',
  apiPathsModule: options.apiPathsModule || '@/utils/api-paths',
};

// 显示帮助信息
if (options.help) {
  showHelp();
  process.exit(0);
}

// 显示版本信息
if (options.version) {
  console.log('API代码生成工具 v1.0.0');
  process.exit(0);
}

// 主函数
async function main() {
  try {
    console.log('开始生成API代码...');
    console.log(`Swagger文档URL: ${config.swaggerUrl}`);
    console.log(`输出目录: ${config.outputDir}`);
    
    // 获取Swagger文档
    const swaggerDoc = await fetchSwaggerDoc(config.swaggerUrl);
    console.log(`成功获取Swagger文档，包含 ${Object.keys(swaggerDoc.paths || {}).length} 个API路径`);
    
    // 生成API路径常量
    if (config.modules.length === 0) {
      // 生成所有模块
      await generateAllModules(swaggerDoc);
    } else {
      // 生成指定模块
      await generateSpecificModules(swaggerDoc, config.modules);
    }
    
    console.log('API代码生成完成！');
  } catch (error) {
    console.error('生成API代码失败:', error);
    process.exit(1);
  }
}

// 解析命令行参数
function parseArgs(args) {
  const options = {};
  
  for (let i = 0; i < args.length; i++) {
    const arg = args[i];
    
    if (arg.startsWith('--')) {
      const [key, value] = arg.slice(2).split('=');
      options[key] = value || true;
    } else if (arg.startsWith('-')) {
      const key = arg.slice(1);
      
      if (i + 1 < args.length && !args[i + 1].startsWith('-')) {
        options[key] = args[++i];
      } else {
        options[key] = true;
      }
    }
  }
  
  return options;
}

// 显示帮助信息
function showHelp() {
  console.log(`
API代码生成工具

使用方法: node generate-api.js [options]

选项:
  -h, --help                显示帮助信息
  -v, --version             显示版本信息
  -u, --url=URL             指定Swagger文档URL
  -o, --output=DIR          指定输出目录
  -p, --paths=FILE          指定API路径文件
  -m, --modules=MOD1,MOD2   指定要生成的模块
  -e, --exclude=MOD1,MOD2   指定要排除的模块
  --groupByTag=true|false   是否按标签分组
  --camelCase=true|false    是否使用驼峰命名
  --comments=true|false     是否包含注释
  --overwrite=true|false    是否覆盖现有文件
  --requestModule=MODULE    指定请求模块
  --apiPathsModule=MODULE   指定API路径模块

示例:
  node generate-api.js --url=http://localhost:8000/swagger/?format=json
  node generate-api.js -m users,testcases -o ../src/api
  `);
}

// 获取Swagger文档
async function fetchSwaggerDoc(url) {
  return new Promise((resolve, reject) => {
    const parsedUrl = new URL(url);
    const client = parsedUrl.protocol === 'https:' ? https : http;
    
    const options = {
      hostname: parsedUrl.hostname,
      port: parsedUrl.port || (parsedUrl.protocol === 'https:' ? 443 : 80),
      path: parsedUrl.pathname + parsedUrl.search,
      method: 'GET',
      headers: {
        'Accept': 'application/json'
      }
    };
    
    const req = client.request(options, (res) => {
      let data = '';
      
      res.on('data', (chunk) => {
        data += chunk;
      });
      
      res.on('end', () => {
        if (res.statusCode >= 200 && res.statusCode < 300) {
          try {
            const swaggerDoc = JSON.parse(data);
            resolve(swaggerDoc);
          } catch (error) {
            reject(new Error(`解析Swagger文档失败: ${error.message}`));
          }
        } else {
          reject(new Error(`获取Swagger文档失败: ${res.statusCode} ${res.statusMessage}`));
        }
      });
    });
    
    req.on('error', (error) => {
      reject(new Error(`请求Swagger文档失败: ${error.message}`));
    });
    
    req.end();
  });
}

// 生成所有模块
async function generateAllModules(swaggerDoc) {
  // 获取所有标签
  const tags = swaggerDoc.tags || [];
  
  // 过滤排除的模块
  const filteredTags = tags.filter(tag => !config.excludeModules.includes(tag.name));
  
  console.log(`将生成 ${filteredTags.length} 个模块的API代码`);
  
  // 生成API路径常量
  await generateApiPaths(swaggerDoc, filteredTags);
  
  // 生成每个模块的API代码
  for (const tag of filteredTags) {
    await generateModuleCode(swaggerDoc, tag.name);
  }
}

// 生成指定模块
async function generateSpecificModules(swaggerDoc, modules) {
  console.log(`将生成 ${modules.length} 个指定模块的API代码`);
  
  // 获取所有标签
  const tags = swaggerDoc.tags || [];
  
  // 过滤指定的模块
  const filteredTags = tags.filter(tag => modules.includes(tag.name));
  
  if (filteredTags.length === 0) {
    console.warn('未找到指定的模块，请检查模块名称是否正确');
    return;
  }
  
  // 生成API路径常量
  await generateApiPaths(swaggerDoc, filteredTags);
  
  // 生成每个模块的API代码
  for (const tag of filteredTags) {
    await generateModuleCode(swaggerDoc, tag.name);
  }
}

// 生成API路径常量
async function generateApiPaths(swaggerDoc, tags) {
  // 提取所有路径
  const paths = swaggerDoc.paths || {};
  
  // 按标签分组
  const apiPaths = {};
  
  // 初始化标签组
  tags.forEach(tag => {
    const tagKey = formatKey(tag.name, config.camelCaseKeys);
    apiPaths[tagKey] = {
      _description: tag.description || ''
    };
  });
  
  // 处理每个路径
  Object.entries(paths).forEach(([path, methods]) => {
    Object.entries(methods).forEach(([method, operation]) => {
      const tag = operation.tags && operation.tags[0];
      if (tag && tags.some(t => t.name === tag)) {
        const tagKey = formatKey(tag, config.camelCaseKeys);
        if (!apiPaths[tagKey]) {
          apiPaths[tagKey] = { _description: '' };
        }
        
        const operationId = operation.operationId || `${method}${formatKey(path, true)}`;
        const key = formatKey(operationId, config.camelCaseKeys);
        
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
        if (config.includeComments && operation.summary) {
          apiPaths[tagKey][`${key}_description`] = operation.summary;
        }
      }
    });
  });
  
  // 生成API路径常量代码
  let apiPathsCode = '';
  
  // 导入语句
  apiPathsCode += `/**
 * API路径常量
 * 
 * 自动生成的API路径常量
 * 生成时间: ${new Date().toISOString()}
 */

// 基础路径前缀
export const API_PREFIX = '/api';

// API版本
export const API_VERSION = 'v1';

`;
  
  // 生成每个标签的API路径常量
  Object.entries(apiPaths).forEach(([tagKey, paths]) => {
    if (config.includeComments && paths._description) {
      apiPathsCode += `// ${paths._description}\n`;
    }
    
    apiPathsCode += `export const ${tagKey.toUpperCase()}_API = {\n`;
    
    Object.entries(paths).forEach(([key, value]) => {
      if (key === '_description') return;
      
      if (key.endsWith('_description')) return;
      
      const description = paths[`${key}_description`];
      if (config.includeComments && description) {
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
  
  // 生成getFullPath函数
  apiPathsCode += `/**
 * 获取完整的API路径
 * @param {string} path - API路径
 * @param {Object} options - 配置选项
 * @param {boolean} options.addPrefix - 是否添加API前缀，默认为true
 * @param {boolean} options.addVersion - 是否添加API版本，默认为false
 * @param {Object} options.params - URL参数对象
 * @returns {string} - 完整的API路径
 */
export function getFullPath(path, options = {}) {
  const {
    addPrefix = true,
    addVersion = false,
    params = null
  } = options;
  
  // 如果路径已经包含API前缀，则不再添加
  let fullPath = path;
  if (addPrefix && !path.startsWith(API_PREFIX)) {
    fullPath = \`\${API_PREFIX}\${path}\`;
  }
  
  // 添加API版本
  if (addVersion && !fullPath.includes(\`/\${API_VERSION}/\`)) {
    // 在API前缀后添加版本
    const prefixEndIndex = addPrefix ? API_PREFIX.length : 0;
    fullPath = \`\${fullPath.substring(0, prefixEndIndex)}/\${API_VERSION}\${fullPath.substring(prefixEndIndex)}\`;
  }
  
  // 添加URL参数
  if (params && typeof params === 'object') {
    const queryParams = new URLSearchParams();
    Object.entries(params).forEach(([key, value]) => {
      if (value !== undefined && value !== null) {
        queryParams.append(key, value);
      }
    });
    
    const queryString = queryParams.toString();
    if (queryString) {
      fullPath = \`\${fullPath}\${fullPath.includes('?') ? '&' : '?'}\${queryString}\`;
    }
  }
  
  return fullPath;
}

/**
 * 构建API路径
 * @param {string} basePath - 基础路径
 * @param {Object} pathParams - 路径参数
 * @param {Object} queryParams - 查询参数
 * @returns {string} - 完整的API路径
 */
export function buildApiPath(basePath, pathParams = {}, queryParams = {}) {
  // 替换路径参数
  let path = basePath;
  Object.entries(pathParams).forEach(([key, value]) => {
    path = path.replace(\`:\${key}\`, encodeURIComponent(value));
  });
  
  return getFullPath(path, { params: queryParams });
}

/**
 * 获取API模块
 * @param {string} moduleName - 模块名称
 * @returns {Object} - API模块对象
 */
export function getApiModule(moduleName) {
  const modules = {
${Object.keys(apiPaths).map(tagKey => `    ${tagKey}: ${tagKey.toUpperCase()}_API`).join(',\n')}
  };
  
  return modules[moduleName.toLowerCase()] || null;
}

export default {
  API_PREFIX,
  API_VERSION,
${Object.keys(apiPaths).map(tagKey => `  ${tagKey.toUpperCase()}_API`).join(',\n')},
  getFullPath,
  buildApiPath,
  getApiModule
};`;
  
  // 写入文件
  const apiPathsFilePath = config.apiPathsFile;
  const apiPathsDir = path.dirname(apiPathsFilePath);
  
  // 创建目录
  if (!fs.existsSync(apiPathsDir)) {
    fs.mkdirSync(apiPathsDir, { recursive: true });
  }
  
  // 检查文件是否存在
  if (fs.existsSync(apiPathsFilePath) && !config.overwrite) {
    console.log(`API路径文件已存在: ${apiPathsFilePath}`);
    console.log('使用 --overwrite=true 参数覆盖现有文件');
  } else {
    fs.writeFileSync(apiPathsFilePath, apiPathsCode);
    console.log(`API路径常量已生成: ${apiPathsFilePath}`);
  }
}

// 生成模块代码
async function generateModuleCode(swaggerDoc, tagName) {
  // 提取所有路径
  const paths = swaggerDoc.paths || {};
  
  // 过滤指定标签的路径
  const tagPaths = {};
  
  Object.entries(paths).forEach(([path, methods]) => {
    Object.entries(methods).forEach(([method, operation]) => {
      const tag = operation.tags && operation.tags[0];
      if (tag === tagName) {
        if (!tagPaths[path]) {
          tagPaths[path] = {};
        }
        tagPaths[path][method] = operation;
      }
    });
  });
  
  if (Object.keys(tagPaths).length === 0) {
    console.warn(`未找到标签为 ${tagName} 的API路径`);
    return;
  }
  
  // 生成API函数代码
  const tagKey = formatKey(tagName, config.camelCaseKeys);
  const moduleName = tagKey;
  
  let moduleCode = `/**
 * ${tagName} API
 * 
 * 自动生成的API模块
 * 生成时间: ${new Date().toISOString()}
 */

import request from '${config.requestModule}';
import { ${tagKey.toUpperCase()}_API, getFullPath } from '${config.apiPathsModule}';

`;
  
  // 生成每个API函数
  Object.entries(tagPaths).forEach(([path, methods]) => {
    Object.entries(methods).forEach(([method, operation]) => {
      const operationId = operation.operationId || `${method}${formatKey(path, true)}`;
      const key = formatKey(operationId, config.camelCaseKeys);
      
      // 提取参数
      const pathParams = [];
      const queryParams = [];
      
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
      if (config.includeComments) {
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
      const requestConfig = `{
    url: getFullPath(${tagKey.toUpperCase()}_API.${key.toUpperCase()}${pathParams.length > 0 ? `(${pathParams.join(', ')})` : ''}),
    method: '${method}',
${queryParams.length > 0 ? '    params,\n' : ''}${hasRequestBody ? '    data,\n' : ''}  }`;
      
      // 生成完整函数代码
      moduleCode += `${functionComment}
export function ${key}(${functionParams.join(', ')}) {
  return request(${requestConfig});
}

`;
    });
  });
  
  // 生成导出代码
  moduleCode += `export default {
${Object.entries(tagPaths).flatMap(([path, methods]) => 
    Object.entries(methods).map(([method, operation]) => {
      const operationId = operation.operationId || `${method}${formatKey(path, true)}`;
      const key = formatKey(operationId, config.camelCaseKeys);
      return `  ${key}`;
    })
  ).join(',\n')}
};`;
  
  // 写入文件
  const moduleFilePath = path.join(config.outputDir, `${moduleName}.js`);
  const moduleDir = path.dirname(moduleFilePath);
  
  // 创建目录
  if (!fs.existsSync(moduleDir)) {
    fs.mkdirSync(moduleDir, { recursive: true });
  }
  
  // 检查文件是否存在
  if (fs.existsSync(moduleFilePath) && !config.overwrite) {
    console.log(`模块文件已存在: ${moduleFilePath}`);
    console.log('使用 --overwrite=true 参数覆盖现有文件');
  } else {
    fs.writeFileSync(moduleFilePath, moduleCode);
    console.log(`模块代码已生成: ${moduleFilePath}`);
  }
}

// 格式化键名
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

// 创建路径函数代码
function createPathFunction(path) {
  // 提取路径参数
  const pathParams = [];
  const regex = /{([^}]+)}/g;
  let match;
  
  while ((match = regex.exec(path)) !== null) {
    pathParams.push(match[1]);
  }
  
  // 创建函数
  return function() {
    const args = Array.from(arguments);
    let result = path;
    
    pathParams.forEach((param, index) => {
      result = result.replace(`{${param}}`, args[index]);
    });
    
    return result;
  };
}

// 将Swagger类型映射为JavaScript类型
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

// 运行主函数
main().catch(error => {
  console.error(error);
  process.exit(1);
}); 