import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import userApi from '@/api/user'
import router from '@/router'

export const useUserStore = defineStore('user', () => {
  // 状态
  const token = ref(localStorage.getItem('token') || '')
  const user = ref(JSON.parse(localStorage.getItem('user') || '{}'))
  
  // 计算属性
  const isLoggedIn = computed(() => !!token.value)
  const isAdmin = computed(() => user.value.is_staff === true)
  
  // 操作
  async function login(credentials) {
    try {
      console.log('开始登录请求...')
      const response = await userApi.login(credentials)
      console.log('登录响应:', response)
      
      token.value = response.access
      localStorage.setItem('token', token.value)
      localStorage.setItem('refresh_token', response.refresh)
      console.log('令牌已保存到localStorage')
      
      // 确保获取用户信息成功
      console.log('开始获取用户信息...')
      const userInfo = await fetchUserInfo()
      if (!userInfo) {
        console.error('获取用户信息失败')
        return false
      }
      
      console.log('登录成功，用户信息:', userInfo)
      return true
    } catch (error) {
      console.error('登录失败:', error)
      if (error.response) {
        console.error('错误响应:', error.response)
      }
      return false
    }
  }
  
  async function register(userData) {
    try {
      await userApi.register(userData)
      return true
    } catch (error) {
      console.error('注册失败:', error)
      throw error; // 将错误向上传递，以便在组件中处理
    }
  }
  
  async function fetchUserInfo() {
    try {
      console.log('发送获取用户信息请求...')
      console.log('当前令牌:', localStorage.getItem('token'))
      const response = await userApi.getUserInfo()
      console.log('获取用户信息响应:', response)
      
      // 处理头像URL，添加时间戳避免缓存问题
      if (response && response.avatar) {
        const timestamp = new Date().getTime()
        
        // 确保默认头像路径正确 - 改进检测逻辑
        if (response.avatar.startsWith('/avatars/') && 
            (response.avatar.includes('male') || response.avatar.includes('female'))) {
          // 这是默认头像，保持原样
          console.log('使用默认头像:', response.avatar)
        } else {
          // 这是自定义头像，添加时间戳避免缓存
          response.avatar = response.avatar.includes('?') 
            ? `${response.avatar}&_t=${timestamp}` 
            : `${response.avatar}?_t=${timestamp}`
        }
        
        console.log('获取到的头像URL:', response.avatar)
      }
      
      user.value = response
      // 强制更新localStorage中的用户信息
      localStorage.setItem('user', JSON.stringify(user.value))
      console.log('用户信息已保存到localStorage')
      return user.value
    } catch (error) {
      console.error('获取用户信息失败:', error)
      if (error.response) {
        console.error('错误响应:', error.response)
      }
      return null
    }
  }
  
  async function updateUserInfo(userData) {
    try {
      const response = await userApi.updateUserInfo(userData)
      
      // 处理头像URL，添加时间戳避免缓存问题
      if (response && response.avatar) {
        const timestamp = new Date().getTime()
        
        // 确保默认头像路径正确 - 改进检测逻辑
        if (response.avatar.startsWith('/avatars/') && 
            (response.avatar.includes('male') || response.avatar.includes('female'))) {
          // 这是默认头像，保持原样
          console.log('使用默认头像:', response.avatar)
        } else {
          // 这是自定义头像，添加时间戳避免缓存
          response.avatar = response.avatar.includes('?') 
            ? `${response.avatar}&_t=${timestamp}` 
            : `${response.avatar}?_t=${timestamp}`
        }
        
        console.log('更新后的头像URL:', response.avatar)
      }
      
      // 更新用户信息
      user.value = { ...user.value, ...response }
      
      // 强制更新localStorage中的用户信息
      localStorage.setItem('user', JSON.stringify(user.value))
      console.log('更新后的用户信息已保存到localStorage')
      
      return true
    } catch (error) {
      console.error('更新用户信息失败:', error)
      if (error.response) {
        console.error('错误响应:', error.response)
      }
      return false
    }
  }
  
  async function changePassword(passwordData) {
    try {
      await userApi.changePassword(passwordData)
      return true
    } catch (error) {
      console.error('修改密码失败:', error)
      return false
    }
  }
  
  function logout() {
    token.value = ''
    user.value = {}
    localStorage.removeItem('token')
    localStorage.removeItem('refresh_token')
    localStorage.removeItem('user')
    router.push('/login')
  }
  
  return {
    token,
    user,
    isLoggedIn,
    isAdmin,
    login,
    register,
    fetchUserInfo,
    updateUserInfo,
    changePassword,
    logout
  }
}) 