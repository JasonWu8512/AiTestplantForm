<!--
/**
 * 用户个人信息页面
 * 
 * 该页面允许用户查看和编辑个人信息，包括基本信息和密码修改。
 * 新增功能：自定义头像选择，支持默认卡通头像和本地图片上传。
 * 
 * 作者: AiTestPlantForm团队
 * 创建日期: 2023-06-01
 * 最后修改: 2025-03-07
 */
-->
<template>
  <div class="profile-container">
    <div class="page-container">
      <div class="page-header">
        <h2 class="page-title">个人信息</h2>
        <el-button @click="handleBack" plain icon="el-icon-back" class="back-button">返回</el-button>
      </div>
      
      <el-tabs v-model="activeTab" class="custom-tabs">
        <el-tab-pane label="基本信息" name="basic">
          <el-form ref="basicFormRef" :model="basicForm" :rules="basicRules" label-width="100px" class="form-container">
            <!-- 头像选择区域 -->
            <el-form-item label="头像" class="avatar-form-item">
              <div class="avatar-container">
                <div class="current-avatar">
                  <el-avatar :size="120" :src="avatarPreview" class="avatar-preview">{{ userInitials }}</el-avatar>
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
                      <!-- 使用原生文件输入框替代el-upload -->
                      <div class="file-upload-wrapper">
                        <el-button type="primary" @click="triggerFileInput" class="upload-button">
                          <i class="el-icon-upload"></i> 选择图片
                        </el-button>
                        <input 
                          type="file" 
                          ref="fileInput" 
                          style="display: none" 
                          accept="image/jpeg,image/png,image/gif"
                          @change="handleFileChange"
                        />
                      </div>
                      <div v-if="customAvatarFile" class="selected-file-info">
                        <i class="el-icon-document"></i> 已选择: {{ customAvatarFile.name }}
                      </div>
                      <div class="upload-tips">
                        <i class="el-icon-info-circle"></i> 支持JPG、PNG、GIF格式，文件大小不超过2MB
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </el-form-item>
            
            <div class="form-divider"></div>
            
            <div class="form-section-title">基本资料</div>
            
            <el-form-item label="用户名" class="form-item">
              <el-input v-model="basicForm.username" disabled class="form-input disabled-input" />
            </el-form-item>
            
            <el-form-item label="邮箱" prop="email" class="form-item">
              <el-input v-model="basicForm.email" @input="formChanged = true" class="form-input" />
            </el-form-item>
            
            <div class="form-row">
              <el-form-item label="姓" prop="last_name" class="form-item half-width">
                <el-input v-model="basicForm.last_name" @input="formChanged = true" class="form-input" />
              </el-form-item>
              
              <el-form-item label="名" prop="first_name" class="form-item half-width">
                <el-input v-model="basicForm.first_name" @input="formChanged = true" class="form-input" />
              </el-form-item>
            </div>
            
            <el-form-item label="手机号" prop="phone" class="form-item">
              <el-input v-model="basicForm.phone" @input="formChanged = true" class="form-input" />
            </el-form-item>
            
            <div class="form-divider"></div>
            
            <div class="form-section-title">工作信息</div>
            
            <div class="form-row">
              <el-form-item label="部门" prop="department" class="form-item half-width">
                <el-input v-model="basicForm.department" @input="formChanged = true" class="form-input" />
              </el-form-item>
              
              <el-form-item label="职位" prop="position" class="form-item half-width">
                <el-input v-model="basicForm.position" @input="formChanged = true" class="form-input" />
              </el-form-item>
            </div>
            
            <!-- 只有当表单有修改时才显示按钮 -->
            <el-form-item class="action-buttons-container" v-if="formChanged">
              <div class="form-buttons">
                <el-button @click="handleBack" class="cancel-button">取消</el-button>
                <el-button type="primary" :loading="basicLoading" @click="updateBasicInfo" class="save-button">保存</el-button>
              </div>
            </el-form-item>
          </el-form>
        </el-tab-pane>
        
        <el-tab-pane label="修改密码" name="password">
          <el-form ref="passwordFormRef" :model="passwordForm" :rules="passwordRules" label-width="120px" class="form-container">
            <div class="password-form-header">
              <i class="el-icon-lock password-icon"></i>
              <div class="password-form-title">修改您的密码</div>
              <div class="password-form-subtitle">为了保障账户安全，建议定期更换密码</div>
            </div>
            
            <el-form-item label="当前密码" prop="old_password" class="form-item">
              <el-input 
                v-model="passwordForm.old_password" 
                type="password" 
                show-password 
                @input="passwordFormChanged = true" 
                class="form-input"
                placeholder="请输入当前密码"
              />
            </el-form-item>
            
            <el-form-item label="新密码" prop="new_password" class="form-item">
              <el-input 
                v-model="passwordForm.new_password" 
                type="password" 
                show-password 
                @input="passwordFormChanged = true" 
                class="form-input"
                placeholder="请输入新密码"
              />
            </el-form-item>
            
            <el-form-item label="确认新密码" prop="new_password2" class="form-item">
              <el-input 
                v-model="passwordForm.new_password2" 
                type="password" 
                show-password 
                @input="passwordFormChanged = true" 
                class="form-input"
                placeholder="请再次输入新密码"
              />
            </el-form-item>
            
            <div class="password-tips">
              <i class="el-icon-info-circle"></i> 密码长度不能少于6个字符，建议使用字母、数字和特殊字符的组合
            </div>
            
            <!-- 只有当密码表单有修改时才显示按钮 -->
            <el-form-item class="action-buttons-container" v-if="passwordFormChanged">
              <div class="form-buttons">
                <el-button @click="handleBack" class="cancel-button">取消</el-button>
                <el-button type="primary" :loading="passwordLoading" @click="updatePassword" class="save-button">保存</el-button>
              </div>
            </el-form-item>
          </el-form>
        </el-tab-pane>
      </el-tabs>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed, watch } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { useUserStore } from '@/store/user'
