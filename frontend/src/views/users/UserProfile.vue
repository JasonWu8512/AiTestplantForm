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
  <div class="profile-wrapper">
    <div class="profile-page">
      <div class="page-header">
        <div class="title-section">
          <h2 class="page-title">个人信息</h2>
          <p class="page-description">查看和编辑个人资料，管理账户信息和安全设置</p>
        </div>
        <el-button @click="handleBack" plain class="back-button">
          <el-icon><ArrowLeft /></el-icon>返回
        </el-button>
      </div>
      
      <div class="content-box">
        <el-tabs v-model="activeTab" class="custom-tabs">
          <el-tab-pane label="基本信息" name="basic">
            <el-form ref="basicFormRef" :model="basicForm" :rules="basicRules" label-width="100px" class="form-container">
              <!-- 头像选择区域 -->
              <el-form-item label="头像" class="avatar-form-item">
                <div class="avatar-container">
                  <div class="avatar-preview-section">
                    <el-avatar :size="120" :src="avatarPreview" class="avatar-preview">{{ userInitials }}</el-avatar>
                    <div class="avatar-actions">
                      <el-button type="primary" size="small" @click="triggerFileInput" class="action-button">
                        <el-icon><Upload /></el-icon> 上传头像
                      </el-button>
                      <input 
                        type="file" 
                        ref="fileInput" 
                        style="display: none" 
                        accept="image/jpeg,image/png,image/gif"
                        @change="handleFileChange"
                      />
                      <el-button v-if="hasCustomAvatar" type="danger" size="small" @click="removeCustomAvatar" class="action-button">
                        <el-icon><Delete /></el-icon> 移除
                      </el-button>
                    </div>
                  </div>
                  
                  <div class="avatar-options">
                    <div class="section-title">选择默认头像</div>
                    <div class="default-avatars-grid">
                      <div 
                        v-for="(avatar, index) in defaultAvatars" 
                        :key="index" 
                        class="avatar-item"
                        :class="{ 'selected': selectedDefaultAvatar === avatar }"
                        @click="selectDefaultAvatar(avatar)"
                      >
                        <img :src="avatar" alt="默认头像" class="avatar-img" />
                        <div class="avatar-check" v-if="selectedDefaultAvatar === avatar">
                          <el-icon><Check /></el-icon>
                        </div>
                      </div>
                    </div>
                    
                    <div class="upload-info" v-if="customAvatarFile">
                      <div class="selected-file-info">
                        <el-icon><Document /></el-icon> 已选择: {{ customAvatarFile.name }}
                      </div>
                      <div class="upload-tips">
                        <el-icon><InfoFilled /></el-icon> 点击"保存"按钮完成上传
                      </div>
                    </div>
                    <div class="upload-tips" v-else>
                      <el-icon><InfoFilled /></el-icon> 支持JPG、PNG、GIF格式，文件大小不超过2MB
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
                <el-icon class="password-icon"><Lock /></el-icon>
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
                >
                  <template #prefix>
                    <el-icon><Key /></el-icon>
                  </template>
                </el-input>
              </el-form-item>
              
              <el-form-item label="新密码" prop="new_password" class="form-item">
                <el-input 
                  v-model="passwordForm.new_password" 
                  type="password" 
                  show-password 
                  @input="passwordFormChanged = true" 
                  class="form-input"
                  placeholder="请输入新密码"
                >
                  <template #prefix>
                    <el-icon><EditPen /></el-icon>
                  </template>
                </el-input>
              </el-form-item>
              
              <el-form-item label="确认新密码" prop="new_password2" class="form-item">
                <el-input 
                  v-model="passwordForm.new_password2" 
                  type="password" 
                  show-password 
                  @input="passwordFormChanged = true" 
                  class="form-input"
                  placeholder="请再次输入新密码"
                >
                  <template #prefix>
                    <el-icon><Check /></el-icon>
                  </template>
                </el-input>
              </el-form-item>
              
              <div class="password-tips">
                <el-icon><InfoFilled /></el-icon> 密码长度不能少于6个字符，建议使用字母、数字和特殊字符的组合
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
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed, watch } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { useUserStore } from '@/store/user'
import { useRouter } from 'vue-router'
import { 
  ArrowLeft, 
  Upload, 
  Delete, 
  Lock, 
  Key, 
  EditPen, 
  Check, 
  InfoFilled,
  Document
} from '@element-plus/icons-vue'

