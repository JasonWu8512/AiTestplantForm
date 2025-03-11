<template>
  <div class="project-list-container fullscreen-container">
    <div class="page-header">
      <div class="title-section">
        <h2 class="page-title">项目管理</h2>
        <p class="page-description">创建和管理测试项目，组织测试用例和测试计划</p>
      </div>
      <el-button type="primary" class="ocean-button" @click="handleAddProject">
        <el-icon><Plus /></el-icon>新建项目
      </el-button>
    </div>
    
    <!-- 搜索栏 -->
    <div class="search-bar">
      <el-input
        v-model="searchKeyword"
        placeholder="搜索项目名称或描述"
        clearable
        @clear="handleSearch"
        @keyup.enter="handleSearch"
      >
        <template #append>
          <el-button @click="handleSearch">
            <el-icon><Search /></el-icon>
          </el-button>
        </template>
      </el-input>
      
      <el-select v-model="statusFilter" placeholder="状态" clearable @change="handleSearch">
        <el-option label="活跃" value="active" />
        <el-option label="归档" value="archived" />
        <el-option label="已删除" value="deleted" />
      </el-select>
    </div>
    
    <div class="content-wrapper">
      <!-- 项目列表 -->
      <div class="table-container">
        <el-table
          v-loading="loading"
          :data="projectList"
          border
          style="width: 100%"
          height="100%"
          row-class-name="project-row"
        >
          <el-table-column prop="id" label="ID" width="80" />
          <el-table-column prop="name" label="项目名称" min-width="150" />
          <el-table-column prop="description" label="描述" min-width="200" show-overflow-tooltip />
          <el-table-column prop="status_display" label="状态" width="100">
            <template #default="scope">
              <el-tag :type="getStatusType(scope.row.status)">
                {{ scope.row.status_display || getStatusText(scope.row.status) }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="test_cases_count" label="测试用例数" width="120" />
          <el-table-column prop="creator_name" label="创建者" width="120" />
          <el-table-column prop="created_at" label="创建时间" width="180">
            <template #default="scope">
              {{ formatDate(scope.row.created_at) }}
            </template>
          </el-table-column>
          <el-table-column label="操作" width="250" fixed="right">
            <template #default="scope">
              <el-button size="small" type="default" class="view-btn ocean-button" @click="handleViewTestCases(scope.row)">
                查看用例
              </el-button>
              <el-button size="small" type="primary" class="ocean-button" @click="handleEditProject(scope.row)">
                编辑
              </el-button>
              <el-button 
                size="small" 
                type="danger" 
                class="ocean-button"
                @click="handleDeleteProject(scope.row)"
                :disabled="scope.row.status === 'deleted'"
              >
                删除
              </el-button>
            </template>
          </el-table-column>
        </el-table>
      </div>
      
      <!-- 分页 -->
      <div class="pagination-container">
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
    </div>
    
    <!-- 项目表单对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="dialogType === 'add' ? '新建项目' : '编辑项目'"
      width="500px"
      class="ocean-dialog"
    >
      <el-form
        ref="projectFormRef"
        :model="projectForm"
        :rules="projectRules"
        label-width="100px"
      >
        <el-form-item label="项目名称" prop="name">
          <el-input v-model="projectForm.name" placeholder="请输入项目名称" />
        </el-form-item>
        <el-form-item label="项目描述" prop="description">
          <el-input
            v-model="projectForm.description"
            type="textarea"
            rows="4"
            placeholder="请输入项目描述"
          />
        </el-form-item>
        <el-form-item label="状态" prop="status">
          <el-select v-model="projectForm.status" placeholder="请选择状态">
            <el-option label="活跃" value="active" />
            <el-option label="归档" value="archived" />
            <el-option label="已删除" value="deleted" />
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" class="ocean-button" @click="submitProjectForm">确定</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus, Search } from '@element-plus/icons-vue'
import { useRouter } from 'vue-router'
import { getProjects, createProject, updateProject, deleteProject } from '@/api/testcase'

// 路由
const router = useRouter()

// 数据
const loading = ref(false)
const projectList = ref([])
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(0)
const searchKeyword = ref('')
const statusFilter = ref('')

// 对话框
const dialogVisible = ref(false)
const dialogType = ref('add') // 'add' 或 'edit'
const projectFormRef = ref(null)
const projectForm = reactive({
  id: null,
  name: '',
  description: '',
  status: 'active'
})

// 表单验证规则
const projectRules = {
  name: [
    { required: true, message: '请输入项目名称', trigger: 'blur' },
    { min: 2, max: 100, message: '长度在 2 到 100 个字符', trigger: 'blur' }
  ],
  status: [
    { required: true, message: '请选择状态', trigger: 'change' }
  ]
}

// 生命周期钩子
onMounted(() => {
  fetchProjects()
})

// 方法
/**
 * 获取项目列表
 */
const fetchProjects = async () => {
  loading.value = true
  try {
    const params = {
      page: currentPage.value,
      page_size: pageSize.value,
      search: searchKeyword.value || undefined,
      status: statusFilter.value || undefined
    }
    const response = await getProjects(params)
    
    // 根据实际后端返回的数据结构进行处理
    if (response.results) {
      // 如果后端返回的是 { results: [...], count: ... } 格式
      projectList.value = response.results
      total.value = response.count || 0
    } else if (response.data && response.data.items) {
      // 如果后端返回的是 { data: { items: [...], total: ... } } 格式
      projectList.value = response.data.items
      total.value = response.data.total || 0
    } else if (Array.isArray(response)) {
      // 如果后端直接返回数组
      projectList.value = response
      total.value = response.length
    } else {
      // 其他情况，记录错误并设置为空数组
      console.error('未知的响应格式:', response)
      projectList.value = []
      total.value = 0
    }
    
    console.log('获取到的项目列表:', projectList.value)
  } catch (error) {
    console.error('获取项目列表失败:', error)
    // 不显示错误提示，只在控制台记录错误
    projectList.value = []
    total.value = 0
  } finally {
    loading.value = false
  }
}

/**
 * 处理搜索
 */
const handleSearch = () => {
  currentPage.value = 1
  fetchProjects()
}

/**
 * 处理页码变化
 */
const handleCurrentChange = (val) => {
  currentPage.value = val
  fetchProjects()
}

/**
 * 处理每页条数变化
 */
const handleSizeChange = (val) => {
  pageSize.value = val
  currentPage.value = 1
  fetchProjects()
}

/**
 * 处理添加项目
 */
const handleAddProject = () => {
  dialogType.value = 'add'
  projectForm.id = null
  projectForm.name = ''
  projectForm.description = ''
  projectForm.status = 'active'
  dialogVisible.value = true
}

/**
 * 处理编辑项目
 */
const handleEditProject = (row) => {
  dialogType.value = 'edit'
  projectForm.id = row.id
  projectForm.name = row.name
  projectForm.description = row.description || ''
  projectForm.status = row.status
  dialogVisible.value = true
}

/**
 * 处理删除项目
 */
const handleDeleteProject = (row) => {
  ElMessageBox.confirm(
    '确定要删除该项目吗？删除后不可恢复。',
    '警告',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    }
  ).then(async () => {
    try {
      await deleteProject(row.id)
      ElMessage.success('删除成功')
      fetchProjects()
    } catch (error) {
      console.error('删除项目失败:', error)
      ElMessage.error('删除项目失败')
    }
  }).catch(() => {
    // 取消删除
  })
}