import { useRouter } from 'vue-router'

const userStore = useUserStore()
const router = useRouter()
const activeTab = ref('basic')
const fileInput = ref(null)

// 表单修改状态
const formChanged = ref(false)
const passwordFormChanged = ref(false)
const originalFormData = ref({})

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
    formChanged.value = true
    return URL.createObjectURL(customAvatarFile.value)
  }
  if (selectedDefaultAvatar.value) {
    formChanged.value = true
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
  formChanged.value = true
}

// 触发文件输入框点击
const triggerFileInput = () => {
  fileInput.value.click()
}

// 处理文件选择
const handleFileChange = (event) => {
  const file = event.target.files[0]
  if (!file) return
  
  const isImage = file.type.startsWith('image/')
  const isLt2M = file.size / 1024 / 1024 < 2
  
  if (!isImage) {
    ElMessage.error('上传头像图片只能是图片格式!')
    return
  }
  
  if (!isLt2M) {
    ElMessage.error('上传头像图片大小不超过 2MB!')
    return
  }
  
  customAvatarFile.value = file
  selectedDefaultAvatar.value = null
  basicForm.avatar = file
  formChanged.value = true
  
  // 显示成功消息
  ElMessage.success('图片已选择，点击保存按钮完成上传')
  
  // 打印日志，帮助调试
  console.log('选择的文件:', file)
  console.log('预览URL:', URL.createObjectURL(file))
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
    
    // 保存原始表单数据，用于检测变更
    originalFormData.value = { ...basicForm }
    
    // 如果用户已有头像，显示当前头像
    if (user.avatar) {
      // 检查是否是默认头像之一
      const isDefaultAvatar = defaultAvatars.includes(user.avatar)
      if (isDefaultAvatar) {
        selectedDefaultAvatar.value = user.avatar
      }
    }
  }
  
  // 重置表单修改状态
  formChanged.value = false
  passwordFormChanged.value = false
})

