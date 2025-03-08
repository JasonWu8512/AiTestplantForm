<template>
  <div class="execution-list-container">
    <div class="execution-header">
      <h2>测试执行管理</h2>
      <div class="execution-actions">
        <el-button type="primary" @click="handleCreateFromPlan">从测试计划创建</el-button>
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
          <el-button type="primary" @click="handleSearch">搜索</el-button>
          <el-button @click="resetSearch">重置</el-button>
        </el-form-item>
      </el-form>
    </div>

    <!-- 测试执行列表 -->
    <el-table
      v-loading="loading"
      :data="executionList"
      border
      style="width: 100%"
      @row-click="handleRowClick"
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
            @click.stop="handleStart(scope.row)"
          >
            开始执行
          </el-button>
          <el-button
            v-if="scope.row.status === 'running'"
            type="warning"
            size="small"
            @click.stop="handlePause(scope.row)"
          >
            暂停
          </el-button>
          <el-button
            v-if="scope.row.status === 'paused'"
            type="success"
            size="small"
            @click.stop="handleStart(scope.row)"
          >
            继续执行
          </el-button>
          <el-button
            v-if="['running', 'paused'].includes(scope.row.status)"
            type="info"
            size="small"
            @click.stop="handleComplete(scope.row)"
          >
            完成
          </el-button>
          <el-button
            v-if="['pending', 'running', 'paused'].includes(scope.row.status)"
            type="danger"
            size="small"
            @click.stop="handleAbort(scope.row)"
          >
            中止
          </el-button>
          <el-button
            type="primary"
            size="small"
            @click.stop="handleView(scope.row)"
          >
            查看
          </el-button>
          <el-button
            v-if="scope.row.status === 'pending'"
            type="danger"
            size="small"
            @click.stop="handleDelete(scope.row)"
          >
            删除
          </el-button>
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

    <!-- 从测试计划创建测试执行对话框 -->
    <el-dialog
      v-model="createDialog.visible"
      title="从测试计划创建测试执行"
      width="600px"
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
          <el-button type="primary" @click="confirmCreateFromPlan" :loading="createDialog.loading">
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
    const response = await getExecutionList(params)
    executionList.value = response.results
    pagination.total = response.count
  } catch (error) {
    console.error('获取测试执行列表失败:', error)
    ElMessage.error('获取测试执行列表失败')
  } finally {
    loading.value = false
  }
}

// 获取测试计划列表
const fetchTestPlanList = async () => {
  try {
    const response = await getTestPlans({ status: 'ready,in_progress' })
    planOptions.value = response.results
  } catch (error) {
    console.error('获取测试计划列表失败:', error)
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
const formatDateTime = (dateTimeStr) => {
  const date = new Date(dateTimeStr)
  return date.toLocaleString()
}

// 行点击
const handleRowClick = (row) => {
  router.push(`/executions/${row.id}`)
}

// 查看测试执行
const handleView = (row) => {
  router.push(`/executions/${row.id}`)
}

// 从测试计划创建测试执行
const handleCreateFromPlan = () => {
  createDialog.form.planId = null
  createDialog.form.remarks = ''
  createDialog.visible = true
  fetchTestPlanList()
}

// 确认从测试计划创建测试执行
const confirmCreateFromPlan = async () => {
  if (!createDialog.form.planId) {
    ElMessage.warning('请选择测试计划')
    return
  }

  createDialog.loading = true
  try {
    const data = {
      remarks: createDialog.form.remarks
    }
    await createExecutionFromPlan(createDialog.form.planId, data)
    ElMessage.success('创建测试执行成功')
    createDialog.visible = false
    fetchExecutionList()
  } catch (error) {
    console.error('创建测试执行失败:', error)
    ElMessage.error('创建测试执行失败')
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
    await ElMessageBox.confirm('确定要中止此测试执行吗?', '提示', {
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
    await ElMessageBox.confirm('确定要删除此测试执行吗?', '提示', {
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
  fetchExecutionList()
})
</script>

<style scoped>
.execution-list-container {
  padding: 20px;
}

.execution-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.search-container {
  margin-bottom: 20px;
  padding: 15px;
  background-color: #f5f7fa;
  border-radius: 4px;
}

.pagination-container {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}
</style> 