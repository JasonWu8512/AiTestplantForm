<template>
  <div class="profile-container">
    <div class="page-container">
      <h2 class="page-title">个人信息</h2>
      
      <el-tabs v-model="activeTab">
        <el-tab-pane label="基本信息" name="basic">
          <el-form ref="basicFormRef" :model="basicForm" :rules="basicRules" label-width="100px" class="form-container">
            <!-- 头像选择区域 -->
            <el-form-item label="头像">
              <div class="avatar-container">
                <div class="current-avatar">
                  <el-avatar :size="100" :src="avatarPreview">{{ userInitials }}</el-avatar>
                  <div class="avatar-text">当前头像</div>
                </div>
                
                <div class="avatar-options">
                  <div class="avatar-section">
                    <div class="section-title">选择默认头像</div>
                    <div class="default-avatars">
                      <div 
                        v-for="(avatar, index) in defaultAvatars" 
                        :key="index" 
                        class="avatar-item"
                        :class="{ 'selected': selectedDefaultAvatar === avatar }"
                        @click="selectDefaultAvatar(avatar)"
                      >
                        <img :src="avatar" alt="默认头像" class="avatar-img" />
                      </div>
                    </div>
                  </div>
                  
                  <div class="avatar-section">
                    <div class="section-title">上传自定义头像</div>
                    <div class="upload-container">
                      <el-upload
                        class="avatar-uploader"
                        action="#"
                        :auto-upload="false"
                        :show-file-list="false"
                        :on-change="handleAvatarChange"
                        accept="image/jpeg,image/png,image/gif"
                      >
                        <el-button type="primary">选择图片</el-button>
                      </el-upload>
                      <div class="upload-tips">
                        支持JPG、PNG、GIF格式，文件大小不超过2MB
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </el-form-item>
            
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
import { ref, reactive, onMounted, computed } from 'vue'
import { ElMessage } from 'element-plus'
import { useUserStore } from '@/store/user'

const userStore = useUserStore()
const activeTab = ref('basic')

// 默认头像列表
const defaultAvatars = [
  '/avatars/male1.svg',
  '/avatars/male2.svg',
  '/avatars/male3.svg',
  '/avatars/female1.svg',
  '/avatars/female2.svg',
  '/avatars/female3.svg'
]

// 基本信息表单
const basicForm = reactive({
  username: '',
  email: '',
  first_name: '',
  last_name: '',
  phone: '',
  department: '',
  position: '',
  avatar: null
})

// 密码表单
const passwordForm = reactive({
  old_password: '',
  new_password: '',
  new_password2: ''
})

// 头像相关状态
const selectedDefaultAvatar = ref(null)
const customAvatarFile = ref(null)
const avatarPreview = computed(() => {
  if (customAvatarFile.value) {
    return URL.createObjectURL(customAvatarFile.value)
  }
  if (selectedDefaultAvatar.value) {
    return selectedDefaultAvatar.value
  }
  return userStore.user.avatar || ''
})

// 用户名首字母（用于没有头像时显示）
const userInitials = computed(() => {
  const username = userStore.user.username || ''
  return username.substring(0, 1).toUpperCase()
})

// 选择默认头像
const selectDefaultAvatar = (avatar) => {
  selectedDefaultAvatar.value = avatar
  customAvatarFile.value = null
  basicForm.avatar = avatar
}

// 处理头像上传
const handleAvatarChange = (file) => {
  const isImage = file.type.startsWith('image/')
  const isLt2M = file.size / 1024 / 1024 < 2
  
  if (!isImage) {
    ElMessage.error('上传头像图片只能是图片格式!')
    return false
  }
  
  if (!isLt2M) {
    ElMessage.error('上传头像图片大小不能超过 2MB!')
    return false
  }
  
  customAvatarFile.value = file.raw
  selectedDefaultAvatar.value = null
  basicForm.avatar = file.raw
}

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
    
    // 如果用户已有头像，显示当前头像
    if (user.avatar) {
      // 检查是否是默认头像之一
      const isDefaultAvatar = defaultAvatars.includes(user.avatar)
      if (isDefaultAvatar) {
        selectedDefaultAvatar.value = user.avatar
      }
    }
  }
})

// 更新基本信息
const updateBasicInfo = async () => {
  if (!basicFormRef.value) return
  
  await basicFormRef.value.validate(async (valid) => {
    if (valid) {
      basicLoading.value = true
      try {
        // 创建FormData对象用于文件上传
        const formData = new FormData()
        
        // 添加基本信息字段
        formData.append('email', basicForm.email)
        formData.append('first_name', basicForm.first_name)
        formData.append('last_name', basicForm.last_name)
        formData.append('phone', basicForm.phone)
        formData.append('department', basicForm.department)
        formData.append('position', basicForm.position)
        
        // 处理头像
        if (customAvatarFile.value) {
          // 上传自定义头像
          formData.append('avatar', customAvatarFile.value)
        } else if (selectedDefaultAvatar.value) {
          // 使用默认头像
          formData.append('avatar', selectedDefaultAvatar.value)
        }
        
        const success = await userStore.updateUserInfo(formData)
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

.page-title {
  margin-bottom: 20px;
  font-size: 24px;
  color: #303133;
}

.form-container {
  max-width: 600px;
}

/* 头像相关样式 */
.avatar-container {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.current-avatar {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
}

.avatar-text {
  font-size: 14px;
  color: #606266;
}

.avatar-options {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.avatar-section {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.section-title {
  font-size: 16px;
  font-weight: bold;
  color: #303133;
}

.default-avatars {
  display: flex;
  flex-wrap: wrap;
  gap: 15px;
}

.avatar-item {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  overflow: hidden;
  cursor: pointer;
  border: 2px solid transparent;
  transition: all 0.3s;
}

.avatar-item:hover {
  transform: scale(1.05);
}

.avatar-item.selected {
  border-color: #409EFF;
}

.avatar-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.upload-container {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.upload-tips {
  font-size: 12px;
  color: #909399;
}
</style> 