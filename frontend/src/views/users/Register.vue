<template>
  <div class="register-container space-background">
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
      <h2 class="auth-title tech-title">注册</h2>
      
      <el-form ref="registerFormRef" :model="registerForm" :rules="registerRules" label-width="0">
        <el-form-item prop="username">
          <el-input 
            v-model="registerForm.username" 
            placeholder="用户名" 
            prefix-icon="User" 
            class="tech-input" 
          />
        </el-form-item>
        
        <el-form-item prop="email">
          <el-input 
            v-model="registerForm.email" 
            placeholder="邮箱" 
            prefix-icon="Message" 
            class="tech-input" 
          />
        </el-form-item>
        
        <el-form-item prop="password">
          <el-input 
            v-model="registerForm.password" 
            placeholder="密码" 
            prefix-icon="Lock" 
            type="password" 
            show-password 
            class="tech-input" 
          />
        </el-form-item>
        
        <el-form-item prop="password2">
          <el-input 
            v-model="registerForm.password2" 
            placeholder="确认密码" 
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
            class="register-button tech-button" 
            @click="handleRegister"
          >
            注册
          </el-button>
        </el-form-item>
      </el-form>
      
      <div class="auth-footer">
        <span>已有账号？</span>
        <router-link to="/login" class="tech-link">立即登录</router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { useUserStore } from '@/store/user'
import { User, Message, Lock } from '@element-plus/icons-vue'

const router = useRouter()
const userStore = useUserStore()

// 注册表单
const registerForm = reactive({
  username: '',
  email: '',
  password: '',
  password2: ''
})

// 验证密码是否一致
const validatePass2 = (rule, value, callback) => {
  if (value === '') {
    callback(new Error('请再次输入密码'))
  } else if (value !== registerForm.password) {
    callback(new Error('两次输入密码不一致'))
  } else {
    callback()
  }
}

// 表单验证规则
const registerRules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, max: 20, message: '长度在 3 到 20 个字符', trigger: 'blur' }
  ],
  email: [
    { required: true, message: '请输入邮箱地址', trigger: 'blur' },
    { type: 'email', message: '请输入正确的邮箱地址', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, message: '密码长度不能少于6个字符', trigger: 'blur' }
  ],
  password2: [
    { required: true, message: '请再次输入密码', trigger: 'blur' },
    { validator: validatePass2, trigger: 'blur' }
  ]
}

const registerFormRef = ref(null)
const loading = ref(false)

// 处理注册
const handleRegister = async () => {
  if (!registerFormRef.value) return
  
  await registerFormRef.value.validate(async (valid) => {
    if (valid) {
      loading.value = true
      try {
        const success = await userStore.register(registerForm)
        if (success) {
          ElMessage.success('注册成功，请登录')
          router.push('/login')
        } else {
          ElMessage.error('注册失败，请稍后重试')
        }
      } catch (error) {
        console.error('注册错误:', error)
        ElMessage.error('注册失败，请稍后重试')
      } finally {
        loading.value = false
      }
    }
  })
}
</script>

<style scoped>
.register-container {
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  position: relative;
}

.register-button {
  width: 100%;
}
</style> 