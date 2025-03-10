<template>
  <div class="testcase-detail-container">
    <div class="header">
      <h2>测试用例详情</h2>
      <el-button @click="goBack">返回列表</el-button>
    </div>
    
    <el-card v-loading="loading">
      <template #header>
        <div class="card-header">
          <span>基本信息</span>
        </div>
      </template>
      
      <div class="info-content" v-if="testcase">
        <div class="info-item">
          <span class="label">用例名称:</span>
          <span class="value">{{ testcase.name }}</span>
        </div>
        <div class="info-item">
          <span class="label">优先级:</span>
          <span class="value">{{ getPriorityLabel(testcase.priority) }}</span>
        </div>
        <div class="info-item">
          <span class="label">状态:</span>
          <span class="value">{{ testcase.status_display || getStatusLabel(testcase.status) }}</span>
        </div>
        <div class="info-item">
          <span class="label">创建者:</span>
          <span class="value">{{ testcase.creator_name || '-' }}</span>
        </div>
        <div class="info-item">
          <span class="label">创建时间:</span>
          <span class="value">{{ formatDateTime(testcase.created_at) }}</span>
        </div>
        <div class="info-item">
          <span class="label">更新时间:</span>
          <span class="value">{{ formatDateTime(testcase.updated_at) }}</span>
        </div>
      </div>
      
      <div class="description-section" v-if="testcase">
        <div class="section-title">描述</div>
        <div class="section-content">{{ testcase.description || '无描述' }}</div>
      </div>
      
      <div class="steps-section" v-if="testcase">
        <div class="section-title">测试步骤</div>
        <div class="section-content">{{ testcase.steps || '无测试步骤' }}</div>
      </div>
      
      <div class="expected-results-section" v-if="testcase">
        <div class="section-title">预期结果</div>
        <div class="section-content">{{ testcase.expected_results || '无预期结果' }}</div>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { getTestCaseDetail } from '@/api/testcase'

const route = useRoute()
const router = useRouter()
const testcaseId = route.params.id
const loading = ref(false)
const testcase = ref(null)

// 获取测试用例详情
const fetchTestCaseDetail = async () => {
  loading.value = true
  try {
    const response = await getTestCaseDetail(testcaseId)
    testcase.value = response
  } catch (error) {
    console.error('获取测试用例详情失败:', error)
    ElMessage.error('获取测试用例详情失败')
  } finally {
    loading.value = false
  }
}

// 返回列表
const goBack = () => {
  // 检查是否有来源路由
  if (route.query.from === 'execution' && route.query.executionId) {
    // 如果是从测试执行详情页来的，则返回测试执行详情页
    router.push(`/executions/${route.query.executionId}`)
  } else {
    // 否则返回测试用例列表页
    router.push('/testcases')
  }
}

// 获取优先级标签
const getPriorityLabel = (priority) => {
  const priorityMap = {
    'high': '高',
    'medium': '中',
    'low': '低'
  }
  return priorityMap[priority] || priority
}

// 获取状态标签
const getStatusLabel = (status) => {
  const statusMap = {
    'active': '启用',
    'inactive': '禁用',
    'draft': '草稿'
  }
  return statusMap[status] || status
}

// 格式化日期时间
const formatDateTime = (dateTimeStr) => {
  if (!dateTimeStr) return '-'
  const date = new Date(dateTimeStr)
  return date.toLocaleString()
}

onMounted(() => {
  fetchTestCaseDetail()
})
</script>

<style scoped>
.testcase-detail-container {
  padding: 20px;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
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

.description-section,
.steps-section,
.expected-results-section {
  margin-top: 20px;
}
</style> 