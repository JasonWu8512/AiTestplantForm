<template>
  <div class="dashboard-container">
    <h2>系统概览</h2>
    
    <!-- 数据卡片 -->
    <div class="data-cards">
      <el-card class="data-card" shadow="hover">
        <template #header>
          <div class="card-header">
            <span>项目数量</span>
            <el-tag type="success">活跃</el-tag>
          </div>
        </template>
        <div class="card-content">
          <div class="card-value">{{ summary.project_count || 0 }}</div>
          <div class="card-footer">
            <span>最近7天新增: {{ summary.recent_testcase_count || 0 }}</span>
          </div>
        </div>
      </el-card>
      
      <el-card class="data-card" shadow="hover">
        <template #header>
          <div class="card-header">
            <span>测试用例数量</span>
            <el-tag type="success">活跃</el-tag>
          </div>
        </template>
        <div class="card-content">
          <div class="card-value">{{ summary.testcase_count || 0 }}</div>
          <div class="card-footer">
            <span>最近7天新增: {{ summary.recent_testcase_count || 0 }}</span>
          </div>
        </div>
      </el-card>
      
      <el-card class="data-card" shadow="hover">
        <template #header>
          <div class="card-header">
            <span>测试计划数量</span>
            <el-tag type="primary">进行中</el-tag>
          </div>
        </template>
        <div class="card-content">
          <div class="card-value">{{ summary.testplan_count || 0 }}</div>
          <div class="card-footer">
            <span>最近7天新增: {{ summary.recent_testplan_count || 0 }}</span>
          </div>
        </div>
      </el-card>
      
      <el-card class="data-card" shadow="hover">
        <template #header>
          <div class="card-header">
            <span>测试执行数量</span>
            <el-tag type="warning">待执行</el-tag>
          </div>
        </template>
        <div class="card-content">
          <div class="card-value">{{ summary.execution_count || 0 }}</div>
          <div class="card-footer">
            <span>最近7天完成: {{ summary.recent_execution_count || 0 }}</span>
          </div>
        </div>
      </el-card>
    </div>
    
    <!-- 项目选择器 -->
    <div class="project-selector">
      <span>选择项目:</span>
      <el-select v-model="selectedProject" placeholder="全部项目" clearable @change="fetchStatistics">
        <el-option
          v-for="project in projects"
          :key="project.id"
          :label="project.name"
          :value="project.id"
        ></el-option>
      </el-select>
    </div>
    
    <!-- 统计数据 -->
    <div class="statistics-container">
      <el-card class="chart-card">
        <template #header>
          <div class="card-header">
            <span>测试用例状态分布</span>
          </div>
        </template>
        <div class="static-chart">
          <div v-for="(count, status) in statistics.testcase_status" :key="status" class="stat-item">
            <div class="stat-label">{{ getStatusText(status) }}</div>
            <div class="stat-value">{{ count }}</div>
          </div>
        </div>
      </el-card>
      
      <el-card class="chart-card">
        <template #header>
          <div class="card-header">
            <span>测试用例优先级分布</span>
          </div>
        </template>
        <div class="static-chart">
          <div v-for="(count, priority) in statistics.testcase_priority" :key="priority" class="stat-item">
            <div class="stat-label">{{ getPriorityText(priority) }}</div>
            <div class="stat-value">{{ count }}</div>
          </div>
        </div>
      </el-card>
      
      <el-card class="chart-card">
        <template #header>
          <div class="card-header">
            <span>测试计划状态分布</span>
          </div>
        </template>
        <div class="static-chart">
          <div v-for="(count, status) in statistics.testplan_status" :key="status" class="stat-item">
            <div class="stat-label">{{ getStatusText(status) }}</div>
            <div class="stat-value">{{ count }}</div>
          </div>
        </div>
      </el-card>
      
      <el-card class="chart-card">
        <template #header>
          <div class="card-header">
            <span>测试结果状态分布</span>
          </div>
        </template>
        <div class="static-chart">
          <div v-for="(count, status) in statistics.testresult_status" :key="status" class="stat-item">
            <div class="stat-label">{{ getResultStatusText(status) }}</div>
            <div class="stat-value">{{ count }}</div>
          </div>
        </div>
      </el-card>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'
import { getSummary, getStatistics } from '@/api/dashboard'

// 数据
const summary = ref({})
const statistics = ref({
  testcase_status: {},
  testcase_priority: {},
  testplan_status: {},
  testresult_status: {},
  testcase_trend: [],
  testresult_trend: []
})
const projects = ref([])
const selectedProject = ref(null)

// 获取概览数据
const fetchSummary = async () => {
  try {
    const response = await getSummary()
    summary.value = response
  } catch (error) {
    console.error('获取概览数据失败:', error)
  }
}

// 获取统计数据
const fetchStatistics = async () => {
  try {
    const params = {}
    if (selectedProject.value) {
      params.project = selectedProject.value
    }
    
    const response = await getStatistics(params)
    statistics.value = response
  } catch (error) {
    console.error('获取统计数据失败:', error)
  }
}

// 初始化
onMounted(() => {
  fetchSummary()
  fetchStatistics()
})

/**
 * 获取状态文本
 */
const getStatusText = (status) => {
  const statusMap = {
    draft: '草稿',
    active: '活跃',
    inactive: '不活跃',
    archived: '已归档',
    ready: '就绪',
    in_progress: '进行中',
    completed: '已完成'
  }
  return statusMap[status] || status
}

/**
 * 获取结果状态文本
 */
const getResultStatusText = (status) => {
  const statusMap = {
    pending: '待执行',
    passed: '通过',
    failed: '失败',
    blocked: '阻塞',
    skipped: '跳过'
  }
  return statusMap[status] || status
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
</script>

<style scoped>
.dashboard-container {
  padding: 20px;
}

.data-cards {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  margin-bottom: 20px;
}

.data-card {
  flex: 1;
  min-width: 200px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 10px 0;
}

.card-value {
  font-size: 36px;
  font-weight: bold;
  color: #409EFF;
  margin-bottom: 10px;
}

.card-footer {
  font-size: 14px;
  color: #909399;
}

.project-selector {
  display: flex;
  align-items: center;
  margin-bottom: 20px;
  gap: 10px;
}

.statistics-container {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20px;
  margin-top: 20px;
}

.chart-card {
  margin-bottom: 20px;
}

.static-chart {
  display: flex;
  flex-wrap: wrap;
  gap: 15px;
  padding: 20px;
}

.stat-item {
  flex: 1;
  min-width: 100px;
  text-align: center;
  padding: 10px;
  border-radius: 4px;
  background-color: #f5f7fa;
}

.stat-label {
  font-weight: bold;
  margin-bottom: 5px;
}

.stat-value {
  font-size: 24px;
  color: #409EFF;
}
</style> 