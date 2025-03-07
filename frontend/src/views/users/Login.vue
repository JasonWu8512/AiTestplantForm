<template>
  <div class="login-container space-background">
    <!-- 科技网格 -->
    <div class="tech-grid"></div>
    
    <!-- 光束效果 -->
    <div class="light-beam"></div>
    
    <!-- 浮动粒子 -->
    <div class="particles">
      <div class="particle" v-for="i in 20" :key="i"></div>
    </div>
    
    <!-- 行星系统 -->
    <div class="planets">
      <div class="planet-mercury"></div>
      <div class="planet-venus"></div>
      <div class="planet-earth"></div>
      <div class="planet-mars"></div>
      <div class="planet-jupiter"></div>
      <div class="planet-saturn"></div>
      <div class="planet-saturn-ring"></div>
      <div class="planet-uranus"></div>
      <div class="planet-neptune"></div>
    </div>
    
    <img src="@/assets/logo.svg" alt="AiTestPlantForm Logo" class="tech-logo" />
    <div class="auth-container tech-container">
      <h2 class="auth-title tech-title">登录</h2>
      
      <el-form ref="loginFormRef" :model="loginForm" :rules="loginRules" label-width="0" @keyup.enter="handleLogin">
        <el-form-item prop="username">
          <el-input 
            v-model="loginForm.username" 
            placeholder="用户名" 
            prefix-icon="User" 
            class="tech-input" 
          />
        </el-form-item>
        
        <el-form-item prop="password">
          <el-input 
            v-model="loginForm.password" 
            placeholder="密码" 
            prefix-icon="Lock" 
            type="password" 
            show-password 
            class="tech-input" 
          />
        </el-form-item>
        
        <el-form-item>
          <el-button 
            type="primary" 
            :loading="loading" 
            class="login-button tech-button" 
            @click="handleLogin"
          >
            登录
          </el-button>
        </el-form-item>
      </el-form>
      
      <div class="auth-footer">
        <span>还没有账号？</span>
        <router-link to="/register" class="tech-link">立即注册</router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'
import { useUserStore } from '@/store/user'
import { User, Lock } from '@element-plus/icons-vue'

const router = useRouter()
const route = useRoute()
const userStore = useUserStore()

// 登录表单
const loginForm = reactive({
  username: '',
  password: ''
})

// 表单验证规则
const loginRules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, message: '密码长度不能少于6个字符', trigger: 'blur' }
  ]
}

const loginFormRef = ref(null)
const loading = ref(false)

// 处理登录
const handleLogin = async () => {
  if (!loginFormRef.value) return
  
  await loginFormRef.value.validate(async (valid) => {
    if (valid) {
      loading.value = true
      try {
        const success = await userStore.login(loginForm)
        if (success) {
          ElMessage.success('登录成功')
          // 如果有重定向，则跳转到重定向页面，否则跳转到首页
          const redirect = route.query.redirect || '/'
          router.push(redirect)
        } else {
          ElMessage.error('登录失败，请检查用户名和密码')
        }
      } catch (error) {
        console.error('登录错误:', error)
        ElMessage.error('登录失败，请稍后重试')
      } finally {
        loading.value = false
      }
    }
  })
}
</script>

<style scoped>
.login-container {
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  position: relative;
}

.login-button {
  width: 100%;
}
</style> 