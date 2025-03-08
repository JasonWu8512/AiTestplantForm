<template>
  <div class="project-list-container">
    <div class="page-header">
      <h2>项目管理</h2>
      <el-button type="primary" @click="handleAddProject">
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
    
    <!-- 项目列表 -->
    <el-table
      v-loading="loading"
      :data="projectList"
      border
      style="width: 100%"
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
          <el-button size="small" @click="handleViewTestCases(scope.row)">
            查看用例
          </el-button>
          <el-button size="small" type="primary" @click="handleEditProject(scope.row)">
            编辑
          </el-button>
          <el-button 
            size="small" 
            type="danger" 
            @click="handleDeleteProject(scope.row)"
            :disabled="scope.row.status === 'deleted'"
          >
            删除
          </el-button>
        </template>
      </el-table-column>
    </el-table>
    
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
    
    <!-- 项目表单对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="dialogType === 'add' ? '新建项目' : '编辑项目'"
      width="500px"
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
          <el-button type="primary" @click="submitProjectForm">确定</el-button>
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
    const response = await getProjects({
      page: currentPage.value,
      limit: pageSize.value,
      search: searchKeyword.value
    })
    projectList.value = response.data.items
    total.value = response.data.total
  } catch (error) {
    console.error('获取项目列表失败:', error)
    ElMessage.error('获取项目列表失败')
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
        if (dialogType.value === 'add') {
          await createProject(projectForm)
          ElMessage.success('创建成功')
        } else {
          await updateProject(projectForm.id, projectForm)
          ElMessage.success('更新成功')
        }
        dialogVisible.value = false
        fetchProjects()
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
  padding: 20px;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.search-bar {
  display: flex;
  margin-bottom: 20px;
  gap: 10px;
}

.search-bar .el-input {
  width: 300px;
}

.pagination-container {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}
</style> 