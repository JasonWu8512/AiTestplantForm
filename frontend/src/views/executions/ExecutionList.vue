<template>
  <div class="execution-list-container fullscreen-container">
    <div class="execution-header">
      <div class="title-section">
        <h2 class="page-title">测试执行管理</h2>
        <p class="page-description">管理和查看测试执行记录，跟踪测试计划的执行状态和结果</p>
      </div>
      <div class="execution-actions">
        <el-button type="primary" class="ocean-button" @click="handleCreateFromPlan">从测试计划创建</el-button>
        <!-- 暂时注释掉不需要的功能按钮
        <el-button type="danger" class="ocean-button" @click="handleClearAllExecutions">清空执行列表</el-button>
        <el-button type="warning" class="ocean-button" @click="handleRemoveEmptyRecords">删除空白记录</el-button>
        <el-button type="info" class="ocean-button" @click="handleCheckDatabaseRecords">检查数据库记录</el-button>
        -->
      </div>
    </div>

    <!-- 搜索区域 -->
    <div class="search-container">
      <el-form :inline="true" :model="searchForm" class="search-form">
        <el-form-item label="测试计划">
          <el-input v-model="searchForm.planName" placeholder="测试计划名称" clearable></el-input>
        </el-form-item>
        <el-form-item label="状态">
          <el-select v-model="searchForm.status" placeholder="执行状态" clearable style="width: 150px;">
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
          :data="displayedExecutions"
          border
          style="width: 100%"
          height="100%"
          @row-click="handleRowClick"
          row-class-name="execution-row"
        >
          <el-table-column prop="id" label="ID" width="80"></el-table-column>
          <el-table-column prop="plan_detail.name" label="测试计划" min-width="180">
            <template #default="scope">
              {{ scope.row.plan_detail && scope.row.plan_detail.name ? scope.row.plan_detail.name : (scope.row.plan_name || '-') }}
            </template>
          </el-table-column>
          <el-table-column prop="plan_detail.project_name" label="项目名称" min-width="180">
            <template #default="scope">
              {{ scope.row.plan_detail && scope.row.plan_detail.project_name ? scope.row.plan_detail.project_name : '-' }}
            </template>
          </el-table-column>
          <el-table-column prop="executor.username" label="执行者" width="120">
            <template #default="scope">
              {{ scope.row.executor_name || (scope.row.executor && scope.row.executor.username ? scope.row.executor.username : '-') }}
            </template>
          </el-table-column>
          <el-table-column prop="status_display" label="状态" width="120">
            <template #default="scope">
              <el-tag :type="getStatusType(scope.row.status)">
                <span class="status-icon">
                  <i :class="getStatusIcon(scope.row.status)"></i>
                </span>
                {{ scope.row.status_display }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="start_time" label="开始时间" width="180">
            <template #default="scope">
              {{ scope.row.start_time ? formatDateTime(scope.row.start_time) : 
                 (scope.row.plan_detail && scope.row.plan_detail.start_time ? formatDateTime(scope.row.plan_detail.start_time) : '-') }}
            </template>
          </el-table-column>
          <el-table-column prop="end_time" label="结束时间" width="180">
            <template #default="scope">
              {{ scope.row.end_time ? formatDateTime(scope.row.end_time) : 
                 (scope.row.plan_detail && scope.row.plan_detail.end_time ? formatDateTime(scope.row.plan_detail.end_time) : '-') }}
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
import { ref, reactive, onMounted, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { 
  getExecutionList, 
  createExecutionFromPlan, 
  startExecution, 
  pauseExecution, 
  completeExecution, 
  abortExecution, 
  deleteExecution,
  getExecutionDetail
} from '@/api/execution'
import { getTestPlans, getTestPlanById } from '@/api/testplan'
import feedback from '@/utils/feedback'
import errorMonitor from '@/utils/error-monitor'
import { ElMessageBox } from 'element-plus'

const router = useRouter()
const route = useRoute()
const loading = ref(false)
const executionList = ref([])
const displayedExecutions = ref([]) // 当前页显示的测试执行
const allExecutions = ref([]) // 所有测试执行
const planOptions = ref([])

// 统一错误处理函数
const handleApiError = (error, defaultMessage = '操作失败') => {
  // 记录错误
  errorMonitor.logApiError(error, { 
    context: 'ExecutionList', 
    defaultMessage 
  })
  
  // 显示错误消息
  feedback.showApiError(error, defaultMessage)
}

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
    // 构建查询参数
    const params = {
      plan_name: searchForm.planName,
      status: searchForm.status
    }
    
    console.log('发送到后端的参数:', JSON.stringify(params))
    
    const response = await getExecutionList(params)
    
    // 更健壮的数据处理
    if (Array.isArray(response)) {
      allExecutions.value = response
    } else if (response && Array.isArray(response.results)) {
      allExecutions.value = response.results
    } else if (response && response.data && Array.isArray(response.data)) {
      allExecutions.value = response.data
    } else {
      console.warn('未能识别的响应格式或数据为空，将尝试直接使用:', response)
      // 如果无法识别格式，但响应不为空，尝试直接使用
      allExecutions.value = Array.isArray(response) ? response : []
    }
    
    // 应用分页
    applyPagination()
  } catch (error) {
    console.error('获取测试执行列表失败:', error)
    if (error.response) {
      console.error('错误响应数据:', error.response.data)
      console.error('错误状态码:', error.response.status)
    }
    handleApiError(error, '获取测试执行列表失败')
    allExecutions.value = []
  } finally {
    loading.value = false
  }
}

