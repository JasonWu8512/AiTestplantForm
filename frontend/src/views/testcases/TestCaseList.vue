<template>
  <div class="testcase-list-container fullscreen-container">
    <div class="page-header">
      <div class="title-section">
        <h2>测试用例管理</h2>
        <span v-if="currentProject" class="project-name">
          项目：{{ currentProject.name }}
        </span>
      </div>
      <div class="button-group">
        <el-button @click="handleBackToProjects" v-if="currentProject">
          <el-icon><Back /></el-icon>返回项目列表
        </el-button>
        <el-button type="primary" @click="handleAddTestCase">
          <el-icon><Plus /></el-icon>新建测试用例
        </el-button>
        <el-dropdown @command="handleImportExport">
          <el-button type="success">
            <el-icon><Upload /></el-icon>导入/导出
            <el-icon class="el-icon--right"><ArrowDown /></el-icon>
          </el-button>
          <template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item command="import">导入测试用例</el-dropdown-item>
              <el-dropdown-item command="export">导出测试用例</el-dropdown-item>
            </el-dropdown-menu>
          </template>
        </el-dropdown>
      </div>
    </div>
    
    <!-- 搜索栏 -->
    <div class="search-bar">
      <el-input
        v-model="searchKeyword"
        placeholder="搜索测试用例名称或描述"
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
      
      <el-select 
        v-model="projectFilter" 
        placeholder="选择项目" 
        clearable 
        @change="handleSearch"
        v-if="!currentProject"
      >
        <el-option
          v-for="item in projectOptions"
          :key="item.value"
          :label="item.label"
          :value="item.value"
        />
      </el-select>
      
      <el-select v-model="priorityFilter" placeholder="优先级" clearable @change="handleSearch">
        <el-option label="最高 (P0)" value="P0" />
        <el-option label="高 (P1)" value="P1" />
        <el-option label="中 (P2)" value="P2" />
        <el-option label="低 (P3)" value="P3" />
      </el-select>
      
      <el-select v-model="statusFilter" placeholder="状态" clearable @change="handleSearch">
        <el-option label="草稿" value="draft" />
        <el-option label="活跃" value="active" />
        <el-option label="废弃" value="deprecated" />
        <el-option label="已删除" value="deleted" />
      </el-select>
    </div>
    
    <div class="content-wrapper">
      <!-- 测试用例列表 -->
      <div class="table-container">
        <el-table
          v-loading="loading"
          :data="testCaseList"
          border
          style="width: 100%"
          height="100%"
        >
          <el-table-column prop="id" label="ID" width="80" />
          <el-table-column prop="name" label="用例名称" min-width="150" show-overflow-tooltip />
          <el-table-column prop="priority_display" label="优先级" width="100">
            <template #default="scope">
              <el-tag :type="getPriorityType(scope.row.priority)">
                {{ scope.row.priority_display || getPriorityText(scope.row.priority) }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="status_display" label="状态" width="100">
            <template #default="scope">
              <el-tag :type="getStatusType(scope.row.status)">
                {{ scope.row.status_display || getStatusText(scope.row.status) }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="project_name" label="所属项目" width="150" v-if="!currentProject" />
          <el-table-column prop="creator_name" label="创建者" width="120" />
          <el-table-column prop="created_at" label="创建时间" width="180">
            <template #default="scope">
              {{ formatDate(scope.row.created_at) }}
            </template>
          </el-table-column>
          <el-table-column label="操作" width="200" fixed="right">
            <template #default="scope">
              <el-button size="small" @click="handleViewTestCase(scope.row)">
                查看
              </el-button>
              <el-button size="small" type="primary" @click="handleEditTestCase(scope.row)">
                编辑
              </el-button>
              <el-button 
                size="small" 
                type="danger" 
                @click="handleDeleteTestCase(scope.row)"
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
    
    <!-- 测试用例表单对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="dialogType === 'add' ? '新建测试用例' : dialogType === 'edit' ? '编辑测试用例' : '查看测试用例'"
      width="800px"
    >
      <el-form
        ref="testCaseFormRef"
        :model="testCaseForm"
        :rules="testCaseRules"
        label-width="100px"
        :disabled="dialogType === 'view'"
      >
        <el-form-item label="用例名称" prop="name">
          <el-input v-model="testCaseForm.name" placeholder="请输入用例名称" />
        </el-form-item>
        
        <el-form-item label="所属项目" prop="project" v-if="!currentProject">
          <el-select v-model="testCaseForm.project" placeholder="请选择项目">
            <el-option
              v-for="item in projectOptions"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            />
          </el-select>
        </el-form-item>
        
        <el-form-item label="优先级" prop="priority">
          <el-select v-model="testCaseForm.priority" placeholder="请选择优先级">
            <el-option label="最高 (P0)" value="P0" />
            <el-option label="高 (P1)" value="P1" />
            <el-option label="中 (P2)" value="P2" />
            <el-option label="低 (P3)" value="P3" />
          </el-select>
        </el-form-item>
        
        <el-form-item label="状态" prop="status">
          <el-select v-model="testCaseForm.status" placeholder="请选择状态">
            <el-option label="草稿" value="draft" />
            <el-option label="活跃" value="active" />
            <el-option label="废弃" value="deprecated" />
            <el-option label="已删除" value="deleted" />
          </el-select>
        </el-form-item>
        
        <el-form-item label="用例描述" prop="description">
          <el-input
            v-model="testCaseForm.description"
            type="textarea"
            rows="3"
            placeholder="请输入用例描述"
          />
        </el-form-item>
        
        <el-form-item label="测试步骤" prop="steps">
          <el-input
            v-model="testCaseForm.steps"
            type="textarea"
            rows="5"
            placeholder="请输入测试步骤"
          />
        </el-form-item>
        
        <el-form-item label="预期结果" prop="expected_results">
          <el-input
            v-model="testCaseForm.expected_results"
            type="textarea"
            rows="5"
            placeholder="请输入预期结果"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">{{ dialogType === 'view' ? '关闭' : '取消' }}</el-button>
          <el-button type="primary" @click="submitTestCaseForm" v-if="dialogType !== 'view'">确定</el-button>
        </span>
      </template>
    </el-dialog>
    
    <!-- 导入对话框 -->
    <el-dialog
      v-model="importDialogVisible"
      title="导入测试用例"
      width="500px"
    >
      <el-form
        ref="importFormRef"
        :model="importForm"
        :rules="importRules"
        label-width="100px"
      >
        <el-form-item label="所属项目" prop="project" v-if="!currentProject">
          <el-select v-model="importForm.project" placeholder="请选择项目">
            <el-option
              v-for="item in projectOptions"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            />
          </el-select>
        </el-form-item>
        
        <el-form-item label="文件" prop="file">
          <el-upload
            ref="uploadRef"
            action="#"
            :auto-upload="false"
            :limit="1"
            :on-change="handleFileChange"
            :on-remove="handleFileRemove"
            accept=".csv,.xlsx,.xls"
          >
            <el-button type="primary">选择文件</el-button>
            <template #tip>
              <div class="el-upload__tip">
                请上传CSV或Excel文件，大小不超过10MB
              </div>
            </template>
          </el-upload>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="importDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="submitImportForm">确定</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus, Search, Upload, ArrowDown, Back } from '@element-plus/icons-vue'
import { useRouter, useRoute } from 'vue-router'
import { getProjects, getTestCases, createTestCase, updateTestCase, deleteTestCase, importTestCases, exportTestCases, getProject, getTestCase } from '@/api/testcase'

// 路由
const router = useRouter()
const route = useRoute()

// 数据
const loading = ref(false)
const testCaseList = ref([])
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(0)
const searchKeyword = ref('')
const priorityFilter = ref('')
const statusFilter = ref('')
const projectFilter = ref('')
const projectOptions = ref([])
const currentProject = ref(null)

// 对话框
const dialogVisible = ref(false)
const dialogType = ref('add') // 'add', 'edit', 'view'
const testCaseFormRef = ref(null)
const testCaseForm = reactive({
  id: null,
  name: '',
  description: '',
  priority: 'P2',
  status: 'draft',
  steps: '',
  expected_results: '',
  project: null
})

// 导入对话框
const importDialogVisible = ref(false)
const importFormRef = ref(null)
const uploadRef = ref(null)
const importForm = reactive({
  project: null,
  file: null
})

// 表单验证规则
const testCaseRules = {
  name: [
    { required: true, message: '请输入用例名称', trigger: 'blur' },
    { min: 2, max: 200, message: '长度在 2 到 200 个字符', trigger: 'blur' }
  ],
  project: [
    { required: true, message: '请选择项目', trigger: 'change' }
  ],
  priority: [
    { required: true, message: '请选择优先级', trigger: 'change' }
  ],
  status: [
    { required: true, message: '请选择状态', trigger: 'change' }
  ],
  steps: [
    { required: true, message: '请输入测试步骤', trigger: 'blur' }
  ],
  expected_results: [
    { required: true, message: '请输入预期结果', trigger: 'blur' }
  ]
}

// 导入表单验证规则
const importRules = {
  project: [
    { required: true, message: '请选择项目', trigger: 'change' }
  ],
  file: [
    { required: true, message: '请选择文件', trigger: 'change' }
  ]
}

// 计算属性
const projectId = computed(() => {
  return route.query.project ? parseInt(route.query.project) : null
})

// 生命周期钩子
onMounted(async () => {
  // 加载项目选项
  await loadProjectOptions()
  
  // 如果URL中有项目ID，则加载该项目信息
  if (projectId.value) {
    await loadProjectInfo(projectId.value)
  }
  
  // 加载测试用例列表
  fetchTestCases()
})

// 方法
/**
 * 加载项目选项
 */
const loadProjectOptions = async () => {
  try {
    console.log('加载项目选项')
    const response = await getProjects()
    console.log('项目选项响应:', response)
    
    // 根据实际后端返回的数据结构进行处理
    let projects = []
    
    if (response.results) {
      // 如果后端返回的是 { results: [...], count: ... } 格式
      projects = response.results
    } else if (response.data && response.data.items) {
      // 如果后端返回的是 { data: { items: [...], total: ... } } 格式
      projects = response.data.items
    } else if (Array.isArray(response)) {
      // 如果后端直接返回数组
      projects = response
    } else {
      console.error('未知的响应格式:', response)
      projects = []
    }
    
    projectOptions.value = projects.map(project => ({
      value: project.id,
      label: project.name
    }))
    
    console.log('处理后的项目选项:', projectOptions.value)
  } catch (error) {
    console.error('加载项目选项失败:', error)
    projectOptions.value = []
    ElMessage.error('加载项目选项失败')
  }
}

/**
 * 加载项目信息
 */
const loadProjectInfo = async (id) => {
  try {
    console.log('加载项目信息，ID:', id)
    const response = await getProject(id)
    console.log('项目信息响应:', response)
    
    // 根据实际后端返回的数据结构进行处理
    if (response) {
      currentProject.value = response
      // 设置项目过滤器
      projectFilter.value = id
    } else {
      console.error('项目信息为空')
      ElMessage.warning('无法加载项目信息')
    }
  } catch (error) {
    console.error('加载项目信息失败:', error)
    ElMessage.error('加载项目信息失败')
    // 导航回项目列表
    router.push('/projects')
  }
}

/**
 * 获取测试用例列表
 */
const fetchTestCases = async () => {
  loading.value = true
  try {
    const params = {
      page: currentPage.value,
      page_size: pageSize.value,
      search: searchKeyword.value || undefined
    }
    
    if (priorityFilter.value) {
      params.priority = priorityFilter.value
    }
    
    if (statusFilter.value) {
      params.status = statusFilter.value
    }
    
    if (currentProject.value) {
      params.project_id = currentProject.value.id
    } else if (projectFilter.value) {
      params.project_id = projectFilter.value
    }
    
    console.log('获取测试用例列表，参数:', params)
    const response = await getTestCases(params)
    console.log('测试用例列表响应:', response)
    
    // 根据实际后端返回的数据结构进行处理
    if (response.results) {
      // 如果后端返回的是 { results: [...], count: ... } 格式
      testCaseList.value = response.results
      total.value = response.count || 0
    } else if (response.data && response.data.items) {
      // 如果后端返回的是 { data: { items: [...], total: ... } } 格式
      testCaseList.value = response.data.items
      total.value = response.data.total || 0
    } else if (Array.isArray(response)) {
      // 如果后端直接返回数组
      testCaseList.value = response
      total.value = response.length
    } else {
      // 其他情况，记录错误并设置为空数组
      console.error('未知的响应格式:', response)
      testCaseList.value = []
      total.value = 0
    }
    
    console.log('处理后的测试用例列表:', testCaseList.value)
  } catch (error) {
    console.error('获取测试用例列表失败:', error)
    testCaseList.value = []
    total.value = 0
    ElMessage.error('获取测试用例列表失败')
  } finally {
    loading.value = false
  }
}

/**
 * 处理搜索
 */
const handleSearch = () => {
  currentPage.value = 1
  fetchTestCases()
}

/**
 * 处理页码变化
 */
const handleCurrentChange = (val) => {
  currentPage.value = val
  fetchTestCases()
}

/**
 * 处理每页条数变化
 */
const handleSizeChange = (val) => {
  pageSize.value = val
  currentPage.value = 1
  fetchTestCases()
}

/**
 * 处理返回项目列表
 */
const handleBackToProjects = () => {
  router.push({ name: 'ProjectList' })
}

/**
 * 处理添加测试用例
 */
const handleAddTestCase = () => {
  dialogType.value = 'add'
  testCaseForm.id = null
  testCaseForm.name = ''
  testCaseForm.description = ''
  testCaseForm.priority = 'P2'
  testCaseForm.status = 'draft'
  testCaseForm.steps = ''
  testCaseForm.expected_results = ''
  
  // 如果有当前项目，则设置为当前项目
  if (currentProject.value) {
    testCaseForm.project = currentProject.value.id
  } else {
    testCaseForm.project = null
  }
  
  dialogVisible.value = true
}

/**
 * 处理查看测试用例
 */
const handleViewTestCase = (row) => {
  dialogType.value = 'view'
  loadTestCaseDetail(row.id)
}

/**
 * 处理编辑测试用例
 */
const handleEditTestCase = (row) => {
  dialogType.value = 'edit'
  loadTestCaseDetail(row.id)
}

/**
 * 加载测试用例详情
 */
const loadTestCaseDetail = async (id) => {
  try {
    console.log('加载测试用例详情，ID:', id)
    const response = await getTestCase(id)
    console.log('测试用例详情响应:', response)
    
    // 根据实际后端返回的数据结构进行处理
    if (response) {
      testCaseForm.id = response.id
      testCaseForm.name = response.name
      testCaseForm.description = response.description || ''
      testCaseForm.priority = response.priority
      testCaseForm.status = response.status
      testCaseForm.steps = response.steps
      testCaseForm.expected_results = response.expected_results
      testCaseForm.project = response.project
      
      dialogVisible.value = true
    } else {
      console.error('测试用例详情为空')
      ElMessage.warning('无法加载测试用例详情')
    }
  } catch (error) {
    console.error('加载测试用例详情失败:', error)
    ElMessage.error('加载测试用例详情失败')
  }
}

/**
 * 处理删除测试用例
 */
const handleDeleteTestCase = (row) => {
  ElMessageBox.confirm(
    '确定要删除该测试用例吗？删除后不可恢复。',
    '警告',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    }
  ).then(async () => {
    try {
      await deleteTestCase(row.id)
      ElMessage.success('删除成功')
      fetchTestCases()
    } catch (error) {
      console.error('删除测试用例失败:', error)
      ElMessage.error('删除测试用例失败')
    }
  }).catch(() => {
    // 取消删除
  })
}

/**
 * 提交测试用例表单
 */
const submitTestCaseForm = async () => {
  if (!testCaseFormRef.value) return
  
  await testCaseFormRef.value.validate(async (valid) => {
    if (valid) {
      try {
        if (dialogType.value === 'add') {
          await createTestCase(testCaseForm)
          ElMessage.success('创建成功')
        } else {
          await updateTestCase(testCaseForm.id, testCaseForm)
          ElMessage.success('更新成功')
        }
        dialogVisible.value = false
        fetchTestCases()
      } catch (error) {
        console.error('保存测试用例失败:', error)
        ElMessage.error('保存测试用例失败')
      }
    }
  })
}

/**
 * 处理导入/导出
 */
const handleImportExport = (command) => {
  if (command === 'import') {
    // 重置导入表单
    importForm.file = null
    if (uploadRef.value) {
      uploadRef.value.clearFiles()
    }
    
    // 如果有当前项目，则设置为当前项目
    if (currentProject.value) {
      importForm.project = currentProject.value.id
    } else {
      importForm.project = null
    }
    
    importDialogVisible.value = true
  } else if (command === 'export') {
    handleExportTestCases()
  }
}

/**
 * 处理文件变更
 */
const handleFileChange = (file) => {
  importForm.file = file.raw
}

/**
 * 处理文件移除
 */
const handleFileRemove = () => {
  importForm.file = null
}

/**
 * 提交导入表单
 */
const submitImportForm = async () => {
  if (!importFormRef.value) return
  
  await importFormRef.value.validate(async (valid) => {
    if (valid) {
      try {
        const formData = new FormData()
        formData.append('file', importForm.file)
        
        // 如果有当前项目，则使用当前项目ID
        if (currentProject.value) {
          formData.append('project_id', currentProject.value.id)
        } else {
          formData.append('project_id', importForm.project)
        }
        
        const response = await importTestCases(formData)
        ElMessage.success(response.data.message || '导入成功')
        importDialogVisible.value = false
        fetchTestCases()
      } catch (error) {
        console.error('导入测试用例失败:', error)
        ElMessage.error('导入测试用例失败')
      }
    }
  })
}

/**
 * 处理导出测试用例
 */
const handleExportTestCases = async () => {
  try {
    const params = {}
    
    // 应用当前的过滤条件
    if (searchKeyword.value) {
      params.search = searchKeyword.value
    }
    
    if (priorityFilter.value) {
      params.priority = priorityFilter.value
    }
    
    if (statusFilter.value) {
      params.status = statusFilter.value
    }
    
    // 如果有当前项目或者选择了项目过滤器
    if (currentProject.value) {
      params.project_id = currentProject.value.id
    } else if (projectFilter.value) {
      params.project_id = projectFilter.value
    }
    
    const response = await exportTestCases(params)
    
    // 创建Blob对象
    const blob = new Blob([response.data], { type: 'application/vnd.ms-excel' })
    
    // 创建下载链接
    const link = document.createElement('a')
    link.href = URL.createObjectURL(blob)
    link.download = 'test_cases.xlsx'
    link.click()
    
    // 释放URL对象
    URL.revokeObjectURL(link.href)
    
    ElMessage.success('导出成功')
  } catch (error) {
    console.error('导出测试用例失败:', error)
    ElMessage.error('导出测试用例失败')
  }
}

/**
 * 获取优先级类型
 */
const getPriorityType = (priority) => {
  const priorityMap = {
    P0: 'danger',
    P1: 'warning',
    P2: 'success',
    P3: 'info'
  }
  return priorityMap[priority] || 'info'
}

/**
 * 获取优先级文本
 */
const getPriorityText = (priority) => {
  const priorityMap = {
    P0: '最高',
    P1: '高',
    P2: '中',
    P3: '低'
  }
  return priorityMap[priority] || priority
}

/**
 * 获取状态类型
 */
const getStatusType = (status) => {
  const statusMap = {
    draft: 'info',
    active: 'success',
    deprecated: 'warning',
    deleted: 'danger'
  }
  return statusMap[status] || 'info'
}

/**
 * 获取状态文本
 */
const getStatusText = (status) => {
  const statusMap = {
    draft: '草稿',
    active: '活跃',
    deprecated: '废弃',
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
.testcase-list-container {
  /* 移除原有的padding，使用fullscreen-container的padding */
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.title-section {
  display: flex;
  align-items: center;
}

.project-name {
  margin-left: 15px;
  font-size: 16px;
  color: #606266;
}

.button-group {
  display: flex;
  gap: 10px;
}

.search-bar {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-bottom: 20px;
  background-color: #f5f7fa;
  padding: 15px;
  border-radius: 4px;
}

.content-wrapper {
  display: flex;
  flex-direction: column;
  height: 100%;
}

.table-container {
  flex: 1;
  margin-bottom: 20px;
}

.pagination-container {
  display: flex;
  justify-content: flex-end;
}
</style> 