const userStore = useUserStore()
const router = useRouter()
const activeTab = ref('basic')
const fileInput = ref(null)

// 表单修改状态
const formChanged = ref(false)
const passwordFormChanged = ref(false)
const originalFormData = ref({})

// 默认头像列表 - 确保路径格式一致
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
  // 获取用户信息
  const user = await userStore.fetchUserInfo()
  console.log('获取到的用户信息:', user)
  
  if (user) {
    // 填充表单数据
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
      console.log('用户当前头像:', user.avatar)
      
      // 改进的默认头像检测逻辑
      if (user.avatar.startsWith('/avatars/') && 
          (user.avatar.includes('male') || user.avatar.includes('female'))) {
        console.log('检测到默认头像路径:', user.avatar)
        
        // 尝试在默认头像列表中找到匹配项
        const matchedAvatar = defaultAvatars.find(avatar => 
          user.avatar === avatar || user.avatar.includes(avatar.replace('/avatars/', ''))
        )
        
        if (matchedAvatar) {
          console.log('匹配到默认头像:', matchedAvatar)
          selectedDefaultAvatar.value = matchedAvatar
        } else {
          // 如果没有精确匹配，但路径格式正确，使用用户当前头像
          console.log('未找到精确匹配，使用当前头像路径:', user.avatar)
          // 检查是否需要添加前导斜杠
          const normalizedPath = user.avatar.startsWith('/') ? user.avatar : `/${user.avatar}`
          // 查找最接近的默认头像
          const closestMatch = defaultAvatars.find(avatar => 
            normalizedPath.includes('male') && avatar.includes('male') ||
            normalizedPath.includes('female') && avatar.includes('female')
          )
          
          selectedDefaultAvatar.value = closestMatch || defaultAvatars[0]
          console.log('选择的默认头像:', selectedDefaultAvatar.value)
        }
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
  try {
    // 表单验证
    await basicFormRef.value.validate()
    
    // 显示加载状态
    basicLoading.value = true
    
    // 创建FormData对象
    const formData = new FormData()
    
    // 添加基本字段
    formData.append('username', basicForm.username)
    formData.append('email', basicForm.email)
    formData.append('first_name', basicForm.first_name)
    formData.append('last_name', basicForm.last_name)
    formData.append('phone', basicForm.phone || '')
    formData.append('department', basicForm.department || '')
    formData.append('position', basicForm.position || '')
    
    // 处理头像
    if (customAvatarFile.value) {
      // 上传自定义头像
      console.log('上传自定义头像:', customAvatarFile.value)
      formData.append('avatar', customAvatarFile.value)
    } else if (selectedDefaultAvatar.value) {
      // 使用默认头像URL
      console.log('使用默认头像:', selectedDefaultAvatar.value)
      
      // 对于默认头像，我们直接发送一个特殊字段，让后端知道这是默认头像
      // 不再尝试将URL转换为文件对象
      formData.append('use_default_avatar', selectedDefaultAvatar.value.replace('/avatars/', ''));
      
      // 记录日志，帮助调试
      console.log('发送默认头像标识:', selectedDefaultAvatar.value.replace('/avatars/', ''));
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
      
      // 强制刷新头像预览
      if (updatedUser && updatedUser.avatar) {
        // 添加时间戳强制刷新
        const timestamp = new Date().getTime()
        const forceRefreshUrl = updatedUser.avatar.includes('?') 
          ? `${updatedUser.avatar}&_t=${timestamp}` 
          : `${updatedUser.avatar}?_t=${timestamp}`
        
        // 更新头像预览
        avatarPreview.value = forceRefreshUrl
        console.log('强制刷新头像预览:', forceRefreshUrl)
      }
    } else {
      ElMessage.error('个人信息更新失败')
    }
  } catch (error) {
    console.error('更新个人信息出错:', error)
    ElMessage.error('表单验证失败，请检查输入')
  } finally {
    basicLoading.value = false
  }
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

<style>
/* 移除全局样式，使用更具体的选择器 */
</style>

<style scoped>
.profile-wrapper {
  width: 100%;
  min-height: 100vh;
  overflow-y: auto;
  background-color: #f5f7fa;
}

.profile-page {
  padding: 20px;
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 20px;
  width: 100%;
}

.content-box {
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  padding: 24px;
  margin-bottom: 20px;
}

.title-section {
  max-width: 70%;
  margin-bottom: 8px;
}

.page-title {
  font-size: 24px;
  font-weight: 600;
  margin-bottom: 8px;
  position: relative;
  padding-bottom: 10px;
}

.page-title::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  width: 60px;
  height: 3px;
  background: linear-gradient(to right, var(--primary-color, #3498db), var(--primary-light, #2980b9));
  border-radius: 3px;
}

.page-description {
  color: var(--text-secondary, #606266);
  font-size: var(--font-size-md, 14px);
  margin-top: var(--spacing-sm, 8px);
  line-height: 1.5;
}

.back-button {
  display: flex;
  align-items: center;
  gap: 5px;
}

/* 自定义标签页样式 */
.custom-tabs {
  width: 100%;
}

.custom-tabs :deep(.el-tabs__header) {
  margin-bottom: 24px;
  border-bottom: 1px solid #e4e7ed;
  padding-bottom: 0;
}

.custom-tabs :deep(.el-tabs__item) {
  font-size: 16px;
  padding: 0 24px;
  height: 48px;
  line-height: 48px;
}

.custom-tabs :deep(.el-tabs__active-bar) {
  height: 3px;
  background-color: var(--primary-color, #3498db);
}

.custom-tabs :deep(.el-tabs__item.is-active) {
  color: var(--primary-color, #3498db);
  font-weight: 600;
}

.custom-tabs :deep(.el-tabs__content) {
  overflow: visible;
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
  position: relative; /* 确保按钮容器正确定位 */
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
  border-bottom: 1px solid #ebeef5;
  padding-bottom: 32px;
}

.avatar-container {
  display: flex;
  flex-direction: column;
  gap: 32px;
}

.avatar-preview-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
  padding: 20px;
  background-color: #f9fafc;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.05);
}

.avatar-preview {
  border: 4px solid #fff;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  background-color: var(--primary-color, #3498db);
  font-size: 48px;
  font-weight: 600;
  color: #fff;
  transition: all 0.3s ease;
}

.avatar-preview:hover {
  transform: scale(1.05);
}

.avatar-actions {
  display: flex;
  gap: 12px;
}

.action-button {
  height: 36px;
  font-weight: 500;
  border-radius: 4px;
  transition: all 0.3s ease;
}

.avatar-options {
  display: flex;
  flex-direction: column;
  gap: 20px;
  padding: 20px;
  background-color: #f9fafc;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.05);
}

.section-title {
  font-size: 16px;
  font-weight: 600;
  color: #303133;
  position: relative;
  padding-left: 12px;
  margin-bottom: 16px;
}

.section-title::before {
  content: '';
  position: absolute;
  left: 0;
  top: 50%;
  transform: translateY(-50%);
  width: 4px;
  height: 16px;
  background-color: var(--primary-color, #3498db);
  border-radius: 2px;
}

.default-avatars-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
  justify-content: center;
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
  position: relative;
}

.avatar-item:hover {
  transform: scale(1.05);
  box-shadow: 0 4px 16px 0 rgba(0, 0, 0, 0.15);
}

.avatar-item.selected {
  border-color: var(--primary-color, #3498db);
}

.avatar-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.avatar-check {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(52, 152, 219, 0.6);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 24px;
  border-radius: 50%;
}

.selected-file-info {
  font-size: 14px;
  color: var(--primary-color, #3498db);
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
  margin-top: 8px;
}

/* 密码表单样式 */
.password-form-header {
  text-align: center;
  margin-bottom: 32px;
  padding: 32px;
  background-color: #f9fafc;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.05);
}

.password-icon {
  font-size: 48px;
  color: var(--primary-color, #3498db);
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
  padding: 16px;
  background-color: #f9fafc;
  border-radius: 8px;
  display: flex;
  align-items: center;
  gap: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.05);
}

/* 响应式调整 */
@media (max-width: 768px) {
  .form-row {
    flex-direction: column;
    gap: 0;
  }
  
  .half-width {
    width: 100%;
  }
  
  .form-container {
    padding: 0;
  }
}
</style> 