// 应用分页
const applyPagination = () => {
  const start = (pagination.currentPage - 1) * pagination.pageSize
  const end = start + pagination.pageSize
  displayedExecutions.value = allExecutions.value.slice(start, end)
  
  console.log(`应用分页: 第${pagination.currentPage}页，每页${pagination.pageSize}条，共${pagination.total}条`)
  console.log('当前页数据:', displayedExecutions.value)
}

// 获取测试计划列表
const fetchTestPlanList = async () => {
  // 显示加载状态
  const loadingInstance = feedback.showLoading('正在获取测试计划列表...')
  
  try {
    const response = await getTestPlans()
    console.log('测试计划列表原始响应:', response)
    
    let plans = []
    
    // 处理不同格式的响应
    if (Array.isArray(response)) {
      // 如果后端直接返回数组
      console.log('检测到数组格式响应')
      plans = response
    } else if (response && response.results && Array.isArray(response.results)) {
      // 如果后端返回的是 { results: [...] } 格式（DRF分页）
      console.log('检测到 results 数组格式响应（DRF分页）')
      plans = response.results
    } else if (response && response.data && Array.isArray(response.data)) {
      // 如果后端返回的是 { data: [...] } 格式
      console.log('检测到 data 数组格式响应')
      plans = response.data
    } else if (response && response.data && response.data.items && Array.isArray(response.data.items)) {
      // 如果后端返回的是 { data: { items: [...] } } 格式
      console.log('检测到 data.items 数组格式响应')
      plans = response.data.items
    } else if (response && typeof response === 'object') {
      // 尝试从对象中提取数据
      console.log('尝试从对象中提取数据')
      const possibleArrays = Object.values(response).filter(val => Array.isArray(val))
      if (possibleArrays.length > 0) {
        // 使用找到的第一个数组
        plans = possibleArrays[0]
        console.log('从对象中提取到数组数据:', plans)
      } else {
        console.error('未能从对象中提取到数组数据:', response)
        plans = []
      }
    } else {
      // 其他情况，记录错误并设置为空数组
      console.error('未知的响应格式:', response)
      plans = []
    }
    
    console.log('解析后的测试计划数据:', plans)
    
    // 在前端过滤就绪或进行中的测试计划
    // 放宽过滤条件，允许草稿状态的测试计划也显示
    const filteredPlans = plans.filter(plan => ['draft', 'ready', 'in_progress'].includes(plan.status))
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
      feedback.showWarning('没有可用的测试计划，请先创建测试计划')
    }
  } catch (error) {
    console.error('获取测试计划列表失败:', error)
    if (error.response) {
      console.error('错误响应数据:', error.response.data)
      console.error('错误状态码:', error.response.status)
    }
    handleApiError(error, '获取测试计划列表失败')
    planOptions.value = []
  } finally {
    // 隐藏加载状态
    feedback.hideLoading()
  }
}

// 搜索
const handleSearch = () => {
  console.log('执行搜索操作，搜索条件:', {
    planName: searchForm.planName,
    status: searchForm.status
  })
  
  // 构建查询参数
  const params = {
    plan_name: searchForm.planName,
    status: searchForm.status
  }
  
  console.log('发送到后端的搜索参数:', JSON.stringify(params))
  
  // 重置分页到第一页
  pagination.currentPage = 1
  
  // 获取测试执行列表
  fetchExecutionList()
}

