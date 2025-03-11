<template>
  <page-layout
    title="测试报告管理"
    description="查看和管理测试执行的报告，支持多种报告格式"
    class="report-list-page"
  >
    <!-- 页面操作按钮 -->
    <template #actions>
      <el-button type="primary" @click="handleGenerateReport">
        <el-icon><Plus /></el-icon>生成报告
      </el-button>
    </template>
    
    <!-- 搜索区域 -->
    <template #search>
      <search-panel
        v-model="searchForm"
        @search="handleSearch"
        @reset="resetSearch"
      >
        <el-form-item label="报告名称">
          <el-input
            v-model="searchForm.keyword"
            placeholder="搜索报告名称或测试计划"
            clearable
            @keyup.enter="handleSearch"
          >
            <template #prefix>
              <el-icon><Search /></el-icon>
            </template>
          </el-input>
        </el-form-item>
        
        <el-form-item label="报告类型">
          <el-select 
            v-model="searchForm.reportType" 
            placeholder="选择报告类型" 
            clearable
            style="width: 180px;"
          >
            <el-option label="Allure报告" value="allure"></el-option>
            <el-option label="HTML报告" value="html"></el-option>
            <el-option label="PDF报告" value="pdf"></el-option>
          </el-select>
        </el-form-item>
        
        <el-form-item label="创建时间">
          <el-date-picker
            v-model="searchForm.dateRange"
            type="daterange"
            range-separator="至"
            start-placeholder="开始日期"
            end-placeholder="结束日期"
            format="YYYY-MM-DD"
            value-format="YYYY-MM-DD"
            :shortcuts="dateShortcuts"
          />
        </el-form-item>
      </search-panel>
    </template>
    
    <!-- 数据表格 -->
    <data-table
      :data="reportList"
      :loading="loading"
      :total="pagination.total"
      :current-page="pagination.currentPage"
      :page-size="pagination.pageSize"
      :show-refresh="false"
      :show-settings="false"
      :actions-width="200"
      :actions-label="'操作'"
      @refresh="fetchReportList"
      @page-change="handleCurrentChange"
      @size-change="handleSizeChange"
      class="report-data-table"
    >
      <el-table-column prop="id" label="ID" width="80" align="center"></el-table-column>
      
      <el-table-column prop="name" label="报告名称" min-width="250">
        <template #default="scope">
          <div class="report-info">
            <el-icon class="report-icon"><Document /></el-icon>
            <div class="report-details">
              <div class="report-name">{{ scope.row.name }}</div>
              <div class="report-description" v-if="scope.row.description">
                {{ scope.row.description }}
              </div>
            </div>
          </div>
        </template>
      </el-table-column>
      
      <el-table-column prop="execution_name" label="测试计划" min-width="180">
        <template #default="scope">
          <el-link 
            type="primary" 
            :underline="false"
            @click="navigateToExecution(scope.row.execution)"
          >
            {{ scope.row.execution_name }}
          </el-link>
        </template>
      </el-table-column>
      
      <el-table-column prop="report_type" label="报告类型" width="150" align="center">
        <template #default="scope">
          <status-tag :status="scope.row.report_type" :text="scope.row.report_type_display" />
        </template>
      </el-table-column>
      
      <el-table-column prop="creator_name" label="创建者" width="120" align="center"></el-table-column>
      
      <el-table-column prop="created_at" label="创建时间" width="180">
        <template #default="scope">
          <div class="time-info">
            <div>{{ formatDate(scope.row.created_at) }}</div>
            <div class="time-ago">{{ timeAgo(scope.row.created_at) }}</div>
          </div>
        </template>
      </el-table-column>
      
      <template #actions="{ row }">
        <action-buttons
          :buttons="getActionButtons(row)"
          @click="handleActionClick"
        />
      </template>
    </data-table>
    
    <!-- 生成报告对话框 -->
    <el-dialog
      v-model="generateDialog.visible"
      title="生成测试报告"
      width="600px"
      destroy-on-close
      class="report-dialog"
    >
      <el-form 
        :model="generateDialog.form" 
        label-width="100px"
        :rules="generateDialog.rules"
        ref="generateFormRef"
      >
        <el-form-item label="测试执行" prop="executionId">
          <el-select 
            v-model="generateDialog.form.executionId" 
            placeholder="请选择测试执行" 
            style="width: 100%"
            filterable
            clearable
          >
            <el-option
              v-for="item in executionOptions"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            >
              <div class="execution-option">
                <div class="execution-option-name">{{ item.label }}</div>
                <div class="execution-option-info" v-if="item.info">{{ item.info }}</div>
              </div>
            </el-option>
          </el-select>
          <div class="form-tip">选择要为哪个测试执行生成报告</div>
        </el-form-item>
        
        <el-form-item label="报告名称" prop="name">
          <el-input 
            v-model="generateDialog.form.name" 
            placeholder="请输入报告名称（可选）"
            clearable
            :maxlength="100"
            show-word-limit
          >
            <template #prefix>
              <el-icon><Document /></el-icon>
            </template>
          </el-input>
          <div class="form-tip">报告名称将显示在报告列表中，建议使用简洁明了的名称</div>
        </el-form-item>
        
        <el-form-item label="报告类型" prop="reportType">
          <el-radio-group v-model="generateDialog.form.reportType">
            <el-radio-button label="allure">
              <el-tooltip content="交互式HTML报告，支持详细测试步骤和结果分析" placement="top">
                <div class="radio-content">
                  <el-icon><DataAnalysis /></el-icon>
                  <span>Allure报告</span>
                </div>
              </el-tooltip>
            </el-radio-button>
            <el-radio-button label="html">
              <el-tooltip content="简洁的HTML格式报告，适合快速查看" placement="top">
                <div class="radio-content">
                  <el-icon><Document /></el-icon>
                  <span>HTML报告</span>
                </div>
              </el-tooltip>
            </el-radio-button>
          </el-radio-group>
        </el-form-item>
        
        <el-form-item label="描述" prop="description">
          <el-input
            v-model="generateDialog.form.description"
            type="textarea"
            placeholder="请输入报告描述（可选）"
            rows="3"
            maxlength="200"
            show-word-limit
          >
          </el-input>
          <div class="form-tip">报告描述将显示在报告名称下方，可以添加关于此报告的更多信息</div>
        </el-form-item>
      </el-form>
      
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="generateDialog.visible = false">取消</el-button>
          <el-button type="primary" @click="submitGenerateReport" :loading="generateDialog.loading">
            生成
          </el-button>
        </span>
      </template>
    </el-dialog>
    
    <!-- 报告预览对话框 -->
    <el-dialog
      v-model="previewDialog.visible"
      :title="previewDialog.title"
      width="90%"
      fullscreen
      destroy-on-close
      class="preview-dialog"
    >
      <div class="preview-container">
        <iframe 
          v-if="previewDialog.url" 
          :src="previewDialog.url" 
          class="preview-iframe"
        ></iframe>
        <div v-else class="preview-loading">
          <el-empty description="加载中...">
            <el-button type="primary" @click="previewDialog.visible = false">关闭</el-button>
          </el-empty>
        </div>
      </div>
    </el-dialog>
  </page-layout>
