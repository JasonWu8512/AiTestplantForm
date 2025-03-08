<template>
  <div class="testplan-list-container">
    <div class="page-header">
      <h2>测试计划管理</h2>
      <el-button type="primary" @click="handleAddTestPlan">
        <el-icon><Plus /></el-icon>新建测试计划
      </el-button>
    </div>
    
    <!-- 搜索栏 -->
    <div class="search-bar">
      <el-input
        v-model="searchKeyword"
        placeholder="搜索测试计划名称或描述"
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
      
      <el-select v-model="projectFilter" placeholder="选择项目" clearable @change="handleSearch">
        <el-option
          v-for="item in projectOptions"
          :key="item.value"
          :label="item.label"
          :value="item.value"
        />
      </el-select>
      
      <el-select v-model="statusFilter" placeholder="状态" clearable @change="handleSearch">
        <el-option label="草稿" value="draft" />
        <el-option label="就绪" value="ready" />
        <el-option label="进行中" value="in_progress" />
        <el-option label="已完成" value="completed" />
        <el-option label="已归档" value="archived" />
      </el-select>
    </div>
    
    <!-- 测试计划列表 -->
    <el-table
      v-loading="loading"
      :data="testPlanList"
      border
      style="width: 100%"
    >
      <el-table-column prop="id" label="ID" width="80" />
      <el-table-column prop="name" label="计划名称" min-width="150" show-overflow-tooltip />
      <el-table-column prop="description" label="描述" min-width="200" show-overflow-tooltip />
      <el-table-column prop="status_display" label="状态" width="100">
        <template #default="scope">
          <el-tag :type="getStatusType(scope.row.status)">
            {{ scope.row.status_display || getStatusText(scope.row.status) }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="project_name" label="所属项目" width="150" />
      <el-table-column prop="test_cases_count" label="测试用例数" width="120" />
      <el-table-column prop="creator_name" label="创建者" width="120" />
      <el-table-column label="时间范围" width="180">
        <template #default="scope">
          <div v-if="scope.row.start_time || scope.row.end_time">
            {{ formatDate(scope.row.start_time) }} 至 {{ formatDate(scope.row.end_time) }}
          </div>
          <div v-else>未设置</div>
        </template>
      </el-table-column>
      <el-table-column label="操作" width="250" fixed="right">
        <template #default="scope">
          <el-button size="small" @click="handleViewTestPlan(scope.row)">
            查看
          </el-button>
          <el-button size="small" type="primary" @click="handleEditTestPlan(scope.row)">
            编辑
          </el-button>
          <el-button 
            size="small" 
            type="danger" 
            @click="handleDeleteTestPlan(scope.row)"
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
    
    <!-- 测试计划表单对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="dialogType === 'add' ? '新建测试计划' : dialogType === 'edit' ? '编辑测试计划' : '查看测试计划'"
      width="800px"
    >
      <el-form
        ref="testPlanFormRef"
        :model="testPlanForm"
        :rules="testPlanRules"
        label-width="100px"
        :disabled="dialogType === 'view'"
      >
        <el-form-item label="计划名称" prop="name">
          <el-input v-model="testPlanForm.name" placeholder="请输入计划名称" />
        </el-form-item>
        
        <el-form-item label="所属项目" prop="project">
          <el-select v-model="testPlanForm.project" placeholder="请选择项目">
            <el-option
              v-for="item in projectOptions"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            />
          </el-select>
        </el-form-item>
        
        <el-form-item label="状态" prop="status">
          <el-select v-model="testPlanForm.status" placeholder="请选择状态">
            <el-option label="草稿" value="draft" />
            <el-option label="就绪" value="ready" />
            <el-option label="进行中" value="in_progress" />
            <el-option label="已完成" value="completed" />
            <el-option label="已归档" value="archived" />
          </el-select>
        </el-form-item>
        
        <el-form-item label="时间范围">
          <el-date-picker
            v-model="timeRange"
            type="datetimerange"
            range-separator="至"
            start-placeholder="开始时间"
            end-placeholder="结束时间"
            format="YYYY-MM-DD HH:mm:ss"
            value-format="YYYY-MM-DD HH:mm:ss"
          />
        </el-form-item>
        
        <el-form-item label="计划描述" prop="description">
          <el-input
            v-model="testPlanForm.description"
            type="textarea"
            rows="4"
            placeholder="请输入计划描述"
          />
        </el-form-item>
        
        <el-form-item label="测试用例" v-if="dialogType !== 'add'">
          <div class="test-cases-section">
            <div class="test-cases-header">
              <span>已关联测试用例 ({{ testCases.length }})</span>
              <el-button type="primary" size="small" @click="handleAddTestCases" v-if="dialogType === 'edit'">
                添加测试用例
              </el-button>
            </div>
            
            <el-table
              v-loading="testCasesLoading"
              :data="testCases"
              border
              style="width: 100%"
              max-height="300"
              v-if="testCases.length > 0"
            >
              <el-table-column prop="case_detail.id" label="ID" width="80" />
              <el-table-column prop="case_detail.name" label="用例名称" min-width="150" show-overflow-tooltip />
              <el-table-column prop="case_detail.priority_display" label="优先级" width="100">
                <template #default="scope">
                  <el-tag :type="getPriorityType(scope.row.case_detail.priority)">
                    {{ scope.row.case_detail.priority_display }}
                  </el-tag>
                </template>
              </el-table-column>
              <el-table-column prop="order" label="执行顺序" width="100" />
              <el-table-column label="操作" width="150" v-if="dialogType === 'edit'">
                <template #default="scope">
                  <el-button size="small" type="danger" @click="handleRemoveTestCase(scope.row)">
                    移除
                  </el-button>
                </template>
              </el-table-column>
            </el-table>
            
            <div class="no-data" v-else>
              暂无关联的测试用例
            </div>
          </div>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">{{ dialogType === 'view' ? '关闭' : '取消' }}</el-button>
          <el-button type="primary" @click="submitTestPlanForm" v-if="dialogType !== 'view'">确定</el-button>
        </span>
      </template>
    </el-dialog>
    
    <!-- 添加测试用例对话框 -->
    <el-dialog
      v-model="addCasesDialogVisible"
      title="添加测试用例"
      width="800px"
    >
      <div class="search-bar">
        <el-input
          v-model="caseSearchKeyword"
          placeholder="搜索测试用例名称"
          clearable
          @clear="handleCaseSearch"
          @keyup.enter="handleCaseSearch"
        >
          <template #append>
            <el-button @click="handleCaseSearch">
              <el-icon><Search /></el-icon>
            </el-button>
          </template>
        </el-input>
        
        <el-select v-model="casePriorityFilter" placeholder="优先级" clearable @change="handleCaseSearch">
          <el-option label="最高 (P0)" value="P0" />
          <el-option label="高 (P1)" value="P1" />
          <el-option label="中 (P2)" value="P2" />
          <el-option label="低 (P3)" value="P3" />
        </el-select>
      </div>
      
      <el-table
        v-loading="availableCasesLoading"
        :data="availableCases"
        border
        style="width: 100%"
        max-height="400"
        @selection-change="handleSelectionChange"
      >
        <el-table-column type="selection" width="55" />
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
      </el-table>
      
      <div class="pagination-container">
        <el-pagination
          v-model:current-page="casesCurrentPage"
          v-model:page-size="casesPageSize"
          :page-sizes="[10, 20, 50, 100]"
          layout="total, sizes, prev, pager, next, jumper"
          :total="casesTotal"
          @size-change="handleCaseSizeChange"
          @current-change="handleCaseCurrentChange"
        />
      </div>
      
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="addCasesDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="submitAddTestCases" :disabled="selectedCases.length === 0">
            添加所选用例 ({{ selectedCases.length }})
          </el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed, watch } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus, Search } from '@element-plus/icons-vue'
