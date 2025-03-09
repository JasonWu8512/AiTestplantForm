<template>
  <div class="execution-list-container fullscreen-container">
    <div class="execution-header">
      <h2 class="page-title">测试执行管理</h2>
      <div class="execution-actions">
        <el-button type="primary" class="ocean-button" @click="handleCreateFromPlan">从测试计划创建</el-button>
      </div>
    </div>

    <!-- 搜索区域 -->
    <div class="search-container">
      <el-form :inline="true" :model="searchForm" class="search-form">
        <el-form-item label="测试计划">
          <el-input v-model="searchForm.planName" placeholder="测试计划名称" clearable></el-input>
        </el-form-item>
        <el-form-item label="状态">
          <el-select v-model="searchForm.status" placeholder="执行状态" clearable>
            <el-option label="待执行" value="pending"></el-option>
            <el-option label="执行中" value="running"></el-option>
            <el-option label="已暂停" value="paused"></el-option>
            <el-option label="已完成" value="completed"></el-option>
            <el-option label="已中止" value="aborted"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" class="ocean-button" @click="handleSearch">搜索</el-button>
          <el-button class="ocean-button" @click="resetSearch">重置</el-button>
        </el-form-item>
      </el-form>
    </div>

    <div class="content-wrapper">
      <!-- 测试执行列表 -->
      <div class="table-container">
        <el-table
          v-loading="loading"
          :data="executionList"
          border
          style="width: 100%"
          height="100%"
          @row-click="handleRowClick"
          row-class-name="execution-row"
        >
          <el-table-column prop="id" label="ID" width="80"></el-table-column>
          <el-table-column prop="plan.name" label="测试计划" min-width="180"></el-table-column>
          <el-table-column prop="executor.username" label="执行者" width="120"></el-table-column>
          <el-table-column prop="status_display" label="状态" width="100">
            <template #default="scope">
              <el-tag :type="getStatusType(scope.row.status)">{{ scope.row.status_display }}</el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="start_time" label="开始时间" width="180">
            <template #default="scope">
              {{ scope.row.start_time ? formatDateTime(scope.row.start_time) : '-' }}
            </template>
          </el-table-column>
          <el-table-column prop="end_time" label="结束时间" width="180">
            <template #default="scope">
              {{ scope.row.end_time ? formatDateTime(scope.row.end_time) : '-' }}
            </template>
          </el-table-column>
          <el-table-column label="操作" width="280" fixed="right">
            <template #default="scope">
              <el-button
                v-if="scope.row.status === 'pending'"
                type="success"
                size="small"
                class="ocean-button"
                @click.stop="handleStart(scope.row)"
              >
                开始执行
              </el-button>
              <el-button
                v-if="scope.row.status === 'running'"
                type="warning"
                size="small"
                class="ocean-button"
                @click.stop="handlePause(scope.row)"
              >
                暂停
              </el-button>
              <el-button
                v-if="scope.row.status === 'paused'"
                type="success"
                size="small"
                class="ocean-button"
                @click.stop="handleStart(scope.row)"
              >
                继续执行
              </el-button>
              <el-button
                v-if="['running', 'paused'].includes(scope.row.status)"
                type="info"
                size="small"
                class="ocean-button"
                @click.stop="handleComplete(scope.row)"
              >
                完成
              </el-button>
              <el-button
                v-if="['pending', 'running', 'paused'].includes(scope.row.status)"
                type="danger"
                size="small"
                class="ocean-button"
                @click.stop="handleAbort(scope.row)"
              >
                中止
              </el-button>
              <el-button
                type="primary"
                size="small"
                class="ocean-button"
                @click.stop="handleView(scope.row)"
              >
                查看
              </el-button>
              <el-button
                v-if="scope.row.status === 'pending'"
                type="danger"
                size="small"
                class="ocean-button"
                @click.stop="handleDelete(scope.row)"
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
          v-model:current-page="pagination.currentPage"
          v-model:page-size="pagination.pageSize"
          :page-sizes="[10, 20, 50, 100]"
          layout="total, sizes, prev, pager, next, jumper"
          :total="pagination.total"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        />
      </div>
    </div>

    <!-- 从测试计划创建测试执行对话框 -->
    <el-dialog
      v-model="createDialog.visible"
      title="从测试计划创建测试执行"
      width="600px"
      class="ocean-dialog"
    >
      <el-form :model="createDialog.form" label-width="120px">
        <el-form-item label="测试计划" required>
          <el-select
            v-model="createDialog.form.planId"
            placeholder="请选择测试计划"
            style="width: 100%"
            filterable
          >
            <el-option
              v-for="item in planOptions"
              :key="item.id"
              :label="item.name"
              :value="item.id"
            ></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="备注">
          <el-input
            v-model="createDialog.form.remarks"
            type="textarea"
            placeholder="请输入备注信息"
            rows="3"
          ></el-input>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="createDialog.visible = false">取消</el-button>
          <el-button type="primary" class="ocean-button" @click="confirmCreateFromPlan" :loading="createDialog.loading">
            确认创建
          </el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { 
  getExecutionList, 
  createExecutionFromPlan, 
  startExecution, 
  pauseExecution, 
  completeExecution, 
  abortExecution, 
  deleteExecution 
} from '@/api/execution'
import { getTestPlans } from '@/api/testplan'

