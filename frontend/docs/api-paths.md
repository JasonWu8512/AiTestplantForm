# API路径管理工具

本文档介绍如何使用API路径管理工具，包括API路径常量、API调用函数和Swagger/OpenAPI集成。

## 1. API路径常量

API路径常量定义在 `src/utils/api-paths.js` 文件中，用于集中管理所有API路径，确保前端API调用路径与后端路由配置一致。

### 1.1 基本用法

```javascript
import { USER_API, getFullPath } from '@/utils/api-paths';

// 获取用户列表API路径
const userListPath = USER_API.LIST; // '/users/'

// 获取用户详情API路径
const userDetailPath = USER_API.DETAIL(1); // '/users/1/'

// 获取完整API路径
const fullPath = getFullPath(userListPath); // '/api/users/'
```

### 1.2 API路径常量结构

API路径常量按模块分组，每个模块对应一个常量对象，如：

```javascript
// 用户相关API路径
export const USER_API = {
  LOGIN: '/users/login/',
  LOGOUT: '/users/logout/',
  PROFILE: '/users/profile/',
  LIST: '/users/',
  DETAIL: (id) => `/users/${id}/`,
  // ...
};

// 测试用例相关API路径
export const TESTCASE_API = {
  LIST: '/testcases/',
  DETAIL: (id) => `/testcases/${id}/`,
  // ...
};

// 测试计划相关API路径
export const TESTPLAN_API = {
  LIST: '/testplans/',
  DETAIL: (id) => `/testplans/${id}/`,
  // ...
};
```

### 1.3 辅助函数

API路径管理工具提供了以下辅助函数：

#### getFullPath

获取完整的API路径，包括API前缀和查询参数。

```javascript
/**
 * 获取完整的API路径
 * @param {string} path - API路径
 * @param {Object} options - 配置选项
 * @param {boolean} options.addPrefix - 是否添加API前缀，默认为true
 * @param {boolean} options.addVersion - 是否添加API版本，默认为false
 * @param {Object} options.params - URL参数对象
 * @returns {string} - 完整的API路径
 */
export function getFullPath(path, options = {}) {
  // ...
}
```

示例：

```javascript
// 基本用法
getFullPath('/users/'); // '/api/users/'

// 添加API版本
getFullPath('/users/', { addVersion: true }); // '/api/v1/users/'

// 添加查询参数
getFullPath('/users/', { params: { page: 1, limit: 10 } }); // '/api/users/?page=1&limit=10'
```

#### buildApiPath

构建API路径，替换路径参数并添加查询参数。

```javascript
/**
 * 构建API路径
 * @param {string} basePath - 基础路径
 * @param {Object} pathParams - 路径参数
 * @param {Object} queryParams - 查询参数
 * @returns {string} - 完整的API路径
 */
export function buildApiPath(basePath, pathParams = {}, queryParams = {}) {
  // ...
}
```

示例：

```javascript
// 替换路径参数
buildApiPath('/users/:id', { id: 1 }); // '/api/users/1'

// 替换路径参数并添加查询参数
buildApiPath('/users/:id', { id: 1 }, { fields: 'name,email' }); // '/api/users/1?fields=name%2Cemail'
```

#### getApiModule

获取API模块对象。

```javascript
/**
 * 获取API模块
 * @param {string} moduleName - 模块名称
 * @returns {Object} - API模块对象
 */
export function getApiModule(moduleName) {
  // ...
}
```

示例：

```javascript
// 获取用户模块
const userApi = getApiModule('user'); // USER_API对象

// 获取测试用例模块
const testcaseApi = getApiModule('testcase'); // TESTCASE_API对象
```

## 2. API调用函数

API调用函数定义在 `src/api` 目录下的各个模块文件中，用于封装API请求。

### 2.1 基本用法

```javascript
import { getTestPlans, createTestPlan } from '@/api/testplan';

// 获取测试计划列表
async function fetchTestPlans() {
  try {
    const response = await getTestPlans({ page: 1, limit: 10 });
    console.log('测试计划列表:', response);
  } catch (error) {
    console.error('获取测试计划列表失败:', error);
  }
}

// 创建测试计划
async function createNewTestPlan(data) {
  try {
    const response = await createTestPlan(data);
    console.log('创建测试计划成功:', response);
  } catch (error) {
    console.error('创建测试计划失败:', error);
  }
}
```

### 2.2 API调用函数结构

API调用函数按模块分组，每个模块对应一个文件，如：

- `src/api/user.js`: 用户相关API调用函数
- `src/api/testcase.js`: 测试用例相关API调用函数
- `src/api/testplan.js`: 测试计划相关API调用函数