// 重置搜索
const resetSearch = () => {
  console.log('重置搜索条件')
  searchForm.planName = ''
  searchForm.status = ''
  
  // 构建查询参数
  const params = {
    plan_name: searchForm.planName,
    status: searchForm.status
  }
  
  console.log('重置后发送到后端的参数:', JSON.stringify(params))
  
  // 重置分页到第一页
  pagination.currentPage = 1
  
  // 获取测试执行列表
  fetchExecutionList()
}

// 分页大小变化
const handleSizeChange = (size) => {
  pagination.pageSize = size
  applyPagination()
}

// 当前页变化
const handleCurrentChange = (page) => {
  pagination.currentPage = page
  applyPagination()
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

// 获取状态图标
const getStatusIcon = (status) => {
  const iconMap = {
    pending: 'el-icon-loading',
    running: 'el-icon-loading',
    paused: 'el-icon-pause',
    completed: 'el-icon-check',
    aborted: 'el-icon-close'
  }
  return iconMap[status] || 'el-icon-info'
}

// 格式化日期时间
const formatDateTime = (dateString) => {
  if (!dateString) return ''
  try {
    const date = new Date(dateString)
    if (isNaN(date.getTime())) {
      return '无效日期'
    }
    return date.toLocaleString('zh-CN', {
      year: 'numeric',
      month: '2-digit',
      day: '2-digit',
      hour: '2-digit',
      minute: '2-digit',
      second: '2-digit'
    })
  } catch (error) {
    errorMonitor.logError(error, errorMonitor.ErrorTypes.CUSTOM_ERROR, errorMonitor.ErrorLevels.WARNING, {
      context: 'ExecutionList.formatDateTime',
      dateString
    })
    return '日期格式错误'
  }
}

// 行点击
const handleRowClick = (row) => {
  handleView(row)
}

// 查看测试执行
const handleView = (row) => {
  // 显示加载状态
  const loadingInstance = feedback.showLoading('正在加载测试执行详情...')
  
  // 先检查执行是否存在
  try {
    // 使用路由导航前先检查执行是否存在
    getExecutionDetail(row.id)
      .then(() => {
        router.push({
          name: 'ExecutionDetail',
          params: { id: row.id }
        })
      })
      .catch(error => {
        console.error('获取执行详情失败:', error)
        feedback.showError('该测试执行不存在或已被删除')
        // 刷新列表以移除不存在的执行
        fetchExecutionList()
      })
      .finally(() => {
        // 隐藏加载状态
        feedback.hideLoading()
      })
  } catch (error) {
    handleApiError(error, '获取执行详情失败')
    feedback.hideLoading()
  }
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
    feedback.showWarning('请选择测试计划')
    return
  }
  
  createDialog.loading = true
  // 显示加载状态
  const loadingInstance = feedback.showLoading('正在创建测试执行...')
  
  try {
    console.log('创建测试执行，测试计划ID:', createDialog.form.planId)
    
    // 检查测试计划是否存在测试用例
    try {
      const planDetail = await getTestPlanById(createDialog.form.planId)
      console.log('测试计划详情:', planDetail)
      
      if (planDetail && planDetail.test_cases_count === 0) {
        feedback.showWarning('所选测试计划没有关联任何测试用例，请先添加测试用例')
        createDialog.loading = false
        feedback.hideLoading()
        return
      }
    } catch (error) {
      console.error('获取测试计划详情失败:', error)
      // 继续尝试创建测试执行
    }
    
    const response = await createExecutionFromPlan(createDialog.form.planId, {
      remarks: createDialog.form.remarks
    })
    
    console.log('创建测试执行响应:', response)
    
    // 验证响应数据
    if (!response) {
      console.error('创建测试执行响应为空')
      feedback.showWarning('创建测试执行失败，服务器返回空响应')
      createDialog.visible = false
      createDialog.loading = false
      // 刷新列表
      await fetchExecutionList()
      return
    }
    
    if (!response.id) {
      console.error('创建测试执行响应数据无效:', response)
      feedback.showWarning('创建测试执行成功，但返回的数据格式不正确')
      createDialog.visible = false
      createDialog.loading = false
      // 刷新列表
      await fetchExecutionList()
      return
    }
    
    feedback.showSuccess('创建测试执行成功')
    createDialog.visible = false
    
    // 重置分页到第一页
    pagination.currentPage = 1
    // 清空搜索条件
    searchForm.planName = ''
    searchForm.status = ''
    
    // 直接刷新列表
    await fetchExecutionList()
    
    // 确保新创建的测试执行显示在列表中
    try {
      // 检查allExecutions是否为数组
      if (Array.isArray(allExecutions.value)) {
        // 如果新创建的测试执行不在所有测试执行列表中，添加到列表顶部
        if (!allExecutions.value.some(item => item.id === response.id)) {
          allExecutions.value.unshift(response)
          // 重新应用分页
          applyPagination()
        }
      } else {
        console.warn('allExecutions不是数组，无法添加新创建的测试执行')
        // 如果allExecutions不是数组，直接重新获取列表
        await fetchExecutionList()
      }
    } catch (error) {
      console.error('处理新创建的测试执行时出错:', error)
      // 出错时重新获取列表
      await fetchExecutionList()
    }
  } catch (error) {
    console.error('创建测试执行失败:', error)
    
    // 详细的错误日志
    if (error.response) {
      console.error('错误响应数据:', error.response.data)
      console.error('错误状态码:', error.response.status)
      
      // 针对404错误提供更具体的提示
      if (error.response.status === 404) {
        feedback.showError('创建测试执行失败: 找不到指定的测试计划或API路径不正确')
      } else if (error.response.status === 400) {
        // 尝试从错误响应中提取具体信息
        const errorMessage = error.response.data.message || 
                            (error.response.data.detail ? error.response.data.detail : 
                            '创建测试执行失败，请检查测试计划是否有效')
        feedback.showError(`创建测试执行失败: ${errorMessage}`)
      } else {
        feedback.showError(`创建测试执行失败: ${error.message || '未知错误'}`)
      }
    } else {
      feedback.showError(`创建测试执行失败: ${error.message || '未知错误'}`)
    }
  } finally {
    createDialog.loading = false
    feedback.hideLoading()
  }
}