// 处理返回按钮点击
const handleBack = () => {
  if (activeTab.value === 'basic' && formChanged.value) {
    ElMessageBox.confirm(
      '您有未保存的修改，确定要离开吗？',
      '未保存的修改',
      {
        confirmButtonText: '离开',
        cancelButtonText: '取消',
        type: 'warning',
      }
    )
      .then(() => {
        router.push('/dashboard')
      })
      .catch(() => {
        // 用户取消离开，不做任何操作
      })
  } else if (activeTab.value === 'password' && passwordFormChanged.value) {
    ElMessageBox.confirm(
      '您有未保存的修改，确定要离开吗？',
      '未保存的修改',
      {
        confirmButtonText: '离开',
        cancelButtonText: '取消',
        type: 'warning',
      }
    )
      .then(() => {
        router.push('/dashboard')
      })
      .catch(() => {
        // 用户取消离开，不做任何操作
      })
  } else {
    router.push('/dashboard')
  }
}

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
          console.log('上传自定义头像:', customAvatarFile.value)
          formData.append('avatar', customAvatarFile.value)
        } else if (selectedDefaultAvatar.value) {
          // 使用默认头像
          console.log('使用默认头像:', selectedDefaultAvatar.value)
          formData.append('avatar', selectedDefaultAvatar.value)
        }
        
        const success = await userStore.updateUserInfo(formData)
        if (success) {
          ElMessage.success('个人信息更新成功')
          formChanged.value = false
          
          // 清空文件输入
          if (fileInput.value) {
            fileInput.value.value = ''
          }
          
          // 重新获取用户信息，确保头像更新
          const updatedUser = await userStore.fetchUserInfo()
          console.log('更新后的用户信息:', updatedUser)
          
          // 更新原始表单数据
          originalFormData.value = { ...basicForm }
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
          passwordFormChanged.value = false
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

// 监听标签页切换
watch(activeTab, (newTab) => {
  // 如果从基本信息切换到密码修改，且有未保存的修改
  if (newTab === 'password' && formChanged.value) {
    ElMessageBox.confirm(
      '您在基本信息中有未保存的修改，确定要切换吗？',
      '未保存的修改',
      {
        confirmButtonText: '切换',
        cancelButtonText: '取消',
        type: 'warning',
      }
    )
      .then(() => {
        // 用户确认切换，不做任何操作
      })
      .catch(() => {
        // 用户取消切换，回到基本信息标签
        activeTab.value = 'basic'
      })
  }
  // 如果从密码修改切换到基本信息，且有未保存的修改
  else if (newTab === 'basic' && passwordFormChanged.value) {
    ElMessageBox.confirm(
      '您在密码修改中有未保存的修改，确定要切换吗？',
      '未保存的修改',
      {
        confirmButtonText: '切换',
        cancelButtonText: '取消',
        type: 'warning',
      }
    )
      .then(() => {
        // 用户确认切换，不做任何操作
      })
      .catch(() => {
        // 用户取消切换，回到密码修改标签
        activeTab.value = 'password'
      })
  }
})
</script>

<style scoped>
.profile-container {
  min-height: 100%;
  background-color: #f5f7fa;
  padding: 24px;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.05);
  overflow-y: auto;
  max-height: calc(100vh - 48px); /* 减去页面上下padding */
}

.page-container {
  height: 100%;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.05);
  padding: 24px;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
  padding-bottom: 16px;
  border-bottom: 1px solid #ebeef5;
}

.page-title {
  margin: 0;
  font-size: 24px;
  font-weight: 600;
  color: #303133;
}

.back-button {
  font-weight: 500;
}

/* 自定义标签页样式 */
.custom-tabs :deep(.el-tabs__header) {
  margin-bottom: 24px;
}

.custom-tabs :deep(.el-tabs__item) {
  font-size: 16px;
  padding: 0 24px;
  height: 48px;
  line-height: 48px;
}

.custom-tabs :deep(.el-tabs__active-bar) {
  height: 3px;
}