每个API调用函数都使用API路径常量和 `getFullPath` 函数构建请求URL，如：

```javascript
import request from '@/utils/request';
import { TESTPLAN_API, getFullPath } from '@/utils/api-paths';

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
  });
}
```

## 3. Swagger/OpenAPI集成

API路径管理工具支持从Swagger/OpenAPI文档自动生成API代码，包括API路径常量和API调用函数。

### 3.1 生成API代码

使用以下命令从Swagger/OpenAPI文档生成API代码：

```bash
# 生成所有模块的API代码
npm run generate-api:all

# 生成指定模块的API代码
npm run generate-api:users
npm run generate-api:testcases
npm run generate-api:testplans
npm run generate-api:executions
```

### 3.2 自定义生成选项

可以通过命令行参数自定义生成选项：

```bash
# 指定Swagger文档URL
npm run generate-api -- --url=http://localhost:8000/swagger/?format=json

# 指定输出目录
npm run generate-api -- --output=src/api

# 指定要生成的模块
npm run generate-api -- --modules=users,testcases

# 指定要排除的模块
npm run generate-api -- --exclude=reports,settings

# 是否按标签分组
npm run generate-api -- --groupByTag=true

# 是否使用驼峰命名
npm run generate-api -- --camelCase=true

# 是否包含注释
npm run generate-api -- --comments=true

# 是否覆盖现有文件
npm run generate-api -- --overwrite=true
```

### 3.3 生成的文件

生成的文件包括：

- `src/utils/api-paths.js`: API路径常量
- `src/api/*.js`: API调用函数

### 3.4 Swagger API生成工具

Swagger API生成工具定义在 `src/utils/swagger-generator.js` 文件中，提供了以下功能：

- `generateApiPaths`: 从Swagger/OpenAPI文档生成API路径常量
- `generateApiFunctions`: 从Swagger/OpenAPI文档生成API调用函数
- `generateApiFromUrl`: 从Swagger/OpenAPI URL获取文档并生成API代码
- `generateApiModuleCode`: 生成完整的API模块代码

## 4. 最佳实践

### 4.1 使用API路径常量

始终使用API路径常量而不是硬编码API路径，确保前端API调用路径与后端路由配置一致。

```javascript
// 好的做法
import { USER_API, getFullPath } from '@/utils/api-paths';
const url = getFullPath(USER_API.LIST);

// 不好的做法
const url = '/api/users/';
```

### 4.2 使用API调用函数

始终使用API调用函数而不是直接使用 `axios` 或 `fetch`，确保API调用的一致性和可维护性。

```javascript
// 好的做法
import { getUsers } from '@/api/user';
const response = await getUsers();

// 不好的做法
import axios from 'axios';
const response = await axios.get('/api/users/');
```

### 4.3 处理API错误

始终处理API调用可能出现的错误，提供友好的错误提示。

```javascript
import { getUsers } from '@/api/user';
import { showApiError } from '@/utils/feedback';

try {
  const response = await getUsers();
  // 处理响应数据
} catch (error) {
  // 使用统一的错误处理函数
  showApiError(error, '获取用户列表失败');
}
```

### 4.4 定期更新API代码

定期从Swagger/OpenAPI文档更新API代码，确保前端API调用与后端API保持同步。

```bash
# 更新所有API代码
npm run generate-api:all
```

## 5. 故障排除

### 5.1 API路径不匹配

如果API调用返回404错误，可能是API路径不匹配导致的。检查以下几点：

1. 确认API路径常量是否正确
2. 确认API调用函数是否使用了正确的API路径常量
3. 确认后端路由配置是否与API路径常量一致

### 5.2 API参数错误

如果API调用返回400错误，可能是API参数错误导致的。检查以下几点：

1. 确认API调用函数的参数是否正确
2. 确认API调用函数的参数类型是否正确
3. 确认后端API是否期望接收这些参数

### 5.3 生成API代码失败

如果生成API代码失败，可能是Swagger/OpenAPI文档不可访问或格式不正确导致的。检查以下几点：

1. 确认Swagger/OpenAPI文档URL是否正确
2. 确认Swagger/OpenAPI文档是否可访问
3. 确认Swagger/OpenAPI文档格式是否正确

## 6. 参考资料

- [Swagger/OpenAPI规范](https://swagger.io/specification/)
- [RESTful API设计指南](https://restfulapi.net/)
- [Axios文档](https://axios-http.com/docs/intro)
- [Vue.js文档](https://vuejs.org/guide/introduction.html) 