// 开始执行
const handleStart = async (row) => {
  try {
    // 显示加载状态
    const loadingInstance = feedback.showLoading('正在开始测试执行...')
    
    await startExecution(row.id)
    feedback.showSuccess('开始执行成功')
    await fetchExecutionList()
  } catch (error) {
    handleApiError(error, '开始执行失败')
  } finally {
    // 隐藏加载状态
    feedback.hideLoading()
  }
}

// 暂停执行
const handlePause = async (row) => {
  try {
    // 显示加载状态
    const loadingInstance = feedback.showLoading('正在暂停测试执行...')
    
    await pauseExecution(row.id)
    feedback.showSuccess('暂停执行成功')
    await fetchExecutionList()
  } catch (error) {
    handleApiError(error, '暂停执行失败')
  } finally {
    // 隐藏加载状态
    feedback.hideLoading()
  }
}

// 完成执行
const handleComplete = async (row) => {
  try {
    // 询问是否自动生成报告
    const { action } = await ElMessageBox.confirm(
      '是否在完成测试执行后自动生成测试报告？',
      '完成测试执行',
      {
        confirmButtonText: '是',
        cancelButtonText: '否',
        type: 'info',
        distinguishCancelAndClose: true
      }
    )
    
    // 显示加载状态
    const loadingInstance = feedback.showLoading('正在完成测试执行...')
    
    if (action === 'confirm') {
      // 用户选择自动生成报告
      await completeExecution(row.id, { autoGenerateReport: true })
      feedback.showSuccess('完成执行成功，测试报告生成任务已提交')
    } else {
      // 用户选择不自动生成报告
      await completeExecution(row.id, { autoGenerateReport: false })
      feedback.showSuccess('完成执行成功，未生成测试报告')
    }
    
    await fetchExecutionList()
  } catch (error) {
    if (error !== 'cancel') { // 忽略用户取消的情况
      handleApiError(error, '完成执行失败')
    }
  } finally {
    // 隐藏加载状态
    feedback.hideLoading()
  }
}

