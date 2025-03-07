import request from '@/utils/request'

// 用户API
export default {
  // 登录
  login(data) {
    return request({
      url: '/api/users/token/',
      method: 'post',
      data
    })
  },
  
  // 注册
  register(data) {
    return request({
      url: '/api/users/register/',
      method: 'post',
      data
    })
  },
  
  // 获取用户信息
  getUserInfo() {
    return request({
      url: '/api/users/me/',
      method: 'get'
    })
  },
  
  // 更新用户信息
  updateUserInfo(data) {
    return request({
      url: '/api/users/me/',
      method: 'put',
      data
    })
  },
  
  // 修改密码
  changePassword(data) {
    return request({
      url: '/api/users/change_password/',
      method: 'put',
      data
    })
  },
  
  // 获取用户列表（仅管理员）
  getUserList(params) {
    return request({
      url: '/api/users/',
      method: 'get',
      params
    })
  }
} 