<template>
  <div class="register-container space-background">
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
      <h2 class="auth-title">注册</h2>
      
      <el-form ref="registerFormRef" :model="registerForm" :rules="registerRules" label-width="0" autocomplete="off">
        <el-form-item prop="username">
          <label class="input-label">用户名</label>
          <el-input 
            v-model="registerForm.username" 
            placeholder="请输入3-20个字符的用户名" 
            prefix-icon="User"
            autofocus
            class="custom-input"
            autocomplete="off"
          />
        </el-form-item>
        
        <el-form-item prop="email">
          <label class="input-label">邮箱</label>
          <el-input 
            v-model="registerForm.email" 
            placeholder="请输入有效的邮箱地址" 
            prefix-icon="Message"
            class="custom-input"
          />
        </el-form-item>
        
        <el-form-item prop="password">
          <label class="input-label">密码</label>
          <el-input 
            v-model="registerForm.password" 
            placeholder="请输入至少6个字符的密码" 
            prefix-icon="Lock" 
            type="password" 
            show-password
            class="custom-input"
          />
        </el-form-item>
        
        <el-form-item prop="password2">
          <label class="input-label">确认密码</label>
          <el-input 
            v-model="registerForm.password2" 
            placeholder="请再次输入密码" 
            prefix-icon="Lock" 
            type="password" 
            show-password
            class="custom-input"
          />
        </el-form-item>
        
        <el-form-item>
          <el-button 
            type="primary" 
            :loading="loading" 
            class="register-button" 
            @click="handleRegister"
          >
            注册
          </el-button>
        </el-form-item>
      </el-form>
      
      <div class="auth-footer">
        <span>已有账号？</span>
        <router-link to="/login" class="login-link">立即登录</router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { useUserStore } from '@/store/user'
import { User, Message, Lock } from '@element-plus/icons-vue'

const router = useRouter()
const userStore = useUserStore()

// 设置页面标题
onMounted(() => {
  document.title = '测试平台 - AiTestPlantForm'
})

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
          ElMessage.error('注册失败，请检查输入信息')
        }
      } catch (error) {
        console.error('注册错误:', error)
        if (error.response && error.response.data) {
          const errorData = error.response.data;
          let errorMsg = '注册失败: ';
          
          if (typeof errorData === 'object') {
            for (const key in errorData) {
              if (Array.isArray(errorData[key])) {
                errorMsg += `${key} - ${errorData[key].join(', ')}; `;
              } else {
                errorMsg += `${key} - ${errorData[key]}; `;
              }
            }
          } else {
            errorMsg += '请稍后重试';
          }
          
          ElMessage.error(errorMsg)
        } else {
          ElMessage.error('注册失败，请稍后重试')
        }
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

.register-button {
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
.login-link {
  position: relative;
  z-index: 100;
  cursor: pointer;
}

/* 自定义输入框样式，覆盖自动填充的蓝底色块 */
:deep(.custom-input .el-input__inner) {
  background-color: white !important;
  box-shadow: none !important;
}

:deep(.custom-input .el-input__inner:-webkit-autofill),
:deep(.custom-input .el-input__inner:-webkit-autofill:hover),
:deep(.custom-input .el-input__inner:-webkit-autofill:focus) {
  -webkit-box-shadow: 0 0 0 1000px white inset !important;
  -webkit-text-fill-color: #333 !important;
  caret-color: #333 !important;
}
</style> 