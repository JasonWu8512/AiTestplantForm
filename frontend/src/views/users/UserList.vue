<template>
  <div class="user-list-container">
    <div class="page-container">
      <div class="title-section">
        <h2 class="page-title">用户管理</h2>
        <p class="page-description">创建和管理系统用户，分配权限和角色</p>
      </div>
      
      <div class="table-operations">
        <el-button type="primary" @click="handleAdd">添加用户</el-button>
        <el-input
          v-model="searchQuery"
          placeholder="搜索用户"
          style="width: 200px; margin-left: 10px;"
          clearable
          @clear="fetchUsers"
          @keyup.enter="fetchUsers"
        >
          <template #suffix>
            <el-icon class="el-input__icon" @click="fetchUsers"><search /></el-icon>
          </template>
        </el-input>
      </div>
      
      <el-table :data="users" border style="width: 100%" v-loading="loading">
        <el-table-column prop="username" label="用户名" width="120" />
        <el-table-column prop="email" label="邮箱" width="180" />
        <el-table-column prop="first_name" label="名" width="100" />
        <el-table-column prop="last_name" label="姓" width="100" />
        <el-table-column prop="department" label="部门" width="120" />
        <el-table-column prop="position" label="职位" width="120" />
        <el-table-column prop="is_active" label="状态" width="80">
          <template #default="scope">
            <el-tag :type="scope.row.is_active ? 'success' : 'danger'">
              {{ scope.row.is_active ? '激活' : '禁用' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="date_joined" label="注册时间" width="180">
          <template #default="scope">
            {{ formatDate(scope.row.date_joined) }}
          </template>
        </el-table-column>
        <el-table-column label="操作" fixed="right" width="150">
          <template #default="scope">
            <el-button type="primary" size="small" @click="handleEdit(scope.row)">编辑</el-button>
            <el-button 
              type="danger" 
              size="small" 
              @click="handleDelete(scope.row)"
              :disabled="scope.row.id === currentUserId"
            >删除</el-button>
          </template>
        </el-table-column>
      </el-table>
      
      <div class="table-pagination">
        <el-pagination
          v-model:current-page="currentPage"
          v-model:page-size="pageSize"
          :page-sizes="[10, 20, 50, 100]"
          layout="total, sizes, prev, pager, next, jumper"
          :total="total"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        />
      </div>
      
      <!-- 用户表单对话框 -->
      <el-dialog
        v-model="dialogVisible"
        :title="dialogType === 'add' ? '添加用户' : '编辑用户'"
        width="500px"
      >
        <el-form ref="userFormRef" :model="userForm" :rules="userRules" label-width="100px">
          <el-form-item label="用户名" prop="username" v-if="dialogType === 'add'">
            <el-input v-model="userForm.username" />
          </el-form-item>
          
          <el-form-item label="邮箱" prop="email">
            <el-input v-model="userForm.email" />
          </el-form-item>
          
          <el-form-item label="姓" prop="last_name">
            <el-input v-model="userForm.last_name" />
          </el-form-item>
          
          <el-form-item label="名" prop="first_name">
            <el-input v-model="userForm.first_name" />
          </el-form-item>
          
          <el-form-item label="手机号" prop="phone">
            <el-input v-model="userForm.phone" />
          </el-form-item>
          
          <el-form-item label="部门" prop="department">
            <el-input v-model="userForm.department" />
          </el-form-item>
          
          <el-form-item label="职位" prop="position">
            <el-input v-model="userForm.position" />
          </el-form-item>
          
          <el-form-item label="状态">
            <el-switch v-model="userForm.is_active" />
          </el-form-item>
          
          <el-form-item label="密码" prop="password" v-if="dialogType === 'add'">
            <el-input v-model="userForm.password" type="password" show-password />
          </el-form-item>
          
          <el-form-item label="确认密码" prop="password2" v-if="dialogType === 'add'">
            <el-input v-model="userForm.password2" type="password" show-password />
          </el-form-item>
        </el-form>
        
        <template #footer>
          <span class="dialog-footer">
            <el-button @click="dialogVisible = false">取消</el-button>
            <el-button type="primary" @click="submitForm" :loading="formLoading">确定</el-button>
          </span>
        </template>
      </el-dialog>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Search } from '@element-plus/icons-vue'
import { useUserStore } from '@/store/user'
import api from '@/api/user'

const userStore = useUserStore()

// 当前用户ID
const currentUserId = computed(() => userStore.user.id)

// 表格数据
const users = ref([])
const loading = ref(false)
const total = ref(0)
const currentPage = ref(1)
const pageSize = ref(10)
const searchQuery = ref('')

// 对话框
const dialogVisible = ref(false)
const dialogType = ref('add') // 'add' 或 'edit'
const userFormRef = ref(null)
const formLoading = ref(false)

// 用户表单
const userForm = reactive({
  id: null,
  username: '',
  email: '',
  first_name: '',
  last_name: '',
  phone: '',
  department: '',
  position: '',
  is_active: true,
  password: '',
  password2: ''
})

// 验证密码是否一致
const validatePass2 = (rule, value, callback) => {
  if (dialogType.value === 'add') {
    if (value === '') {
      callback(new Error('请再次输入密码'))
    } else if (value !== userForm.password) {
      callback(new Error('两次输入密码不一致'))
    } else {
      callback()
    }
  } else {
    callback()
  }
}

// 表单验证规则
const userRules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, max: 20, message: '长度在 3 到 20 个字符', trigger: 'blur' }
  ],
  email: [
    { type: 'email', message: '请输入正确的邮箱地址', trigger: 'blur' }
  ],
  phone: [
    { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号码', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur', required: dialogType.value === 'add' },
    { min: 6, message: '密码长度不能少于6个字符', trigger: 'blur' }
  ],
  password2: [
    { required: true, message: '请再次输入密码', trigger: 'blur', required: dialogType.value === 'add' },
    { validator: validatePass2, trigger: 'blur' }
  ]
}

