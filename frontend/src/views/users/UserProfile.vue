<template>
  <div class="profile-container">
    <div class="page-container">
      <h2 class="page-title">个人信息</h2>
      
      <el-tabs v-model="activeTab">
        <el-tab-pane label="基本信息" name="basic">
          <el-form ref="basicFormRef" :model="basicForm" :rules="basicRules" label-width="100px" class="form-container">
            <el-form-item label="用户名">
              <el-input v-model="basicForm.username" disabled />
            </el-form-item>
            
            <el-form-item label="邮箱" prop="email">
              <el-input v-model="basicForm.email" />
            </el-form-item>
            
            <el-form-item label="姓" prop="last_name">
              <el-input v-model="basicForm.last_name" />
            </el-form-item>
            
            <el-form-item label="名" prop="first_name">
              <el-input v-model="basicForm.first_name" />
            </el-form-item>
            
            <el-form-item label="手机号" prop="phone">
              <el-input v-model="basicForm.phone" />
            </el-form-item>
            
            <el-form-item label="部门" prop="department">
              <el-input v-model="basicForm.department" />
            </el-form-item>
            
            <el-form-item label="职位" prop="position">
              <el-input v-model="basicForm.position" />
            </el-form-item>
            
            <el-form-item>
              <el-button type="primary" :loading="basicLoading" @click="updateBasicInfo">保存</el-button>
            </el-form-item>
          </el-form>
        </el-tab-pane>
        
        <el-tab-pane label="修改密码" name="password">
          <el-form ref="passwordFormRef" :model="passwordForm" :rules="passwordRules" label-width="100px" class="form-container">
            <el-form-item label="当前密码" prop="old_password">
              <el-input v-model="passwordForm.old_password" type="password" show-password />
            </el-form-item>
            
            <el-form-item label="新密码" prop="new_password">
              <el-input v-model="passwordForm.new_password" type="password" show-password />
            </el-form-item>
            
            <el-form-item label="确认新密码" prop="new_password2">
              <el-input v-model="passwordForm.new_password2" type="password" show-password />
            </el-form-item>
            
            <el-form-item>
              <el-button type="primary" :loading="passwordLoading" @click="updatePassword">修改密码</el-button>
            </el-form-item>
          </el-form>
        </el-tab-pane>
      </el-tabs>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { useUserStore } from '@/store/user'

const userStore = useUserStore()
const activeTab = ref('basic')

// 基本信息表单
const basicForm = reactive({
  username: '',
  email: '',
  first_name: '',
  last_name: '',
  phone: '',
  department: '',
  position: ''
})

// 密码表单
const passwordForm = reactive({
  old_password: '',
  new_password: '',
  new_password2: ''
})

// 验证新密码是否一致
const validatePass2 = (rule, value, callback) => {
  if (value === '') {
    callback(new Error('请再次输入新密码'))
  } else if (value !== passwordForm.new_password) {
    callback(new Error('两次输入密码不一致'))
  } else {
    callback()
  }
}

// 表单验证规则
const basicRules = {
  email: [
    { type: 'email', message: '请输入正确的邮箱地址', trigger: 'blur' }
  ],
  phone: [
    { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号码', trigger: 'blur' }
  ]
}

const passwordRules = {
  old_password: [
    { required: true, message: '请输入当前密码', trigger: 'blur' }
  ],
  new_password: [
    { required: true, message: '请输入新密码', trigger: 'blur' },
    { min: 6, message: '密码长度不能少于6个字符', trigger: 'blur' }
  ],
  new_password2: [
    { required: true, message: '请再次输入新密码', trigger: 'blur' },
    { validator: validatePass2, trigger: 'blur' }
  ]
}

const basicFormRef = ref(null)
const passwordFormRef = ref(null)
const basicLoading = ref(false)
const passwordLoading = ref(false)

// 获取用户信息
onMounted(async () => {
  const user = await userStore.fetchUserInfo()
  if (user) {
    basicForm.username = user.username || ''
    basicForm.email = user.email || ''
    basicForm.first_name = user.first_name || ''
    basicForm.last_name = user.last_name || ''
    basicForm.phone = user.phone || ''
    basicForm.department = user.department || ''
    basicForm.position = user.position || ''
  }
})

// 更新基本信息
const updateBasicInfo = async () => {
  if (!basicFormRef.value) return
  
  await basicFormRef.value.validate(async (valid) => {
    if (valid) {
      basicLoading.value = true
      try {
        const success = await userStore.updateUserInfo(basicForm)
        if (success) {
          ElMessage.success('个人信息更新成功')
        } else {
          ElMessage.error('个人信息更新失败')
        }
      } catch (error) {
        console.error('更新错误:', error)
        ElMessage.error('个人信息更新失败')
      } finally {
        basicLoading.value = false
      }
    }
  })
}

// 更新密码
const updatePassword = async () => {
  if (!passwordFormRef.value) return
  
  await passwordFormRef.value.validate(async (valid) => {
    if (valid) {
      passwordLoading.value = true
      try {
        const success = await userStore.changePassword(passwordForm)
        if (success) {
          ElMessage.success('密码修改成功')
          passwordForm.old_password = ''
          passwordForm.new_password = ''
          passwordForm.new_password2 = ''
          passwordFormRef.value.resetFields()
        } else {
          ElMessage.error('密码修改失败')
        }
      } catch (error) {
        console.error('密码修改错误:', error)
        ElMessage.error('密码修改失败')
      } finally {
        passwordLoading.value = false
      }
    }
  })
}
</script>

<style scoped>
.profile-container {
  min-height: 100%;
  background-color: #fff;
  padding: 20px;
  border-radius: 4px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}
</style> 