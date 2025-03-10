<template>
  <div class="execution-detail-container" v-loading="loading">
    <div class="execution-header">
      <div class="header-left">
        <h2>测试执行详情</h2>
        <el-tag :type="getStatusType(executionInfo.status)" class="status-tag">
          {{ executionInfo.status_display }}
        </el-tag>
      </div>
      <div class="header-actions">
        <el-button @click="goBack">返回列表</el-button>
        <el-button
          v-if="executionInfo.status === 'pending'"
          type="success"
          @click="handleStart"
        >
          开始执行
        </el-button>
        <el-button
          v-if="executionInfo.status === 'running'"
          type="warning"
          @click="handlePause"
        >
          暂停
        </el-button>
        <el-button
          v-if="executionInfo.status === 'paused'"
          type="success"
          @click="handleStart"
        >
          继续执行
        </el-button>
        <el-button
          v-if="['running', 'paused'].includes(executionInfo.status)"
          type="info"
          @click="handleComplete"
        >
          完成
        </el-button>
        <el-button
          v-if="['pending', 'running', 'paused'].includes(executionInfo.status)"
          type="danger"
          @click="handleAbort"
        >
          中止
        </el-button>
      </div>
    </div>

    <!-- 测试执行基本信息 -->
    <el-card class="info-card">
      <template #header>
        <div class="card-header">
          <span>基本信息</span>
        </div>
      </template>
      <div class="info-content">
        <div class="info-item">
          <span class="label">测试计划:</span>
          <span class="value">{{ executionInfo.plan_name || (executionInfo.plan_detail && executionInfo.plan_detail.name) || '-' }}</span>
        </div>
        <div class="info-item">
          <span class="label">执行者:</span>
          <span class="value">{{ executionInfo.executor_name || '-' }}</span>
        </div>
        <div class="info-item">
          <span class="label">开始时间:</span>
          <span class="value">{{ executionInfo.start_time ? formatDateTime(executionInfo.start_time) : '-' }}</span>
        </div>
        <div class="info-item">
          <span class="label">结束时间:</span>
          <span class="value">{{ executionInfo.end_time ? formatDateTime(executionInfo.end_time) : '-' }}</span>
        </div>
        <div class="info-item">
          <span class="label">创建时间:</span>
          <span class="value">{{ executionInfo.created_at ? formatDateTime(executionInfo.created_at) : '-' }}</span>
        </div>
        <div class="info-item">
          <span class="label">更新时间:</span>
          <span class="value">{{ executionInfo.updated_at ? formatDateTime(executionInfo.updated_at) : '-' }}</span>
        </div>
      </div>
    </el-card>

    <!-- 测试结果统计 -->
    <el-card class="stats-card">
      <template #header>
        <div class="card-header">
          <span>测试结果统计</span>
        </div>
      </template>
      <div class="stats-content">
        <div class="stat-item">
          <div class="stat-value">{{ resultStats.total }}</div>
          <div class="stat-label">总用例数</div>
        </div>
        <div class="stat-item">
          <div class="stat-value passed">{{ resultStats.passed }}</div>
          <div class="stat-label">通过</div>
        </div>
        <div class="stat-item">
          <div class="stat-value failed">{{ resultStats.failed }}</div>
          <div class="stat-label">失败</div>
        </div>
        <div class="stat-item">
          <div class="stat-value blocked">{{ resultStats.blocked }}</div>
          <div class="stat-label">阻塞</div>
        </div>
        <div class="stat-item">
          <div class="stat-value skipped">{{ resultStats.skipped }}</div>
          <div class="stat-label">跳过</div>
        </div>
        <div class="stat-item">
          <div class="stat-value pending">{{ resultStats.pending }}</div>
          <div class="stat-label">待执行</div>
        </div>
      </div>
    </el-card>

    <!-- 测试结果列表 -->
    <el-card class="results-card">
      <template #header>
        <div class="card-header">
          <span>测试结果列表</span>
          <div class="header-actions">
            <el-button
              v-if="['running', 'paused'].includes(executionInfo.status)"
              type="primary"
              size="small"
              @click="handleBatchUpdate"
            >
              批量更新
            </el-button>
          </div>
        </div>
      </template>
      
      <!-- 筛选区域 -->
      <div class="filter-container">
        <el-form :inline="true" :model="filterForm" class="filter-form">
          <el-form-item label="用例名称">
            <el-input v-model="filterForm.caseName" placeholder="用例名称" clearable></el-input>
          </el-form-item>
          <el-form-item label="状态">
            <el-select v-model="filterForm.status" placeholder="结果状态" clearable style="width: 150px;">
              <el-option label="待执行" value="pending"></el-option>
              <el-option label="通过" value="passed"></el-option>
              <el-option label="失败" value="failed"></el-option>
              <el-option label="阻塞" value="blocked"></el-option>
              <el-option label="跳过" value="skipped"></el-option>
            </el-select>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="handleFilter">筛选</el-button>
            <el-button @click="resetFilter">重置</el-button>
          </el-form-item>
        </el-form>
      </div>
      
      <!-- 结果表格 -->
      <el-table
        v-loading="resultsLoading"
        :data="resultList"
        border
        style="width: 100%"
      >
        <el-table-column type="selection" width="55"></el-table-column>
        <el-table-column prop="case.id" label="用例ID" width="80"></el-table-column>
        <el-table-column prop="case.name" label="用例名称" min-width="180"></el-table-column>
        <el-table-column prop="status_display" label="状态" width="100">
          <template #default="scope">
            <el-tag :type="getResultStatusType(scope.row.status)">{{ scope.row.status_display }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="actual_result" label="实际结果" min-width="200">
          <template #default="scope">
            {{ scope.row.actual_result || '-' }}
          </template>
        </el-table-column>
        <el-table-column prop="remarks" label="备注" min-width="150">
          <template #default="scope">
            {{ scope.row.remarks || '-' }}
          </template>
        </el-table-column>
        <el-table-column prop="execution_time" label="执行时间" width="180">
          <template #default="scope">
            {{ scope.row.execution_time ? formatDateTime(scope.row.execution_time) : '-' }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="200" fixed="right">
          <template #default="scope">
            <div class="operation-buttons">
              <el-button
                v-if="['running', 'paused'].includes(executionInfo.status)"
                type="primary"
                size="small"
                @click="handleUpdateResult(scope.row)"
              >
                更新结果
              </el-button>
              <el-button
                type="info"
                size="small"
                @click="handleViewCase(scope.row.case.id)"
              >
                查看用例
              </el-button>
            </div>
          </template>
        </el-table-column>
      </el-table>
      
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
        ></el-pagination>
      </div>
    </el-card>

    <!-- 更新测试结果对话框 -->
    <el-dialog
      v-model="updateDialog.visible"
      title="更新测试结果"
      width="600px"
    >
      <el-form :model="updateDialog.form" label-width="100px">
        <el-form-item label="测试用例">
          <div>{{ updateDialog.form.caseName }}</div>
        </el-form-item>
        <el-form-item label="结果状态" required>
          <el-select v-model="updateDialog.form.status" placeholder="请选择结果状态" style="width: 100%">
            <el-option label="通过" value="passed"></el-option>
            <el-option label="失败" value="failed"></el-option>
            <el-option label="阻塞" value="blocked"></el-option>
            <el-option label="跳过" value="skipped"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="实际结果">
          <el-input
            v-model="updateDialog.form.actualResult"
            type="textarea"
            placeholder="请输入实际结果"
            rows="3"
          ></el-input>
        </el-form-item>
        <el-form-item label="备注">
          <el-input
            v-model="updateDialog.form.remarks"
            type="textarea"
            placeholder="请输入备注信息"
            rows="2"
          ></el-input>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="updateDialog.visible = false">取消</el-button>
          <el-button type="primary" @click="confirmUpdateResult" :loading="updateDialog.loading">
            确认更新
          </el-button>
        </span>
      </template>
    </el-dialog>

    <!-- 批量更新测试结果对话框 -->
    <el-dialog
      v-model="batchDialog.visible"
      title="批量更新测试结果"
      width="600px"
    >
      <el-form :model="batchDialog.form" label-width="100px">
        <el-form-item label="结果状态" required>
          <el-select v-model="batchDialog.form.status" placeholder="请选择结果状态" style="width: 100%">
            <el-option label="通过" value="passed"></el-option>
            <el-option label="失败" value="failed"></el-option>
            <el-option label="阻塞" value="blocked"></el-option>
            <el-option label="跳过" value="skipped"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="备注">
          <el-input
            v-model="batchDialog.form.remarks"
            type="textarea"
            placeholder="请输入备注信息"
            rows="3"
          ></el-input>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="batchDialog.visible = false">取消</el-button>
          <el-button type="primary" @click="confirmBatchUpdate" :loading="batchDialog.loading">
            确认更新
          </el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { 
  getExecutionDetail, 
  getExecutionResults, 
  updateResult, 
  batchUpdateResults,
  startExecution, 
  pauseExecution, 
  completeExecution, 
  abortExecution 
} from '@/api/execution'

const route = useRoute()
const router = useRouter()
const executionId = computed(() => route.params.id)
const loading = ref(false)
const resultsLoading = ref(false)
const executionInfo = ref({})
const resultList = ref([])
const selectedResults = ref([])

// 筛选表单
const filterForm = reactive({
  caseName: '',
  status: ''
})

// 分页
const pagination = reactive({
  currentPage: 1,
  pageSize: 10,
  total: 0
})

// 更新测试结果对话框
const updateDialog = reactive({
  visible: false,
  loading: false,
  form: {
    id: null,
    caseName: '',
    status: '',
    actualResult: '',
    remarks: ''
  }
})

// 批量更新测试结果对话框
const batchDialog = reactive({
  visible: false,
  loading: false,
  form: {
    status: '',
    remarks: ''
  }
})

// 测试结果统计
const resultStats = reactive({
  total: 0,
  passed: 0,
  failed: 0,
  blocked: 0,
  skipped: 0,
  pending: 0
})

// 获取测试执行详情
const fetchExecutionDetail = async () => {
  loading.value = true
  try {
    const response = await getExecutionDetail(executionId.value)
    executionInfo.value = response
  } catch (error) {
    console.error('获取测试执行详情失败:', error)
    if (error.response && error.response.status === 404) {
      ElMessage.error('该测试执行不存在或已被删除')
      // 返回列表页
      setTimeout(() => {
        router.push('/executions')
      }, 1500)
    } else {
      ElMessage.error('获取测试执行详情失败: ' + (error.message || '未知错误'))
    }
  } finally {
    loading.value = false
  }
}

// 获取测试结果列表
const fetchResultList = async () => {
  resultsLoading.value = true
  try {
    const params = {
      page: pagination.currentPage,
      page_size: pagination.pageSize,
      case_name: filterForm.caseName || undefined,
      status: filterForm.status || undefined
    }
    
    try {
      const response = await getExecutionResults(executionId.value, params)
      if (response && response.results) {
        resultList.value = response.results
        pagination.total = response.count || response.results.length
        
        // 更新统计数据
        if (response.stats) {
          updateResultStats(response.stats)
        }
      } else {
        resultList.value = []
        pagination.total = 0
        // 重置统计数据
        resetResultStats()
      }
    } catch (error) {
      if (error.response && error.response.status === 404) {
        ElMessage.error('该测试执行的结果不存在或已被删除')
        resultList.value = []
        pagination.total = 0
        resetResultStats()
      } else {
        throw error
      }
    }
  } catch (error) {
    console.error('获取测试结果列表失败:', error)
    ElMessage.error('获取测试结果列表失败: ' + (error.message || '未知错误'))
    resultList.value = []
    pagination.total = 0
    resetResultStats()
  } finally {
    resultsLoading.value = false
  }
}

// 重置测试结果统计
const resetResultStats = () => {
  resultStats.total = 0
  resultStats.passed = 0
  resultStats.failed = 0
  resultStats.blocked = 0
  resultStats.skipped = 0
  resultStats.pending = 0
}

// 更新测试结果统计
const updateResultStats = (stats) => {
  if (stats) {
    resultStats.total = stats.total || 0
    resultStats.passed = stats.passed || 0
    resultStats.failed = stats.failed || 0
    resultStats.blocked = stats.blocked || 0
    resultStats.skipped = stats.skipped || 0
    resultStats.pending = stats.pending || 0
  }
}

// 筛选
const handleFilter = () => {
  pagination.currentPage = 1
  fetchResultList()
}

// 重置筛选
const resetFilter = () => {
  filterForm.caseName = ''
  filterForm.status = ''
  pagination.currentPage = 1
  fetchResultList()
}

// 分页大小变化
const handleSizeChange = (size) => {
  pagination.pageSize = size
  fetchResultList()
}

// 当前页变化
const handleCurrentChange = (page) => {
  pagination.currentPage = page
  fetchResultList()
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

// 获取结果状态类型
const getResultStatusType = (status) => {
  const statusMap = {
    pending: 'info',
    passed: 'success',
    failed: 'danger',
    blocked: 'warning',
    skipped: ''
  }
  return statusMap[status] || 'info'
}

// 格式化日期时间
const formatDateTime = (dateTimeStr) => {
  const date = new Date(dateTimeStr)
  return date.toLocaleString()
}

// 返回列表
const goBack = () => {
  router.push('/executions')
}

// 查看测试用例
const handleViewCase = (caseId) => {
  // 导航到测试用例详情页面，并传递来源和执行ID参数
  router.push({
    path: `/testcases/${caseId}`,
    query: {
      from: 'execution',
      executionId: executionId.value
    }
  })
}

// 更新测试结果
const handleUpdateResult = (row) => {
  updateDialog.form.id = row.id
  updateDialog.form.caseName = row.case.name
  updateDialog.form.status = row.status === 'pending' ? 'passed' : row.status
  updateDialog.form.actualResult = row.actual_result || ''
  updateDialog.form.remarks = row.remarks || ''
  updateDialog.visible = true
}

// 确认更新测试结果
const confirmUpdateResult = async () => {
  if (!updateDialog.form.status) {
    ElMessage.warning('请选择结果状态')
    return
  }

  updateDialog.loading = true
  try {
    const data = {
      status: updateDialog.form.status,
      actual_result: updateDialog.form.actualResult,
      remarks: updateDialog.form.remarks
    }
    await updateResult(updateDialog.form.id, data)
    ElMessage.success('更新测试结果成功')
    updateDialog.visible = false
    fetchResultList()
    fetchExecutionDetail()
  } catch (error) {
    console.error('更新测试结果失败:', error)
    ElMessage.error('更新测试结果失败')
  } finally {
    updateDialog.loading = false
  }
}

// 批量更新测试结果
const handleBatchUpdate = () => {
  const selection = selectedResults.value
  if (selection.length === 0) {
    ElMessage.warning('请选择要更新的测试结果')
    return
  }

  batchDialog.form.status = ''
  batchDialog.form.remarks = ''
  batchDialog.visible = true
}

// 确认批量更新测试结果
const confirmBatchUpdate = async () => {
  if (!batchDialog.form.status) {
    ElMessage.warning('请选择结果状态')
    return
  }

  batchDialog.loading = true
  try {
    const results = selectedResults.value.map(item => ({
      id: item.id,
      status: batchDialog.form.status,
      remarks: batchDialog.form.remarks
    }))
    
    await batchUpdateResults(results)
    ElMessage.success('批量更新测试结果成功')
    batchDialog.visible = false
    fetchResultList()
    fetchExecutionDetail()
  } catch (error) {
    console.error('批量更新测试结果失败:', error)
    ElMessage.error('批量更新测试结果失败')
  } finally {
    batchDialog.loading = false
  }
}

// 开始执行
const handleStart = async () => {
  try {
    await startExecution(executionId.value)
    ElMessage.success('操作成功')
    fetchExecutionDetail()
  } catch (error) {
    console.error('操作失败:', error)
    ElMessage.error('操作失败')
  }
}

// 暂停执行
const handlePause = async () => {
  try {
    await pauseExecution(executionId.value)
    ElMessage.success('操作成功')
    fetchExecutionDetail()
  } catch (error) {
    console.error('操作失败:', error)
    ElMessage.error('操作失败')
  }
}

// 完成执行
const handleComplete = async () => {
  try {
    await completeExecution(executionId.value)
    ElMessage.success('操作成功')
    fetchExecutionDetail()
  } catch (error) {
    console.error('操作失败:', error)
    ElMessage.error('操作失败')
  }
}

// 中止执行
const handleAbort = async () => {
  try {
    await ElMessageBox.confirm('确定要中止此测试执行吗?', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    await abortExecution(executionId.value)
    ElMessage.success('操作成功')
    fetchExecutionDetail()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('操作失败:', error)
      ElMessage.error('操作失败')
    }
  }
}

// 表格选择变化
const handleSelectionChange = (selection) => {
  selectedResults.value = selection
}

onMounted(() => {
  fetchExecutionDetail()
  fetchResultList()
})
</script>

<style scoped>
.execution-detail-container {
  padding: 20px;
  height: calc(100vh - 80px);
  overflow-y: auto;
  position: relative;
}

.execution-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.header-left {
  display: flex;
  align-items: center;
}

.status-tag {
  margin-left: 10px;
}

.info-card,
.stats-card,
.results-card {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.info-content {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 15px;
}

.info-item {
  display: flex;
  flex-direction: column;
}

.label {
  font-weight: bold;
  color: #606266;
  margin-bottom: 5px;
}

.stats-content {
  display: flex;
  justify-content: space-around;
  flex-wrap: wrap;
}

.stat-item {
  text-align: center;
  padding: 15px;
  min-width: 100px;
}

.stat-value {
  font-size: 24px;
  font-weight: bold;
  margin-bottom: 5px;
}

.stat-label {
  color: #606266;
}

.passed {
  color: #67c23a;
}

.failed {
  color: #f56c6c;
}

.blocked {
  color: #e6a23c;
}

.skipped {
  color: #909399;
}

.pending {
  color: #409eff;
}

.filter-container {
  margin-bottom: 20px;
  padding: 15px;
  background-color: #f5f7fa;
  border-radius: 4px;
}

.pagination-container {
  margin-top: 20px;
  margin-bottom: 20px;
  display: flex;
  justify-content: flex-end;
}

.operation-buttons {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.operation-buttons .el-button {
  margin-left: 0;
  margin-right: 0;
}
</style> 