// 格式化日期
const formatDate = (dateString) => {
  if (!dateString) return ''
  const date = new Date(dateString)
  return date.toLocaleString()
}

// 获取用户列表
const fetchUsers = async () => {
  loading.value = true
  try {
    const params = {
      page: currentPage.value,
      page_size: pageSize.value,
      search: searchQuery.value
    }
    const response = await api.getUserList(params)
    users.value = response.data.results || []
    total.value = response.data.count || 0
  } catch (error) {
    console.error('获取用户列表失败:', error)
    ElMessage.error('获取用户列表失败')
  } finally {
    loading.value = false
  }
}

// 处理页码变化
const handleCurrentChange = (page) => {
  currentPage.value = page
  fetchUsers()
}

// 处理每页条数变化
const handleSizeChange = (size) => {
  pageSize.value = size
  fetchUsers()
}

// 添加用户
const handleAdd = () => {
  dialogType.value = 'add'
  resetForm()
  dialogVisible.value = true
}

// 编辑用户
const handleEdit = (row) => {
  dialogType.value = 'edit'
  resetForm()
  Object.assign(userForm, row)
  dialogVisible.value = true
}

// 删除用户
const handleDelete = (row) => {
  ElMessageBox.confirm(
    `确定要删除用户 ${row.username} 吗？`,
    '警告',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    }
  ).then(async () => {
    try {
      await api.deleteUser(row.id)
      ElMessage.success('删除成功')
      fetchUsers()
    } catch (error) {
      console.error('删除用户失败:', error)
      ElMessage.error('删除用户失败')
    }
  }).catch(() => {})
}

// 重置表单
const resetForm = () => {
  if (userFormRef.value) {
    userFormRef.value.resetFields()
  }
  userForm.id = null
  userForm.username = ''
  userForm.email = ''
  userForm.first_name = ''
  userForm.last_name = ''
  userForm.phone = ''
  userForm.department = ''
  userForm.position = ''
  userForm.is_active = true
  userForm.password = ''
  userForm.password2 = ''
}

// 提交表单
const submitForm = async () => {
  if (!userFormRef.value) return
  
  await userFormRef.value.validate(async (valid) => {
    if (valid) {
      formLoading.value = true
      try {
        if (dialogType.value === 'add') {
          await api.register(userForm)
          ElMessage.success('添加用户成功')
        } else {
          await api.updateUser(userForm.id, userForm)
          ElMessage.success('更新用户成功')
        }
        dialogVisible.value = false
        fetchUsers()
      } catch (error) {
        console.error('操作失败:', error)
        ElMessage.error('操作失败')
      } finally {
        formLoading.value = false
      }
    }
  })
}

// 初始化
onMounted(() => {
  fetchUsers()
})
</script>

<style scoped>
.user-list-container {
  min-height: 100%;
  background-color: #fff;
  padding: 20px;
  border-radius: 4px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.title-section {
  max-width: 70%;
  margin-bottom: 20px;
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
</style> 