import { useRouter } from 'vue-router'
import { getTestPlans, createTestPlan, updateTestPlan, deleteTestPlan, getTestPlanById, getTestPlanCases, addCasesToTestPlan, removeCaseFromTestPlan } from '@/api/testplan'
import { getProjects, getTestCases } from '@/api/testcase'

// 路由
const router = useRouter()

// 数据
const loading = ref(false)
const testPlanList = ref([])
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(0)
const searchKeyword = ref('')
const statusFilter = ref('')
const projectFilter = ref('')
const projectOptions = ref([])

// 对话框
const dialogVisible = ref(false)
const dialogType = ref('add') // 'add', 'edit', 'view'
const testPlanFormRef = ref(null)
const testPlanForm = reactive({
  id: null,
  name: '',
  description: '',
  status: 'draft',
  project: null,
  start_time: null,
  end_time: null
})
const timeRange = ref([])

// 测试用例相关
const testCases = ref([])
const testCasesLoading = ref(false)
const addCasesDialogVisible = ref(false)
const availableCases = ref([])
const availableCasesLoading = ref(false)
const selectedCases = ref([])
const caseSearchKeyword = ref('')
const casePriorityFilter = ref('')
const casesCurrentPage = ref(1)
const casesPageSize = ref(10)
const casesTotal = ref(0)