</template>

<script setup>
import { ref, reactive, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { 
  Search, Plus, Document, InfoFilled, DataAnalysis,
  Download, View, Delete, Share
} from '@element-plus/icons-vue'
import { getReports, generateReport, downloadReport, deleteReport } from '@/api/report'
import { getExecutionList } from '@/api/execution'
import { REPORT_API } from '@/utils/api-paths'
import { formatDate, timeAgo } from '@/utils/date'

// 导入通用组件
import PageLayout from '@/components/common/PageLayout.vue'
import SearchPanel from '@/components/common/SearchPanel.vue'
import DataTable from '@/components/common/DataTable.vue'
import StatusTag from '@/components/common/StatusTag.vue'
import ActionButtons from '@/components/common/ActionButtons.vue'

const router = useRouter()

// 搜索表单
const searchForm = reactive({
  keyword: '',
  reportType: '',
  dateRange: []
})

// 日期快捷选项
const dateShortcuts = [
  {
    text: '最近一周',
    value: () => {
      const end = new Date()
      const start = new Date()
      start.setTime(start.getTime() - 3600 * 1000 * 24 * 7)
      return [start, end]
    }
  },
  {
    text: '最近一个月',
    value: () => {
      const end = new Date()
      const start = new Date()
      start.setTime(start.getTime() - 3600 * 1000 * 24 * 30)
      return [start, end]
    }
  },
  {
    text: '最近三个月',
    value: () => {
      const end = new Date()
      const start = new Date()
      start.setTime(start.getTime() - 3600 * 1000 * 24 * 90)
      return [start, end]
    }
  }
]

// 加载状态
const loading = ref(false)

// 报告列表
const reportList = ref([])

// 分页
const pagination = reactive({
  currentPage: 1,
  pageSize: 10,
  total: 0
})

// 测试执行选项
const executionOptions = ref([])

// 生成报告对话框
const generateDialog = reactive({
  visible: false,
  loading: false,
  form: {
    executionId: '',
    name: '',
    reportType: 'allure',
    description: ''
  },
  rules: {
    executionId: [
      { required: true, message: '请选择测试执行', trigger: 'change' }
    ],
    reportType: [
      { required: true, message: '请选择报告类型', trigger: 'change' }
    ]
  }
})
const generateFormRef = ref(null)

// 报告预览对话框
const previewDialog = reactive({
  visible: false,
  title: '',
  url: ''
})

// 获取报告列表
const fetchReportList = async () => {
  loading.value = true
  try {
    const params = {
      page: pagination.currentPage,
      page_size: pagination.pageSize,
      search: searchForm.keyword || undefined,
      report_type: searchForm.reportType || undefined
    }
    
    // 添加日期范围参数
    if (searchForm.dateRange && searchForm.dateRange.length === 2) {
      params.start_date = searchForm.dateRange[0]
      params.end_date = searchForm.dateRange[1]
    }
    
    const response = await getReports(params)
    reportList.value = response.results || []
    pagination.total = response.count || 0
  } catch (error) {
    console.error('获取报告列表失败:', error)
    ElMessage.error('获取报告列表失败')
  } finally {
    loading.value = false
  }
}

// 获取测试执行选项
const fetchExecutionOptions = async () => {
  try {
    const response = await getExecutionList({ status: 'completed' })
    executionOptions.value = (response || []).map(item => ({
      label: item.plan_name || item.plan?.name || `执行 #${item.id}`,
      value: item.id,
      info: `ID: ${item.id} | 完成时间: ${formatDate(item.end_time)}`
    }))
  } catch (error) {
    console.error('获取测试执行选项失败:', error)
    ElMessage.error('获取测试执行选项失败')
  }
}

// 处理搜索
const handleSearch = () => {
  pagination.currentPage = 1
  fetchReportList()
}

// 重置搜索
const resetSearch = () => {
  searchForm.keyword = ''
  searchForm.reportType = ''
  searchForm.dateRange = []
  pagination.currentPage = 1
  fetchReportList()
}

// 处理分页大小变化
const handleSizeChange = (size) => {
  pagination.pageSize = size
  fetchReportList()
}

// 处理当前页变化
const handleCurrentChange = (page) => {
  pagination.currentPage = page
  fetchReportList()
}

// 处理生成报告
const handleGenerateReport = () => {
  generateDialog.form = {
    executionId: '',
    name: '',
    reportType: 'allure',
    description: ''
  }
  generateDialog.visible = true
  fetchExecutionOptions()
}

// 提交生成报告
const submitGenerateReport = async () => {
  if (!generateFormRef.value) return
  
  try {
    await generateFormRef.value.validate()
    
    generateDialog.loading = true
    const data = {
      execution_id: generateDialog.form.executionId,
      report_type: generateDialog.form.reportType,
      name: generateDialog.form.name || undefined,
      description: generateDialog.form.description || undefined
    }
    
    await generateReport(data)
    ElMessage.success('报告生成任务已提交，请稍后刷新查看')
    generateDialog.visible = false
    
    // 延迟刷新列表
    setTimeout(() => {
      fetchReportList()
    }, 3000)
  } catch (error) {
    if (error === false) {
      // 表单验证失败
      return
    }
    console.error('生成报告失败:', error)
    ElMessage.error('生成报告失败: ' + (error.message || '未知错误'))
  } finally {
    generateDialog.loading = false
  }
}

// 获取操作按钮配置
const getActionButtons = (row) => {
  return [
    {
      key: 'view',
      text: '查看',
      tooltip: null,
      type: 'default',
      icon: null,
      class: 'action-view-btn'
    },
    {
      key: 'download',
      text: '下载',
      tooltip: null,
      type: 'success',
      icon: null,
      class: 'action-download-btn'
    },
    {
      key: 'delete',
      text: '删除',
      tooltip: null,
      type: 'danger',
      icon: null,
      class: 'action-delete-btn'
    }
  ]
}

// 处理操作按钮点击
const handleActionClick = (key, button, row) => {
  const reportRow = reportList.value.find(item => item.id === row.id)
  if (!reportRow) return
  
  switch (key) {
    case 'view':
      handleViewReport(reportRow)
      break
    case 'download':
      handleDownloadReport(reportRow)
      break
    case 'delete':
      handleDeleteReport(reportRow)
      break
  }
}

// 处理查看报告
const handleViewReport = (row) => {
  try {
    ElMessage.info('正在加载报告预览，请稍候...')
    
    // 设置预览对话框
    previewDialog.title = `报告预览: ${row.name || 'Report'}`
    previewDialog.url = `/api${REPORT_API.VIEW(row.id)}`
    previewDialog.visible = true
    
    // 记录查看操作
    console.log('查看报告:', row.id, row.name)
  } catch (error) {
    console.error('查看报告失败:', error)
    ElMessage.error('查看报告失败: ' + (error.message || '未知错误'))
  }
}

// 处理下载报告
const handleDownloadReport = async (row) => {
  try {
    ElMessage.info('正在准备下载报告，请稍候...')
    
    const response = await downloadReport(row.id)
    
    // 检查响应类型
    if (!(response instanceof Blob)) {
      console.error('下载报告响应不是Blob类型:', response)
      ElMessage.error('下载报告失败: 响应格式不正确')
      return
    }
    
    // 创建下载链接
    const url = window.URL.createObjectURL(response)
    const link = document.createElement('a')
    link.href = url
    link.setAttribute('download', `${row.name || 'report'}.zip`)
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    
    // 释放URL对象
    window.URL.revokeObjectURL(url)
    
    ElMessage.success('报告下载成功')
  } catch (error) {
    console.error('下载报告失败:', error)
    ElMessage.error('下载报告失败: ' + (error.message || '未知错误'))
  }
}

// 处理删除报告
const handleDeleteReport = (row) => {
  ElMessageBox.confirm(
    `确定要删除报告 "${row.name}" 吗？此操作不可恢复。`,
    '删除确认',
    {
      confirmButtonText: '确定删除',
      cancelButtonText: '取消',
      type: 'warning'
    }
  ).then(async () => {
    try {
      ElMessage.info('正在删除报告，请稍候...')
      await deleteReport(row.id)
      ElMessage.success('报告删除成功')
      // 刷新列表
      fetchReportList()
    } catch (error) {
      console.error('删除报告失败:', error)
      ElMessage.error('删除报告失败: ' + (error.message || '未知错误'))
    }
  }).catch(() => {
    // 用户取消删除
    ElMessage.info('已取消删除')
  })
}

// 处理分享报告
const handleShareReport = (row) => {
  const url = `${window.location.origin}/api${REPORT_API.VIEW(row.id)}`
  
  // 复制链接到剪贴板
  navigator.clipboard.writeText(url).then(() => {
    ElMessage.success('报告链接已复制到剪贴板')
  }).catch(() => {
    ElMessage.error('复制链接失败，请手动复制')
    // 显示链接供用户手动复制
    ElMessageBox.alert(url, '报告链接', {
      confirmButtonText: '确定',
      center: true,
      callback: () => {}
    })
  })
}

// 导航到测试执行详情
const navigateToExecution = (executionId) => {
  if (!executionId) return
  router.push(`/executions/${executionId}`)
}

// 报告类型状态映射
const reportTypeStatusMap = {
  allure: { type: 'success', icon: 'DataAnalysis', text: 'Allure报告' },
  html: { type: 'primary', icon: 'Document', text: 'HTML报告' },
  pdf: { type: 'warning', icon: 'Document', text: 'PDF报告' }
}

onMounted(() => {
  fetchReportList()
})
</script>

<style scoped>
.report-info {
  display: flex;
  align-items: flex-start;
  gap: var(--spacing-sm);
  padding: var(--spacing-xs) 0;
}

.report-icon {
  font-size: 20px;
  color: var(--primary-color);
  margin-top: 2px;
}

.report-details {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.report-name {
  font-weight: 500;
  color: var(--text-primary);
}

.report-description {
  font-size: var(--font-size-sm);
  color: var(--text-secondary);
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  text-overflow: ellipsis;
}

.time-info {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.time-ago {
  font-size: var(--font-size-xs);
  color: var(--text-secondary);
}

.form-tip {
  font-size: var(--font-size-xs);
  color: var(--text-secondary);
  margin-top: 4px;
  line-height: 1.4;
}

.execution-option {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.execution-option-name {
  font-weight: 500;
}

.execution-option-info {
  font-size: var(--font-size-xs);
  color: var(--text-secondary);
}

.radio-content {
  display: flex;
  align-items: center;
  gap: 5px;
}

.preview-container {
  height: calc(100vh - 120px);
  width: 100%;
  overflow: hidden;
}

.preview-iframe {
  width: 100%;
  height: 100%;
  border: none;
}

.preview-loading {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100%;
}

/* 添加以下样式确保页面内容可滚动 */
.report-list-page {
  height: 100%;
  overflow: auto;
}

.report-list-page :deep(.page-content) {
  height: calc(100vh - 120px);
  overflow: auto;
  padding-bottom: 60px; /* 确保底部有足够的空间 */
}

/* 调整数据表格上方的间距 */
.report-data-table {
  margin-top: -10px;
}

/* 操作栏按钮样式 */
:deep(.action-view-btn),
:deep(.action-download-btn),
:deep(.action-delete-btn) {
  padding: 6px 10px;
  margin: 0 2px;
}

:deep(.action-view-btn) {
  color: #409EFF;
  border-color: #409EFF;
  font-weight: 500;
}

:deep(.action-buttons) {
  display: flex;
  justify-content: space-around;
  width: 100%;
}

/* 确保报告类型标签居中显示 */
:deep(.el-table .cell) {
  display: flex;
  justify-content: center;
}

:deep(.el-table .el-table__cell:not(.is-center) .cell) {
  justify-content: flex-start;
}

/* 确保分页区域可见 */
.report-list-page :deep(.pagination-wrapper) {
  margin-top: 20px;
  position: sticky;
  bottom: 0;
  background-color: #fff;
  z-index: 10;
  padding: 10px 0;
}
</style> 