const router = useRouter()
const loading = ref(false)
const executionList = ref([])
const planOptions = ref([])

// 搜索表单
const searchForm = reactive({
  planName: '',
  status: ''
})

// 分页
const pagination = reactive({
  currentPage: 1,
  pageSize: 10,
  total: 0
})

// 创建测试执行对话框
const createDialog = reactive({
  visible: false,
  loading: false,
  form: {
    planId: null,
    remarks: ''
  }
})

// 获取测试执行列表
const fetchExecutionList = async () => {
  loading.value = true
  try {
    const params = {
      page: pagination.currentPage,
      page_size: pagination.pageSize,
      plan_name: searchForm.planName || undefined,
      status: searchForm.status || undefined
    }
    
    console.log('获取测试执行列表，参数:', params)
    console.log('当前分页信息:', {
      currentPage: pagination.currentPage,
      pageSize: pagination.pageSize,
      total: pagination.total
    })
    
    const response = await getExecutionList(params)
    console.log('测试执行列表原始响应:', response)
    
    // 根据实际后端返回的数据结构进行处理
    if (response.results) {
      // 如果后端返回的是 { results: [...], count: ... } 格式
      console.log('检测到 results 格式响应')
      executionList.value = response.results
      pagination.total = response.count || 0
      console.log('解析后的测试执行列表数量:', executionList.value.length)
      console.log('总数:', pagination.total)
    } else if (response.data && response.data.items) {
      // 如果后端返回的是 { data: { items: [...], total: ... } } 格式
      console.log('检测到 data.items 格式响应')
      executionList.value = response.data.items
      pagination.total = response.data.total || 0
      console.log('解析后的测试执行列表数量:', executionList.value.length)
      console.log('总数:', pagination.total)
    } else if (Array.isArray(response)) {
      // 如果后端直接返回数组
      console.log('检测到数组格式响应')
      executionList.value = response
      pagination.total = response.length
      console.log('解析后的测试执行列表数量:', executionList.value.length)
      console.log('总数:', pagination.total)
    } else if (response.data && Array.isArray(response.data)) {
      // 如果后端返回的是 { data: [...] } 格式
      console.log('检测到 data 数组格式响应')
      executionList.value = response.data
      pagination.total = response.data.length
      console.log('解析后的测试执行列表数量:', executionList.value.length)
      console.log('总数:', pagination.total)
    } else {
      // 其他情况，记录错误并设置为空数组
      console.error('未知的响应格式:', response)
      executionList.value = []
      pagination.total = 0
      console.log('无法解析响应，设置为空列表')
    }
    
    console.log('处理后的测试执行列表:', executionList.value)
    
    if (executionList.value.length === 0) {
      console.log('测试执行列表为空')
      if (pagination.currentPage > 1 && pagination.total > 0) {
        console.log('当前页没有数据但总数不为0，尝试返回第一页')
        pagination.currentPage = 1
        fetchExecutionList()
      }
    }
  } catch (error) {
    console.error('获取测试执行列表失败:', error)
    executionList.value = []
    pagination.total = 0
    ElMessage.error('获取测试执行列表失败')
  } finally {
    loading.value = false
  }
}