// 表单验证规则
const testPlanRules = {
  name: [
    { required: true, message: '请输入计划名称', trigger: 'blur' },
    { min: 2, max: 200, message: '长度在 2 到 200 个字符', trigger: 'blur' }
  ],
  project: [
    { required: true, message: '请选择项目', trigger: 'change' }
  ],
  status: [
    { required: true, message: '请选择状态', trigger: 'change' }
  ]
}

// 监听时间范围变化
watch(timeRange, (newValue) => {
  if (newValue && newValue.length === 2) {
    testPlanForm.start_time = newValue[0]
    testPlanForm.end_time = newValue[1]
  } else {
    testPlanForm.start_time = null
    testPlanForm.end_time = null
  }
})

// 生命周期钩子
onMounted(async () => {
  // 加载项目选项
  await loadProjectOptions()
  
  // 加载测试计划列表
  fetchTestPlans()
})

// 方法
/**
 * 加载项目选项
 */
const loadProjectOptions = async () => {
  try {
    const response = await getProjects()
    projectOptions.value = response.data.items.map(project => ({
      value: project.id,
      label: project.name
    }))
  } catch (error) {
    console.error('加载项目选项失败:', error)
    ElMessage.error('加载项目选项失败')
  }
}

/**
 * 获取测试计划列表
 */
const fetchTestPlans = async () => {
  loading.value = true
  try {
    const params = {
      page: currentPage.value,
      limit: pageSize.value,
      search: searchKeyword.value
    }
    
    if (projectFilter.value) {
      params.project_id = projectFilter.value
    }
    
    if (statusFilter.value) {
      params.status = statusFilter.value
    }
    
    const response = await getTestPlans(params)
    testPlanList.value = response.data.items
    total.value = response.data.total
  } catch (error) {
    console.error('获取测试计划列表失败:', error)
    ElMessage.error('获取测试计划列表失败')
  } finally {
    loading.value = false
  }
}

/**
 * 处理搜索
 */
const handleSearch = () => {
  currentPage.value = 1
  fetchTestPlans()
}

/**
 * 处理页码变化
 */
const handleCurrentChange = (val) => {
  currentPage.value = val
  fetchTestPlans()
}

/**
 * 处理每页条数变化
 */
const handleSizeChange = (val) => {
  pageSize.value = val
  currentPage.value = 1
  fetchTestPlans()
}

/**
 * 处理添加测试计划
 */
const handleAddTestPlan = () => {
  dialogType.value = 'add'
  testPlanForm.id = null
  testPlanForm.name = ''
  testPlanForm.description = ''
  testPlanForm.status = 'draft'
  testPlanForm.project = null
  testPlanForm.start_time = null
  testPlanForm.end_time = null
  timeRange.value = []
  testCases.value = []
  
  dialogVisible.value = true
}

/**
 * 处理查看测试计划
 */
const handleViewTestPlan = (row) => {
  dialogType.value = 'view'
  loadTestPlanDetail(row.id)
}

/**
 * 处理编辑测试计划
 */
const handleEditTestPlan = (row) => {
  dialogType.value = 'edit'
  loadTestPlanDetail(row.id)
}

/**
 * 加载测试计划详情
 */
const loadTestPlanDetail = async (id) => {
  try {
    const response = await getTestPlanById(id)
    const testPlan = response.data
    
    // 填充表单
    testPlanForm.id = testPlan.id
    testPlanForm.name = testPlan.name
    testPlanForm.description = testPlan.description
    testPlanForm.project_id = testPlan.project_id
    testPlanForm.status = testPlan.status
    testPlanForm.start_date = testPlan.start_date
    testPlanForm.end_date = testPlan.end_date
    
    // 加载测试用例
    loadTestCases(id)
  } catch (error) {
    ElMessage.error('获取测试计划详情失败')
    console.error(error)
  }
}

/**
 * 加载测试用例
 */
const loadTestCases = async (planId) => {
  testCasesLoading.value = true
  try {
    const response = await getTestPlanCases(planId)
    testCases.value = response.data.items || []
  } catch (error) {
    ElMessage.error('获取测试用例失败')
    console.error(error)
  } finally {
    testCasesLoading.value = false
  }
}

/**
 * 处理删除测试计划
 */
const handleDeleteTestPlan = (row) => {
  ElMessageBox.confirm(
    '确定要删除该测试计划吗？删除后不可恢复。',
    '警告',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    }
  ).then(async () => {
    try {
      await deleteTestPlan(row.id)
      ElMessage.success('删除成功')
      fetchTestPlans()
    } catch (error) {
      console.error('删除测试计划失败:', error)
      ElMessage.error('删除测试计划失败')
    }
  }).catch(() => {
    // 取消删除
  })
}

/**
 * 提交测试计划表单
 */
