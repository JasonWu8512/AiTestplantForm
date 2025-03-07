<template>
  <div class="dashboard-container">
    <div class="page-container">
      <h2 class="page-title">仪表盘</h2>
      
      <el-row :gutter="20">
        <el-col :span="24">
          <el-card class="welcome-card">
            <h3>欢迎使用 AiTestPlantForm 测试平台</h3>
            <p>这是一个功能强大的测试管理平台，帮助您高效管理测试用例、测试计划和测试执行。</p>
          </el-card>
        </el-col>
      </el-row>
      
      <el-row :gutter="20" class="stat-row">
        <el-col :xs="24" :sm="12" :md="6">
          <el-card class="stat-card">
            <div class="stat-icon">
              <el-icon><user /></el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-title">用户数</div>
              <div class="stat-value">{{ stats.userCount || 0 }}</div>
            </div>
          </el-card>
        </el-col>
        
        <el-col :xs="24" :sm="12" :md="6">
          <el-card class="stat-card">
            <div class="stat-icon">
              <el-icon><document /></el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-title">测试用例</div>
              <div class="stat-value">{{ stats.testcaseCount || 0 }}</div>
            </div>
          </el-card>
        </el-col>
        
        <el-col :xs="24" :sm="12" :md="6">
          <el-card class="stat-card">
            <div class="stat-icon">
              <el-icon><calendar /></el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-title">测试计划</div>
              <div class="stat-value">{{ stats.testplanCount || 0 }}</div>
            </div>
          </el-card>
        </el-col>
        
        <el-col :xs="24" :sm="12" :md="6">
          <el-card class="stat-card">
            <div class="stat-icon">
              <el-icon><data-analysis /></el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-title">测试执行</div>
              <div class="stat-value">{{ stats.executionCount || 0 }}</div>
            </div>
          </el-card>
        </el-col>
      </el-row>
      
      <el-row :gutter="20" class="chart-row">
        <el-col :span="24">
          <el-card class="chart-card">
            <div class="chart-title">功能开发进度</div>
            <el-progress :percentage="40" :format="format" />
            <div class="progress-info">
              <p>第一阶段：环境搭建与基础功能 - <el-tag type="success">已完成</el-tag></p>
              <p>第二阶段：核心功能开发 - <el-tag type="warning">进行中</el-tag></p>
              <p>第三阶段：高级功能开发 - <el-tag type="info">未开始</el-tag></p>
              <p>第四阶段：扩展功能开发 - <el-tag type="info">未开始</el-tag></p>
              <p>第五阶段：优化与完善 - <el-tag type="info">未开始</el-tag></p>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { User, Document, Calendar, DataAnalysis } from '@element-plus/icons-vue'

// 统计数据
const stats = ref({
  userCount: 1,
  testcaseCount: 0,
  testplanCount: 0,
  executionCount: 0
})

// 格式化进度条
const format = (percentage) => {
  return `${percentage}%`
}

// 获取统计数据
const fetchStats = async () => {
  // 这里将来会从API获取数据
  // 目前使用模拟数据
  stats.value = {
    userCount: 1,
    testcaseCount: 0,
    testplanCount: 0,
    executionCount: 0
  }
}

// 初始化
onMounted(() => {
  fetchStats()
})
</script>

<style scoped>
.dashboard-container {
  min-height: 100%;
}

.welcome-card {
  margin-bottom: 20px;
  text-align: center;
  padding: 20px;
}

.welcome-card h3 {
  font-size: 24px;
  margin-bottom: 10px;
}

.stat-row {
  margin-bottom: 20px;
}

.stat-card {
  display: flex;
  align-items: center;
  padding: 20px;
  margin-bottom: 20px;
}

.stat-icon {
  font-size: 48px;
  color: #409EFF;
  margin-right: 20px;
}

.stat-info {
  flex: 1;
}

.stat-title {
  font-size: 16px;
  color: #666;
  margin-bottom: 5px;
}

.stat-value {
  font-size: 28px;
  font-weight: bold;
}

.chart-row {
  margin-bottom: 20px;
}

.chart-card {
  padding: 20px;
}

.chart-title {
  font-size: 18px;
  margin-bottom: 20px;
}

.progress-info {
  margin-top: 20px;
}

.progress-info p {
  margin: 10px 0;
}
</style> 