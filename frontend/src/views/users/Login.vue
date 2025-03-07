<template>
  <div class="login-container space-background">
    <!-- 流星效果 -->
    <div class="shooting-star"></div>
    <div class="shooting-star"></div>
    <div class="shooting-star"></div>
    
    <!-- 太空云雾 -->
    <div class="space-cloud"></div>
    <div class="space-cloud"></div>
    <div class="space-cloud"></div>
    
    <!-- 行星系统 - 随机分布 -->
    <div class="planet mercury" style="top: 15%; left: 8%;"></div>
    <div class="planet venus" style="top: 65%; left: 22%;"></div>
    <div class="planet earth" style="top: 25%; left: 75%;"></div>
    <div class="planet mars" style="top: 78%; left: 85%;"></div>
    <div class="planet jupiter" style="top: 40%; left: 65%;"></div>
    <div class="planet saturn" style="top: 82%; left: 40%;">
      <div class="saturn-ring"></div>
    </div>
    <div class="planet uranus" style="top: 12%; left: 35%;"></div>
    <div class="planet neptune" style="top: 55%; left: 12%;"></div>
    
    <div class="logo-container">
      <img src="@/assets/rocket-logo.svg" alt="测试平台" class="logo" />
      <h1 class="platform-title">测试平台</h1>
    </div>
    
    <div class="auth-container">
      <h2 class="auth-title">登录</h2>
      
      <el-form ref="loginFormRef" :model="loginForm" :rules="loginRules" label-width="0" @keyup.enter="handleLogin">
        <el-form-item prop="username">
          <label class="input-label">用户名</label>
          <el-input 
            v-model="loginForm.username" 
            placeholder="请输入您的用户名" 
            prefix-icon="User"
            autofocus
          />
        </el-form-item>
        
        <el-form-item prop="password">
          <label class="input-label">密码</label>
          <el-input 
            v-model="loginForm.password" 
            placeholder="请输入您的密码" 
            prefix-icon="Lock" 
            type="password" 
            show-password
          />
        </el-form-item>
        
        <el-form-item>
          <el-button 
            type="primary" 
            :loading="loading" 
            class="login-button" 
            @click="handleLogin"
          >
            登录
          </el-button>
        </el-form-item>
      </el-form>
      
      <div class="auth-footer">
        <span>还没有账号？</span>
        <router-link to="/register" class="register-link">立即注册</router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'
import { useUserStore } from '@/store/user'
import { User, Lock } from '@element-plus/icons-vue'

const router = useRouter()
const route = useRoute()
const userStore = useUserStore()

// 设置页面标题
onMounted(() => {
  document.title = '测试平台 - AiTestPlantForm'
})

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

.logo-container {
  position: absolute;
  top: 30px;
  left: 30px;
  display: flex;
  align-items: center;
  z-index: 10;
}

.logo {
  width: 80px;
  height: 80px;
  filter: drop-shadow(0 0 10px rgba(255, 255, 255, 0.5));
}

.platform-title {
  margin-left: 15px;
  font-size: 36px;
  font-weight: bold;
  color: white;
  text-shadow: 0 0 10px rgba(255, 255, 255, 0.5);
}

/* 这些样式将被 space-background.scss 中的样式覆盖，但保留以防需要 */
.auth-container {
  width: 500px;
  padding: 40px;
  margin: 0;
  max-height: 80vh;
  overflow-y: auto;
}

.auth-title {
  text-align: center;
  margin-bottom: 30px;
  font-size: 24px;
  font-weight: bold;
  color: #333;
}

.input-label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
  color: #333;
  font-size: 14px;
}

.login-button {
  width: 100%;
}

.auth-footer {
  margin-top: 20px;
  text-align: center;
  color: #333;
}

.auth-footer a {
  color: #409EFF;
  text-decoration: none;
}

/* 确保链接可点击 */
.register-link {
  position: relative;
  z-index: 100;
  cursor: pointer;
}
</style> 