/**
 * 处理查看测试用例
 */
const handleViewTestCases = (row) => {
  router.push({
    name: 'TestCaseList',
    query: { project: row.id }
  })
}

/**
 * 提交项目表单
 */
const submitProjectForm = async () => {
  if (!projectFormRef.value) return
  
  await projectFormRef.value.validate(async (valid) => {
    if (valid) {
      try {
        console.log('提交项目表单:', projectForm)
        
        if (dialogType.value === 'add') {
          const response = await createProject(projectForm)
          console.log('创建项目成功，响应:', response)
          ElMessage.success('创建成功')
        } else {
          const response = await updateProject(projectForm.id, projectForm)
          console.log('更新项目成功，响应:', response)
          ElMessage.success('更新成功')
        }
        
        dialogVisible.value = false
        
        // 确保在关闭对话框后重新获取项目列表
        await fetchProjects()
        console.log('刷新后的项目列表:', projectList.value)
      } catch (error) {
        console.error('保存项目失败:', error)
        ElMessage.error('保存项目失败')
      }
    }
  })
}

/**
 * 获取状态类型
 */
const getStatusType = (status) => {
  const statusMap = {
    active: 'success',
    archived: 'info',
    deleted: 'danger'
  }
  return statusMap[status] || 'info'
}

/**
 * 获取状态文本
 */
const getStatusText = (status) => {
  const statusMap = {
    active: '活跃',
    archived: '归档',
    deleted: '已删除'
  }
  return statusMap[status] || status
}

/**
 * 格式化日期
 */
const formatDate = (dateString) => {
  if (!dateString) return ''
  const date = new Date(dateString)
  return date.toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit'
  })
}
</script>

<style scoped>
.project-list-container {
  /* 移除原有的padding，使用fullscreen-container的padding */
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 20px;
}

.title-section {
  max-width: 70%;
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

.search-bar {
  display: flex;
  margin-bottom: 20px;
  gap: 10px;
}

.search-bar .el-input {
  width: 300px;
}

.project-row {
  transition: background-color 0.3s ease;
  
  &:hover {
    background-color: rgba(240, 247, 255, 0.5) !important;
  }
}

.ocean-dialog {
  .el-dialog__header {
    position: relative;
    
    &::after {
      content: '';
      position: absolute;
      bottom: 0;
      left: 0;
      width: 100%;
      height: 1px;
      background: linear-gradient(to right, transparent, #3498db, transparent);
    }
  }
}

/* 使用fullscreen-container中的pagination-container样式 */

/* 查看按钮样式 */
.view-btn {
  color: #409EFF !important;
  border-color: #409EFF !important;
  font-weight: 500;
}
</style> 