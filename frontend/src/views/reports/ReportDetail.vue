<template>
  <div class="report-detail-container">
    <div class="header">
      <h2>测试报告详情</h2>
      <div class="header-actions">
        <el-button @click="goBack">返回列表</el-button>
        <el-button type="primary" @click="handleViewReport">查看报告</el-button>
        <el-button type="success" @click="handleDownloadReport">下载报告</el-button>
      </div>
    </div>
    
    <el-card v-loading="loading">
      <template #header>
        <div class="card-header">
          <span>基本信息</span>
        </div>
      </template>
      
      <div class="info-content" v-if="report">
        <div class="info-item">
          <span class="label">报告名称:</span>
          <span class="value">{{ report.name }}</span>
        </div>
        <div class="info-item">
          <span class="label">测试计划:</span>
          <span class="value">{{ report.execution_name }}</span>
        </div>
        <div class="info-item">
          <span class="label">报告类型:</span>
          <span class="value">{{ report.report_type_display }}</span>
        </div>
        <div class="info-item">
          <span class="label">创建者:</span>
          <span class="value">{{ report.creator_name || '-' }}</span>
        </div>
        <div class="info-item">
          <span class="label">创建时间:</span>
          <span class="value">{{ formatDateTime(report.created_at) }}</span>
        </div>
        <div class="info-item">
          <span class="label">更新时间:</span>
          <span class="value">{{ formatDateTime(report.updated_at) }}</span>
        </div>
      </div>
      
      <div class="description-section" v-if="report">
        <div class="section-title">描述</div>
        <div class="section-content">{{ report.description || '无描述' }}</div>
      </div>
    </el-card>
    
    <el-card class="report-preview" v-if="report && report.report_type === 'html'">
      <template #header>
        <div class="card-header">
          <span>报告预览</span>
        </div>
      </template>
      
      <iframe :src="`/api${getFullPath(REPORT_API.VIEW(reportId))}`" class="preview-iframe"></iframe>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { getReportDetail, downloadReport } from '@/api/report'
import { REPORT_API, getFullPath } from '@/utils/api-paths'

const route = useRoute()
const router = useRouter()
const reportId = route.params.id
const loading = ref(false)
const report = ref(null)

// 获取报告详情
const fetchReportDetail = async () => {
  loading.value = true
  try {
    const response = await getReportDetail(reportId)
    report.value = response
  } catch (error) {
    console.error('获取报告详情失败:', error)
    ElMessage.error('获取报告详情失败')
  } finally {
    loading.value = false
  }
}

// 返回列表
const goBack = () => {
  router.push('/reports')
}

// 查看报告
const handleViewReport = () => {
  window.open(`/api${getFullPath(REPORT_API.VIEW(reportId))}`, '_blank')
}

// 下载报告
const handleDownloadReport = async () => {
  try {
    const response = await downloadReport(reportId)
    
    // 创建下载链接
    const url = window.URL.createObjectURL(new Blob([response]))
    const link = document.createElement('a')
    link.href = url
    link.setAttribute('download', `${report.value.name}.zip`)
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    
    ElMessage.success('报告下载成功')
  } catch (error) {
    console.error('下载报告失败:', error)
    ElMessage.error('下载报告失败')
  }
}

// 格式化日期时间
const formatDateTime = (dateTimeStr) => {
  if (!dateTimeStr) return '-'
  const date = new Date(dateTimeStr)
  return date.toLocaleString()
}

onMounted(() => {
  fetchReportDetail()
})
</script>

<style scoped>
.report-detail-container {
  padding: 20px;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.header-actions {
  display: flex;
  gap: 10px;
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
  margin-bottom: 20px;
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

.section-title {
  font-weight: bold;
  font-size: 16px;
  margin-bottom: 10px;
  color: #303133;
  border-bottom: 1px solid #EBEEF5;
  padding-bottom: 10px;
}

.section-content {
  margin-bottom: 20px;
  white-space: pre-line;
}

.description-section {
  margin-top: 20px;
}

.report-preview {
  margin-top: 20px;
}

.preview-iframe {
  width: 100%;
  height: 600px;
  border: none;
}
</style> 