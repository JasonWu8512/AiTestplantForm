import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import api from '@/api/user'
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
      const response = await api.login(credentials)
      token.value = response.data.access
      localStorage.setItem('token', token.value)
      localStorage.setItem('refresh_token', response.data.refresh)
      await fetchUserInfo()
      return true
    } catch (error) {
      console.error('登录失败:', error)
      return false
    }
  }
  
  async function register(userData) {
    try {
      await api.register(userData)
      return true
    } catch (error) {
      console.error('注册失败:', error)
      return false
    }
  }
  
  async function fetchUserInfo() {
    try {
      const response = await api.getUserInfo()
      user.value = response.data
      localStorage.setItem('user', JSON.stringify(user.value))
      return user.value
    } catch (error) {
      console.error('获取用户信息失败:', error)
      return null
    }
  }
  
  async function updateUserInfo(userData) {
    try {
      const response = await api.updateUserInfo(userData)
      user.value = { ...user.value, ...response.data }
      localStorage.setItem('user', JSON.stringify(user.value))
      return true
    } catch (error) {
      console.error('更新用户信息失败:', error)
      return false
    }
  }
  
  async function changePassword(passwordData) {
    try {
      await api.changePassword(passwordData)
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