.form-container {
  max-width: 800px;
  padding-bottom: 40px;
}

.form-divider {
  height: 1px;
  background-color: #ebeef5;
  margin: 24px 0;
}

.form-section-title {
  font-size: 18px;
  font-weight: 600;
  color: #303133;
  margin-bottom: 20px;
}

.form-row {
  display: flex;
  gap: 20px;
  margin-bottom: 0;
}

.form-item {
  margin-bottom: 24px;
}

.half-width {
  width: calc(50% - 10px);
}

.form-input {
  width: 100%;
}

.form-input :deep(.el-input__inner) {
  height: 40px;
  border-radius: 4px;
}

.disabled-input :deep(.el-input__inner) {
  background-color: #f5f7fa;
  color: #909399;
}

.action-buttons-container {
  margin-top: 32px;
  padding-top: 24px;
  border-top: 1px solid #ebeef5;
}

.form-buttons {
  display: flex;
  justify-content: flex-end;
  gap: 16px;
  width: 100%;
}

.cancel-button, .save-button {
  min-width: 100px;
  height: 40px;
  font-weight: 500;
}

/* 头像相关样式 */
.avatar-form-item {
  margin-bottom: 32px;
}

.avatar-container {
  display: flex;
  flex-direction: column;
  gap: 32px;
}

.current-avatar {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
}

.avatar-preview {
  border: 4px solid #ebeef5;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  background-color: #f5f7fa;
  font-size: 48px;
  font-weight: 600;
  color: #409EFF;
}

.avatar-text {
  font-size: 14px;
  color: #606266;
}

.avatar-options {
  display: flex;
  flex-direction: column;
  gap: 32px;
}

.avatar-section {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.section-title {
  font-size: 16px;
  font-weight: 600;
  color: #303133;
  position: relative;
  padding-left: 12px;
}

.section-title::before {
  content: '';
  position: absolute;
  left: 0;
  top: 50%;
  transform: translateY(-50%);
  width: 4px;
  height: 16px;
  background-color: #409EFF;
  border-radius: 2px;
}

.default-avatars {
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
}

.avatar-item {
  width: 64px;
  height: 64px;
  border-radius: 50%;
  overflow: hidden;
  cursor: pointer;
  border: 3px solid transparent;
  transition: all 0.3s;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.avatar-item:hover {
  transform: scale(1.05);
  box-shadow: 0 4px 16px 0 rgba(0, 0, 0, 0.15);
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
  gap: 12px;
}

.file-upload-wrapper {
  display: inline-block;
}

.upload-button {
  height: 40px;
  font-weight: 500;
}

.selected-file-info {
  font-size: 14px;
  color: #409EFF;
  margin-top: 8px;
  background-color: #ecf5ff;
  padding: 8px 12px;
  border-radius: 4px;
  display: inline-flex;
  align-items: center;
  gap: 8px;
}

.upload-tips {
  font-size: 13px;
  color: #909399;
  display: flex;
  align-items: center;
  gap: 6px;
}

/* 密码表单样式 */
.password-form-header {
  text-align: center;
  margin-bottom: 32px;
  padding: 24px;
  background-color: #f5f7fa;
  border-radius: 8px;
}

.password-icon {
  font-size: 48px;
  color: #409EFF;
  margin-bottom: 16px;
}

.password-form-title {
  font-size: 20px;
  font-weight: 600;
  color: #303133;
  margin-bottom: 8px;
}

.password-form-subtitle {
  font-size: 14px;
  color: #606266;
}

.password-tips {
  font-size: 13px;
  color: #909399;
  margin-top: 16px;
  margin-bottom: 32px;
  padding: 12px 16px;
  background-color: #f5f7fa;
  border-radius: 4px;
  display: flex;
  align-items: center;
  gap: 8px;
}

/* 确保标签页内容可滚动 */
:deep(.el-tabs__content) {
  overflow: visible;
}

:deep(.el-tab-pane) {
  min-height: 200px;
}
</style> 