import request from '@/utils/request'

// 用户API
export default {
  // 登录
  login(data) {
    return request({
      url: '/users/token/',
      method: 'post',
      data
    })
  },
  
  // 注册
  register(data) {
    return request({
      url: '/users/register/',
      method: 'post',
      data
    })
  },
  
  // 获取用户信息
  getUserInfo() {
    return request({
      url: '/users/me/',
      method: 'get'
    })
  },
  
  // 更新用户信息
  updateUserInfo(data) {
    const config = {
      url: '/users/update_me/',
      method: 'put',
      data
    };
    
    // 如果是FormData类型，添加适当的Content-Type头
    if (data instanceof FormData) {
      config.headers = {
        'Content-Type': 'multipart/form-data'
      };
    }
    
    return request(config);
  },
  
  // 修改密码
  changePassword(data) {
    return request({
      url: '/users/change_password/',
      method: 'put',
      data
    })
  },
  
  // 获取用户列表（仅管理员）
  getUserList(params) {
    return request({
      url: '/users/',
      method: 'get',
      params
    })
  }
} 