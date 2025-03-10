<template>
  <div class="report-list-container">
    <div class="page-header">
      <h2>测试报告管理</h2>
    </div>
    
    <!-- 搜索栏 -->
    <div class="search-bar">
      <el-input
        v-model="searchKeyword"
        placeholder="搜索报告名称或测试计划"
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
        v-model="reportTypeFilter" 
        placeholder="报告类型" 
        clearable
        @change="handleSearch"
      >
        <el-option label="Allure报告" value="allure"></el-option>
        <el-option label="HTML报告" value="html"></el-option>
        <el-option label="PDF报告" value="pdf"></el-option>
      </el-select>
      
      <el-button type="primary" @click="handleGenerateReport">
        <el-icon><Plus /></el-icon>生成报告
      </el-button>
    </div>
    
    <!-- 报告列表 -->
    <el-table
      v-loading="loading"
      :data="reportList"
      border
      style="width: 100%"
    >
      <el-table-column prop="id" label="ID" width="80"></el-table-column>
      <el-table-column prop="name" label="报告名称" min-width="200"></el-table-column>
      <el-table-column prop="execution_name" label="测试计划" min-width="200"></el-table-column>
      <el-table-column prop="report_type_display" label="报告类型" width="120"></el-table-column>
      <el-table-column prop="creator_name" label="创建者" width="120"></el-table-column>
      <el-table-column prop="created_at" label="创建时间" width="180">
        <template #default="scope">
          {{ formatDateTime(scope.row.created_at) }}
        </template>
      </el-table-column>
      <el-table-column label="操作" width="250" fixed="right">
        <template #default="scope">
          <div class="operation-buttons">
            <el-button
              type="primary"
              size="small"
              @click="handleViewReport(scope.row)"
            >
              查看
            </el-button>
            <el-button
              type="success"
              size="small"
              @click="handleDownloadReport(scope.row)"
            >
              下载
            </el-button>
            <el-button
              type="danger"
              size="small"
              @click="handleDeleteReport(scope.row)"
            >
              删除
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
    
    <!-- 生成报告对话框 -->
    <el-dialog
      v-model="generateDialog.visible"
      title="生成测试报告"
      width="500px"
    >
      <el-form :model="generateDialog.form" label-width="100px">
        <el-form-item label="测试执行" required>
          <el-select v-model="generateDialog.form.executionId" placeholder="请选择测试执行" style="width: 100%">
            <el-option
              v-for="item in executionOptions"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            ></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="报告名称">
          <el-input v-model="generateDialog.form.name" placeholder="请输入报告名称（可选）"></el-input>
        </el-form-item>
        <el-form-item label="报告类型">
          <el-select v-model="generateDialog.form.reportType" placeholder="请选择报告类型" style="width: 100%">
            <el-option label="Allure报告" value="allure"></el-option>
            <el-option label="HTML报告" value="html"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="描述">
          <el-input
            v-model="generateDialog.form.description"
            type="textarea"
            placeholder="请输入报告描述（可选）"
            rows="3"
          ></el-input>
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
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Search, Plus } from '@element-plus/icons-vue'
import { getReports, generateReport, downloadReport, deleteReport } from '@/api/report'
import { getExecutionList } from '@/api/execution'
import { REPORT_API, getFullPath } from '@/utils/api-paths'

// 搜索条件
const searchKeyword = ref('')
const reportTypeFilter = ref('')

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
  }
})

// 获取报告列表
const fetchReportList = async () => {
  loading.value = true
  try {
    const params = {
      page: pagination.currentPage,
      page_size: pagination.pageSize,
      search: searchKeyword.value || undefined,
      report_type: reportTypeFilter.value || undefined
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
      label: `${item.plan_name || item.plan?.name} (ID: ${item.id})`,
      value: item.id
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
  if (!generateDialog.form.executionId) {
    ElMessage.warning('请选择测试执行')
    return
  }
  
  generateDialog.loading = true
  try {
    const data = {
      execution_id: generateDialog.form.executionId,
      report_type: generateDialog.form.reportType,
      name: generateDialog.form.name || undefined,
      description: generateDialog.form.description || undefined
    }
    
    const response = await generateReport(data)
    ElMessage.success('报告生成任务已提交，请稍后刷新查看')
    generateDialog.visible = false
    
    // 延迟刷新列表
    setTimeout(() => {
      fetchReportList()
    }, 3000)
  } catch (error) {
    console.error('生成报告失败:', error)
    ElMessage.error('生成报告失败: ' + (error.message || '未知错误'))
  } finally {
    generateDialog.loading = false
  }
}

// 处理查看报告
const handleViewReport = (row) => {
  // 在新窗口打开报告
  window.open(`/api${getFullPath(REPORT_API.VIEW(row.id))}`, '_blank')
}

// 处理下载报告
const handleDownloadReport = async (row) => {
  try {
    const response = await downloadReport(row.id)
    
    // 创建下载链接
    const url = window.URL.createObjectURL(new Blob([response]))
    const link = document.createElement('a')
    link.href = url
    link.setAttribute('download', `${row.name}.zip`)
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    
    ElMessage.success('报告下载成功')
  } catch (error) {
    console.error('下载报告失败:', error)
    ElMessage.error('下载报告失败')
  }
}

// 处理删除报告
const handleDeleteReport = (row) => {
  ElMessageBox.confirm(
    `确定要删除报告 "${row.name}" 吗？`,
    '删除确认',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    }
  ).then(async () => {
    try {
      await deleteReport(row.id)
      ElMessage.success('删除成功')
      fetchReportList()
    } catch (error) {
      console.error('删除报告失败:', error)
      ElMessage.error('删除报告失败')
    }
  }).catch(() => {
    // 取消删除
  })
}

// 格式化日期时间
const formatDateTime = (dateTimeStr) => {
  if (!dateTimeStr) return '-'
  const date = new Date(dateTimeStr)
  return date.toLocaleString()
}

onMounted(() => {
  fetchReportList()
})
</script>

<style scoped>
.report-list-container {
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

.operation-buttons {
  display: flex;
  gap: 5px;
}

.pagination-container {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}
</style> 