// 获取测试计划列表
const fetchTestPlanList = async () => {
  try {
    // 修改状态过滤参数格式
    console.log('获取测试计划列表，开始请求...')
    
    // 不使用状态过滤，获取所有测试计划
    console.log('请求所有测试计划')
    const response = await getTestPlans()
    console.log('测试计划列表原始响应:', response)
    
    // 根据实际后端返回的数据结构进行处理
    let plans = []
    
    if (response.results) {
      // 如果后端返回的是 { results: [...], count: ... } 格式
      console.log('检测到 results 格式响应')
      plans = response.results
    } else if (response.data && response.data.items) {
      // 如果后端返回的是 { data: { items: [...], total: ... } } 格式
      console.log('检测到 data.items 格式响应')
      plans = response.data.items
    } else if (Array.isArray(response)) {
      // 如果后端直接返回数组
      console.log('检测到数组格式响应')
      plans = response
    } else if (response.data && Array.isArray(response.data)) {
      // 如果后端返回的是 { data: [...] } 格式
      console.log('检测到 data 数组格式响应')
      plans = response.data
    } else {
      // 其他情况，记录错误并设置为空数组
      console.error('未知的响应格式:', response)
      plans = []
    }
    
    console.log('解析后的测试计划数据:', plans)
    
    // 在前端过滤就绪或进行中的测试计划
    const filteredPlans = plans.filter(plan => ['ready', 'in_progress'].includes(plan.status))
    console.log('过滤后的测试计划数据:', filteredPlans)
    
    // 如果没有符合条件的测试计划，显示所有测试计划
    if (filteredPlans.length === 0) {
      console.log('没有就绪或进行中的测试计划，显示所有测试计划')
      planOptions.value = plans.map(plan => ({
        id: plan.id,
        name: `${plan.name} (${plan.status_display || plan.status})`,
      }))
    } else {
      planOptions.value = filteredPlans.map(plan => ({
        id: plan.id,
        name: plan.name
      }))
    }
    
    console.log('最终的测试计划选项:', planOptions.value)
    
    if (planOptions.value.length === 0) {
      ElMessage.warning('没有可用的测试计划，请先创建测试计划')
    }
  } catch (error) {
    console.error('获取测试计划列表失败:', error)
    planOptions.value = []
    ElMessage.error('获取测试计划列表失败')
  }
}

// 搜索
const handleSearch = () => {
  pagination.currentPage = 1
  fetchExecutionList()
}

// 重置搜索
const resetSearch = () => {
  searchForm.planName = ''
  searchForm.status = ''
  pagination.currentPage = 1
  fetchExecutionList()
}

// 分页大小变化
const handleSizeChange = (size) => {
  pagination.pageSize = size
  fetchExecutionList()
}

// 当前页变化
const handleCurrentChange = (page) => {
  pagination.currentPage = page
  fetchExecutionList()
}

// 获取状态类型
const getStatusType = (status) => {
  const statusMap = {
    pending: 'info',
    running: 'primary',
    paused: 'warning',
    completed: 'success',
    aborted: 'danger'
  }
  return statusMap[status] || 'info'
}