const submitTestPlanForm = async () => {
  if (!testPlanFormRef.value) return
  
  await testPlanFormRef.value.validate(async (valid) => {
    if (valid) {
      try {
        if (dialogType.value === 'add') {
          await createTestPlan(testPlanForm)
          ElMessage.success('创建成功')
        } else {
          await updateTestPlan(testPlanForm.id, testPlanForm)
          ElMessage.success('更新成功')
        }
        dialogVisible.value = false
        fetchTestPlans()
      } catch (error) {
        console.error('保存测试计划失败:', error)
        ElMessage.error('保存测试计划失败')
      }
    }
  })
}

/**
 * 处理添加测试用例
 */
const handleAddTestCases = () => {
  // 重置搜索条件
  caseSearchKeyword.value = ''
  casePriorityFilter.value = ''
  casesCurrentPage.value = 1
  selectedCases.value = []
  
  // 加载可用的测试用例
  fetchAvailableCases()
  
  addCasesDialogVisible.value = true
}

/**
 * 获取可用的测试用例
 */
const fetchAvailableCases = async () => {
  availableCasesLoading.value = true
  try {
    const params = {
      page: casesCurrentPage.value,
      page_size: casesPageSize.value,
      project: testPlanForm.project,
      status: 'active'
    }
    
    if (caseSearchKeyword.value) {
      params.search = caseSearchKeyword.value
    }
    
    if (casePriorityFilter.value) {
      params.priority = casePriorityFilter.value
    }
    
    const response = await getTestCases(params)
    
    // 过滤掉已经关联的测试用例
    const existingCaseIds = testCases.value.map(item => item.case_detail.id)
    availableCases.value = (response.data.results || response.data).filter(
      item => !existingCaseIds.includes(item.id)
    )
    
    casesTotal.value = response.data.count || availableCases.value.length
  } catch (error) {
    console.error('获取可用测试用例失败:', error)
    ElMessage.error('获取可用测试用例失败')
  } finally {
    availableCasesLoading.value = false
  }
}

/**
 * 处理测试用例搜索
 */
const handleCaseSearch = () => {
  casesCurrentPage.value = 1
  fetchAvailableCases()
}

/**
 * 处理测试用例页码变化
 */
const handleCaseCurrentChange = (val) => {
  casesCurrentPage.value = val
  fetchAvailableCases()
}

/**
 * 处理测试用例每页条数变化
 */
const handleCaseSizeChange = (val) => {
  casesPageSize.value = val
  casesCurrentPage.value = 1
  fetchAvailableCases()
}

/**
 * 处理选择变化
 */
const handleSelectionChange = (selection) => {
  selectedCases.value = selection
}

/**
 * 提交添加测试用例
 */
const submitAddTestCases = async () => {
  if (selectedCases.value.length === 0) return
  
  try {
    const caseIds = selectedCases.value.map(item => item.id)
    await addCasesToTestPlan(testPlanForm.id, { case_ids: caseIds })
    ElMessage.success('添加成功')
    addCasesDialogVisible.value = false
    
    // 重新加载测试用例
    loadTestCases(testPlanForm.id)
  } catch (error) {
    console.error('添加测试用例失败:', error)
    ElMessage.error('添加测试用例失败')
  }
}

/**
 * 处理移除测试用例
 */
const handleRemoveTestCase = (row) => {
  ElMessageBox.confirm(
    '确定要从测试计划中移除该测试用例吗？',
    '警告',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    }
  ).then(async () => {
    try {
      await removeCaseFromTestPlan(testPlanForm.id, row.case_detail.id)
      ElMessage.success('移除成功')
      
      // 重新加载测试用例
      loadTestCases(testPlanForm.id)
    } catch (error) {
      console.error('移除测试用例失败:', error)
      ElMessage.error('移除测试用例失败')
    }
  }).catch(() => {
    // 取消移除
  })
}

/**
 * 获取状态类型
 */
const getStatusType = (status) => {
  const statusMap = {
    draft: 'info',
    ready: 'warning',
    in_progress: 'primary',
    completed: 'success',
    archived: 'danger'
  }
  return statusMap[status] || 'info'
}

/**
 * 获取状态文本
 */
const getStatusText = (status) => {
  const statusMap = {
    draft: '草稿',
    ready: '就绪',
    in_progress: '进行中',
    completed: '已完成',
    archived: '已归档'
  }
  return statusMap[status] || status
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
    minute: '2-digit'
  })
}
</script>

<style scoped>
.testplan-list-container {
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

.test-cases-section {
  border: 1px solid #ebeef5;
  border-radius: 4px;
  padding: 10px;
}

.test-cases-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.no-data {
  text-align: center;
  color: #909399;
  padding: 20px 0;
}
</style> 