// 中止执行
const handleAbort = async (row) => {
  try {
    const result = await feedback.showConfirm(
      '确定要中止该测试执行吗？此操作不可逆。',
      '中止确认',
      {
        confirmButtonText: '确定中止',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    
    // 显示加载状态
    const loadingInstance = feedback.showLoading('正在中止测试执行...')
    
    await abortExecution(row.id)
    feedback.showSuccess('中止执行成功')
    await fetchExecutionList()
  } catch (error) {
    if (error === 'cancel' || error === 'close') {
      console.log('用户取消了中止操作')
    } else {
      handleApiError(error, '中止执行失败')
    }
  } finally {
    // 隐藏加载状态
    feedback.hideLoading()
  }
}

// 删除测试执行
const handleDelete = async (row) => {
  try {
    const result = await feedback.showConfirm(
      '确定要删除该测试执行吗？此操作不可恢复。',
      '删除确认',
      {
        confirmButtonText: '确定删除',
        cancelButtonText: '取消',
        type: 'error'
      }
    )
    
    // 显示加载状态
    const loadingInstance = feedback.showLoading('正在删除测试执行...')
    
    await deleteExecution(row.id)
    feedback.showSuccess('删除测试执行成功')
    await fetchExecutionList()
  } catch (error) {
    if (error === 'cancel' || error === 'close') {
      console.log('用户取消了删除操作')
    } else {
      handleApiError(error, '删除测试执行失败')
    }
  } finally {
    // 隐藏加载状态
    feedback.hideLoading()
  }
}

// 监听路由变化，当进入该页面时刷新数据
watch(
  () => route.path,
  (newPath) => {
    if (newPath === '/executions') {
      console.log('路由变化，进入测试执行列表页面')
      // 清空搜索条件，确保能看到所有测试执行
      searchForm.planName = ''
      searchForm.status = ''
      // 重置分页到第一页
      pagination.currentPage = 1
      // 获取测试执行列表
      fetchExecutionList()
    }
  },
  { immediate: true }
)

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

// 清空测试执行列表
const handleClearAllExecutions = async () => {
  // 暂时注释掉此功能
  console.log('清空执行列表功能已暂时禁用');
  ElMessage.info('清空执行列表功能已暂时禁用');
  /*
  try {
    await ElMessageBox.confirm('确定要清空所有测试执行记录吗？此操作不可恢复！', '警告', {
      confirmButtonText: '确定清空',
      cancelButtonText: '取消',
      type: 'warning',
      distinguishCancelAndClose: true
    })
    
    loading.value = true
    
    try {
      // 获取所有执行记录
      const response = await getExecutionList({})
      console.log('清空列表获取的执行记录:', response)
      
      let executions = []
      
      // 更健壮的数据处理
      if (Array.isArray(response)) {
        executions = response
      } else if (response && Array.isArray(response.results)) {
        executions = response.results
      } else if (response && response.data && Array.isArray(response.data)) {
        executions = response.data
      } else {
        console.warn('未能识别的响应格式或数据为空，将尝试直接使用:', response)
        // 如果无法识别格式，但响应不为空，尝试直接使用
        executions = Array.isArray(response) ? response : []
      }
      
      console.log('处理后的执行记录数组:', executions)
      
      // 确保executions是数组
      if (!Array.isArray(executions)) {
        console.error('执行记录不是数组:', executions)
        executions = []
      }
      
      // 过滤掉无效的记录
      const validExecutions = executions.filter(execution => execution && execution.id)
      console.log('有效的执行记录数量:', validExecutions.length)
      
      if (validExecutions.length === 0) {
        ElMessage.info('没有找到可删除的执行记录')
        return
      }
      
      // 逐个删除执行记录
      const deletePromises = validExecutions.map(execution => {
        console.log('准备删除执行记录:', execution.id)
        return deleteExecution(execution.id).catch(error => {
          console.error(`删除执行记录 ${execution.id} 失败:`, error)
          // 返回失败信息但不中断整个过程
          return { failed: true, id: execution.id, error }
        })
      })
      
      const results = await Promise.all(deletePromises)
      
      // 检查是否有删除失败的记录
      const failedResults = results.filter(result => result && result.failed)
      if (failedResults.length > 0) {
        console.error('部分执行记录删除失败:', failedResults)
        ElMessage.warning(`已删除 ${results.length - failedResults.length} 条记录，${failedResults.length} 条记录删除失败`)
      } else {
        ElMessage.success(`已成功清空 ${results.length} 条测试执行记录`)
      }
    } catch (error) {
      console.error('清空执行记录过程中出错:', error)
      throw error
    } finally {
      // 无论成功失败，都刷新列表
      await fetchExecutionList()
    }
  } catch (error) {
    if (error !== 'cancel' && error !== 'close') {
      console.error('清空测试执行记录失败:', error)
      if (error.message) {
        ElMessage.error(`清空测试执行记录失败: ${error.message}`)
      } else {
        handleApiError(error, '清空测试执行记录失败')
      }
    }
  } finally {
    loading.value = false
  }
  */
}

// 删除空白记录
const handleRemoveEmptyRecords = async () => {
  // 暂时注释掉此功能
  console.log('删除空白记录功能已暂时禁用');
  ElMessage.info('删除空白记录功能已暂时禁用');
  /*
  try {
    await ElMessageBox.confirm('确定要删除所有空白记录吗？此操作不可恢复！', '警告', {
      confirmButtonText: '确定删除',
      cancelButtonText: '取消',
      type: 'warning',
      distinguishCancelAndClose: true
    })
    
    loading.value = true
    
    try {
      // 获取所有执行记录
      const response = await getExecutionList({})
      console.log('获取的执行记录:', response)
      
      let executions = []
      
      // 更健壮的数据处理
      if (Array.isArray(response)) {
        executions = response
      } else if (response && Array.isArray(response.results)) {
        executions = response.results
      } else if (response && response.data && Array.isArray(response.data)) {
        executions = response.data
      } else {
        console.warn('未能识别的响应格式或数据为空，将尝试直接使用:', response)
        // 如果无法识别格式，但响应不为空，尝试直接使用
        executions = Array.isArray(response) ? response : []
      }
      
      console.log('处理后的执行记录数组:', executions)
      
      // 确保executions是数组
      if (!Array.isArray(executions)) {
        console.error('执行记录不是数组:', executions)
        executions = []
      }
      
      // 识别空白记录
      // 空白记录的定义：缺少plan或executor或其他关键信息的记录
      const emptyRecords = executions.filter(execution => {
        if (!execution || !execution.id) return false
        
        // 检查是否为空白记录
        const isEmpty = (
          !execution.plan || 
          !execution.plan.name || 
          !execution.executor || 
          !execution.executor.username ||
          (execution.status === 'pending' && !execution.start_time && !execution.end_time)
        )
        
        return isEmpty
      })
      
      console.log('识别到的空白记录:', emptyRecords)
      
      if (emptyRecords.length === 0) {
        ElMessage.info('没有找到空白记录')
        return
      }
      
      // 逐个删除空白记录
      const deletePromises = emptyRecords.map(execution => {
        console.log('准备删除空白记录:', execution.id)
        return deleteExecution(execution.id).catch(error => {
          console.error(`删除空白记录 ${execution.id} 失败:`, error)
          // 返回失败信息但不中断整个过程
          return { failed: true, id: execution.id, error }
        })
      })
      
      const results = await Promise.all(deletePromises)
      
      // 检查是否有删除失败的记录
      const failedResults = results.filter(result => result && result.failed)
      if (failedResults.length > 0) {
        console.error('部分空白记录删除失败:', failedResults)
        ElMessage.warning(`已删除 ${emptyRecords.length - failedResults.length} 条空白记录，${failedResults.length} 条记录删除失败`)
      } else {
        ElMessage.success(`已成功删除 ${emptyRecords.length} 条空白记录`)
      }
    } catch (error) {
      console.error('删除空白记录过程中出错:', error)
      throw error
    } finally {
      // 无论成功失败，都刷新列表
      await fetchExecutionList()
    }
  } catch (error) {
    if (error !== 'cancel' && error !== 'close') {
      console.error('删除空白记录失败:', error)
      if (error.message) {
        ElMessage.error(`删除空白记录失败: ${error.message}`)
      } else {
        handleApiError(error, '删除空白记录失败')
      }
    }
  } finally {
    loading.value = false
  }
  */
}

// 检查数据库记录
const handleCheckDatabaseRecords = async () => {
  // 暂时注释掉此功能
  console.log('检查数据库记录功能已暂时禁用');
  ElMessage.info('检查数据库记录功能已暂时禁用');
  /*
  try {
    loading.value = true
    ElMessage.info('正在检查数据库记录，请查看控制台输出...')
    
    // 获取所有执行记录
    const response = await getExecutionList({})
    console.log('===== 数据库记录检查开始 =====')
    console.log('获取的执行记录总数:', response ? (Array.isArray(response) ? response.length : 
                                              (response.results && Array.isArray(response.results) ? response.results.length : 
                                               (response.data && Array.isArray(response.data) ? response.data.length : '未知'))) : '未知')
    
    let executions = []
    
    // 更健壮的数据处理
    if (Array.isArray(response)) {
      executions = response
    } else if (response && Array.isArray(response.results)) {
      executions = response.results
    } else if (response && response.data && Array.isArray(response.data)) {
      executions = response.data
    } else {
      console.warn('未能识别的响应格式或数据为空:', response)
      executions = Array.isArray(response) ? response : []
    }
    
    if (!Array.isArray(executions)) {
      console.error('执行记录不是数组:', executions)
      executions = []
    }
    
    // 识别空白记录
    const emptyRecords = executions.filter(execution => {
      if (!execution || !execution.id) return false
      
      // 检查是否为空白记录
      const isEmpty = (
        !execution.plan || 
        !execution.plan.name || 
        !execution.executor || 
        !execution.executor.username ||
        (execution.status === 'pending' && !execution.start_time && !execution.end_time)
      )
      
      return isEmpty
    })
    
    // 输出详细信息
    console.log('===== 记录统计 =====')
    console.log('总记录数:', executions.length)
    console.log('空白记录数:', emptyRecords.length)
    console.log('正常记录数:', executions.length - emptyRecords.length)
    
    // 输出空白记录详情
    if (emptyRecords.length > 0) {
      console.log('===== 空白记录详情 =====')
      emptyRecords.forEach((record, index) => {
        console.log(`空白记录 #${index + 1} (ID: ${record.id}):`)
        console.log('  - 测试计划:', record.plan ? (record.plan.name || '无名称') : '缺失')
        console.log('  - 执行者:', record.executor ? (record.executor.username || '无用户名') : '缺失')
        console.log('  - 状态:', record.status, record.status_display || '')
        console.log('  - 开始时间:', record.start_time || '缺失')
        console.log('  - 结束时间:', record.end_time || '缺失')
        console.log('  - 创建时间:', record.created_at || '缺失')
        console.log('  - 更新时间:', record.updated_at || '缺失')
      })
      
      // 在页面上显示结果
      ElMessage.warning(`发现 ${emptyRecords.length} 条空白记录，详情请查看控制台输出`)
    } else {
      console.log('没有发现空白记录')
      ElMessage.success('没有发现空白记录')
    }
    
    console.log('===== 数据库记录检查结束 =====')
  } catch (error) {
    console.error('检查数据库记录失败:', error)
    ElMessage.error('检查数据库记录失败: ' + (error.message || '未知错误'))
  } finally {
    loading.value = false
  }
  */
}
</script>

<style scoped>
.execution-list-container {
  padding: 20px;
  height: 100%;
  display: flex;
  flex-direction: column;
}

.execution-header {
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
  background: linear-gradient(to right, var(--primary-color), var(--primary-light));
  border-radius: 3px;
}

.page-description {
  color: var(--text-secondary, #606266);
  font-size: 14px;
  margin-top: 8px;
  line-height: 1.5;
}

.execution-actions {
  display: flex;
  align-items: center;
}

.search-container {
  margin-bottom: 20px;
  padding: 15px;
  background-color: #ffffff;
  border-radius: 6px;
  border: 1px solid #ecf0f1;
}

.search-form {
  display: flex;
  align-items: center;
}

.search-form :deep(.el-form-item) {
  margin-bottom: 0;
  margin-right: 20px;
  display: flex;
  align-items: center;
}

.search-form :deep(.el-form-item__label) {
  line-height: 32px;
}

.search-form :deep(.el-form-item__content) {
  display: flex;
  align-items: center;
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

/* 确保下拉选择框的选项能够正确显示 */
:deep(.el-select-dropdown__item) {
  white-space: normal;
  height: auto;
  line-height: 1.5;
  padding: 8px 20px;
}

/* 状态图标样式 */
.status-icon {
  display: inline-flex;
  align-items: center;
  margin-right: 5px;
}

.el-icon-loading {
  animation: rotating 2s linear infinite;
}

@keyframes rotating {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

/* 使用fullscreen-container中的pagination-container样式 */
</style> 