// 格式化日期时间
const formatDateTime = (dateString) => {
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

// 行点击
const handleRowClick = (row) => {
  handleView(row)
}

// 查看测试执行
const handleView = (row) => {
  router.push({
    name: 'ExecutionDetail',
    params: { id: row.id }
  })
}

// 从测试计划创建测试执行
const handleCreateFromPlan = async () => {
  createDialog.form.planId = null
  createDialog.form.remarks = ''
  createDialog.visible = true
  
  // 获取测试计划列表
  if (planOptions.value.length === 0) {
    await fetchTestPlanList()
  }
}

// 确认创建测试执行
const confirmCreateFromPlan = async () => {
  if (!createDialog.form.planId) {
    ElMessage.warning('请选择测试计划')
    return
  }
  
  createDialog.loading = true
  try {
    console.log('创建测试执行，测试计划ID:', createDialog.form.planId)
    console.log('创建测试执行，备注:', createDialog.form.remarks)
    
    const response = await createExecutionFromPlan(createDialog.form.planId, {
      remarks: createDialog.form.remarks
    })
    
    console.log('创建测试执行响应:', response)
    console.log('创建测试执行成功，新执行ID:', response.id)
    ElMessage.success('创建测试执行成功')
    createDialog.visible = false
    
    // 重置分页到第一页，确保能看到新创建的测试执行
    pagination.currentPage = 1
    
    // 延长延迟时间，确保后端数据已更新
    console.log('等待后端数据更新...')
    setTimeout(() => {
      console.log('开始刷新测试执行列表...')
      // 清空搜索条件，确保能看到所有测试执行
      searchForm.planName = ''
      searchForm.status = ''
      fetchExecutionList()
      console.log('测试执行列表刷新完成')
    }, 1500) // 延长到1.5秒
  } catch (error) {
    console.error('创建测试执行失败:', error)
    if (error.response) {
      console.error('错误响应:', error.response.data)
      if (error.response.data && error.response.data.message) {
        ElMessage.error(`创建失败: ${error.response.data.message}`)
      } else {
        ElMessage.error('创建测试执行失败')
      }
    } else {
      ElMessage.error('创建测试执行失败: ' + (error.message || '未知错误'))
    }
  } finally {
    createDialog.loading = false
  }
}

// 开始执行
const handleStart = async (row) => {
  try {
    await startExecution(row.id)
    ElMessage.success('操作成功')
    fetchExecutionList()
  } catch (error) {
    console.error('操作失败:', error)
    ElMessage.error('操作失败')
  }
}

// 暂停执行
const handlePause = async (row) => {
  try {
    await pauseExecution(row.id)
    ElMessage.success('操作成功')
    fetchExecutionList()
  } catch (error) {
    console.error('操作失败:', error)
    ElMessage.error('操作失败')
  }
}

// 完成执行
const handleComplete = async (row) => {
  try {
    await completeExecution(row.id)
    ElMessage.success('操作成功')
    fetchExecutionList()
  } catch (error) {
    console.error('操作失败:', error)
    ElMessage.error('操作失败')
  }
}

// 中止执行
const handleAbort = async (row) => {
  try {
    await ElMessageBox.confirm('确定要中止该测试执行吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    
    await abortExecution(row.id)
    ElMessage.success('操作成功')
    fetchExecutionList()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('操作失败:', error)
      ElMessage.error('操作失败')
    }
  }
}

// 删除测试执行
const handleDelete = async (row) => {
  try {
    await ElMessageBox.confirm('确定要删除该测试执行吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    
    await deleteExecution(row.id)
    ElMessage.success('删除成功')
    fetchExecutionList()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('删除失败:', error)
      ElMessage.error('删除失败')
    }
  }
}

onMounted(() => {
  console.log('测试执行列表组件挂载')
  // 清空搜索条件，确保能看到所有测试执行
  searchForm.planName = ''
  searchForm.status = ''
  // 重置分页到第一页
  pagination.currentPage = 1
  // 获取测试执行列表
  fetchExecutionList()
})
</script>

<style scoped>
.execution-list-container {
  /* 移除原有的padding，使用fullscreen-container的padding */
}

.execution-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.page-title {
  position: relative;
  display: inline-block;
  
  &::after {
    content: '';
    position: absolute;
    bottom: -8px;
    left: 0;
    width: 50px;
    height: 3px;
    background: linear-gradient(to right, #3498db, #2980b9);
  }
}

.search-container {
  margin-bottom: 20px;
  padding: 15px;
  background-color: #ffffff;
  border-radius: 6px;
  border: 1px solid #ecf0f1;
}

.execution-row {
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
</style> 