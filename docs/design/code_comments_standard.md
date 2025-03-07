# 代码注释规范

为确保代码的可读性和可维护性，所有代码必须遵循以下注释规范：

## Python代码注释规范

### 模块注释
每个Python模块(.py文件)的顶部应该包含以下信息：
- 模块的简要描述
- 作者信息
- 创建日期
- 最后修改日期

示例：
```python
"""
用户模型模块，定义了用户相关的数据模型

作者: AiTestPlantForm团队
创建日期: 2023-06-01
最后修改: 2023-06-10
"""
```

### 类注释
每个类定义前应该有文档字符串(docstring)，包含：
- 类的简要描述
- 类的属性说明
- 类的方法说明（可选，如果方法较多，可以在各方法中单独注释）

示例：
```python
class User(models.Model):
    """
    用户模型类，存储用户基本信息
    
    属性:
        username: 用户名
        email: 邮箱
        password: 密码(加密存储)
        role: 角色(管理员/普通用户)
        status: 状态(启用/禁用)
        created_at: 创建时间
        updated_at: 更新时间
    """
```

### 函数/方法注释
每个函数或方法定义前应该有文档字符串(docstring)，包含：
- 函数的简要描述
- 参数说明
- 返回值说明
- 异常说明（如果有）
- 使用示例（如果复杂）

示例：
```python
def get_user_by_id(user_id):
    """
    根据用户ID获取用户信息
    
    Args:
        user_id (int): 用户ID
        
    Returns:
        User: 用户对象，如果找不到则返回None
        
    Raises:
        ValueError: 当user_id为负数时抛出
        
    Example:
        >>> user = get_user_by_id(1)
        >>> print(user.username)
        'admin'
    """
```

### 行内注释
对于复杂的逻辑，应该添加行内注释，解释代码的目的和工作原理：

示例：
```python
# 验证用户ID
if user_id < 0:
    raise ValueError("用户ID不能为负数")
    
# 查询数据库
return User.objects.filter(id=user_id).first()
```

## JavaScript/Vue代码注释规范

### 文件注释
每个JavaScript/Vue文件的顶部应该包含以下信息：
- 文件的简要描述
- 作者信息
- 创建日期
- 最后修改日期

示例：
```javascript
/**
 * 用户管理页面组件
 * 
 * @author AiTestPlantForm团队
 * @created 2023-06-01
 * @modified 2023-06-10
 */
```

### 组件注释
Vue组件应该包含以下注释：
- 组件的简要描述
- props说明
- 事件说明
- 插槽说明（如果有）

示例：
```javascript
/**
 * 用户表单组件，用于创建和编辑用户
 * 
 * @component UserForm
 * 
 * @prop {Object} [user] - 用户对象，编辑模式下必须提供
 * @prop {Boolean} [isEdit=false] - 是否为编辑模式
 * 
 * @event submit - 表单提交事件，参数为用户对象
 * @event cancel - 取消操作事件
 * 
 * @example
 * <user-form :user="currentUser" :is-edit="true" @submit="handleSubmit" @cancel="handleCancel" />
 */
```

### 函数/方法注释
每个函数或方法应该包含JSDoc风格的注释：
- 函数的简要描述
- 参数说明
- 返回值说明
- 异常说明（如果有）

示例：
```javascript
/**
 * 用户登录函数
 * 
 * @param {string} username - 用户名
 * @param {string} password - 密码
 * @returns {Promise<Object>} 登录结果，包含token和用户信息
 * @throws {Error} 当用户名或密码为空时抛出
 */
async function login(username, password) {
  // 验证输入
  if (!username || !password) {
    throw new Error('用户名和密码不能为空');
  }
  
  // 发送请求
  return await api.post('/auth/login', { username, password });
}
```

### 行内注释
对于复杂的逻辑，应该添加行内注释，解释代码的目的和工作原理：

示例：
```javascript
// 验证输入
if (!username || !password) {
  throw new Error('用户名和密码不能为空');
}

// 发送请求
return await api.post('/auth/login', { username, password });
```

## CSS/SCSS注释规范

### 文件注释
每个CSS/SCSS文件的顶部应该包含以下信息：
- 文件的简要描述
- 作者信息
- 创建日期
- 最后修改日期

示例：
```scss
/**
 * 用户管理页面样式
 * 
 * @author AiTestPlantForm团队
 * @created 2023-06-01
 * @modified 2023-06-10
 */
```

### 区块注释
对于不同的样式区块，应该添加区块注释：

示例：
```scss
/* 头部导航样式 */
.header-nav {
  display: flex;
  justify-content: space-between;
  
  /* 导航链接 */
  .nav-link {
    color: #333;
    padding: 10px;
    
    /* 激活状态 */
    &.active {
      color: #007bff;
    }
  }
}
```

## 注释最佳实践

1. **保持更新**：当代码变更时，确保相应的注释也得到更新
2. **避免过度注释**：不要注释那些显而易见的代码
3. **使用明确的语言**：注释应该清晰、简洁，使用准确的术语
4. **解释为什么，而不仅仅是什么**：代码本身告诉了我们做了什么，注释应该解释为什么这样做
5. **标记待办事项**：使用TODO、FIXME等标记来指示需要改进的地方

示例：
```python
# TODO: 添加缓存机制提高查询性能
# FIXME: 当用户数量大时可能会有性能问题
```

## 代码审查检查点

在代码审查过程中，应该检查以下与注释相关的点：

1. 所有模块、类、函数是否都有适当的注释
2. 注释是否与代码保持一致
3. 复杂逻辑是否有行内注释解释
4. 注释是否遵循了规定的格式
5. 注释是否清晰、简洁、有用
``` 