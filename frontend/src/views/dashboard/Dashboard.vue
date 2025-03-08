<template>
  <div class="dashboard-container fullscreen-container">
    <h2 class="dashboard-title">系统概览</h2>
    
    <div class="content-wrapper">
      <!-- 数据卡片 -->
      <div class="data-cards">
        <el-card class="data-card ocean-card" shadow="hover">
          <template #header>
            <div class="card-header">
              <span>项目数量</span>
              <el-tag type="success">活跃</el-tag>
            </div>
          </template>
          <div class="card-content">
            <div class="card-value">{{ summary.project_count || 0 }}</div>
            <div class="card-footer">
              <span>最近7天新增: {{ summary.recent_project_count || 0 }}</span>
            </div>
          </div>
        </el-card>
        
        <el-card class="data-card ocean-card" shadow="hover">
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
        
        <el-card class="data-card ocean-card" shadow="hover">
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
        
        <el-card class="data-card ocean-card" shadow="hover">
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
      <div class="chart-container">
        <el-card class="chart-card ocean-card" shadow="hover">
          <template #header>
            <div class="card-header">
              <span>测试用例状态分布</span>
            </div>
          </template>
          <div class="chart-wrapper">
            <div ref="testcaseStatusChart" class="chart"></div>
          </div>
        </el-card>
        
        <el-card class="chart-card ocean-card" shadow="hover">
          <template #header>
            <div class="card-header">
              <span>测试用例优先级分布</span>
            </div>
          </template>
          <div class="chart-wrapper">
            <div ref="testcasePriorityChart" class="chart"></div>
          </div>
        </el-card>
        
        <el-card class="chart-card ocean-card" shadow="hover">
          <template #header>
            <div class="card-header">
              <span>测试计划状态分布</span>
            </div>
          </template>
          <div class="chart-wrapper">
            <div ref="testplanStatusChart" class="chart"></div>
          </div>
        </el-card>
        
        <el-card class="chart-card ocean-card" shadow="hover">
          <template #header>
            <div class="card-header">
              <span>测试结果状态分布</span>
            </div>
          </template>
          <div class="chart-wrapper">
            <div ref="testresultStatusChart" class="chart"></div>
          </div>
        </el-card>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount, nextTick } from 'vue'
import { getSummary, getStatistics } from '@/api/dashboard'
import * as echarts from 'echarts/core'
import { PieChart } from 'echarts/charts'
import { TitleComponent, TooltipComponent, LegendComponent } from 'echarts/components'
import { LabelLayout } from 'echarts/features'
import { CanvasRenderer } from 'echarts/renderers'

// 注册必要的组件
echarts.use([
  PieChart,
  TitleComponent,
  TooltipComponent,
  LegendComponent,
  LabelLayout,
  CanvasRenderer
])

// 图表引用
const testcaseStatusChart = ref(null)
const testcasePriorityChart = ref(null)
const testplanStatusChart = ref(null)
const testresultStatusChart = ref(null)

// 图表实例
let testcaseStatusChartInstance = null
let testcasePriorityChartInstance = null
let testplanStatusChartInstance = null
let testresultStatusChartInstance = null

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
    summary.value = response || {}
  } catch (error) {
    console.error('获取概览数据失败:', error)
    // 不显示错误提示，只在控制台记录错误
    summary.value = {}
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
    statistics.value = response || {
      testcase_status: {},
      testcase_priority: {},
      testplan_status: {},
      testresult_status: {},
      testcase_trend: [],
      testresult_trend: []
    }
    
    // 获取数据后更新图表
    nextTick(() => {
      renderCharts()
    })
  } catch (error) {
    console.error('获取统计数据失败:', error)
    // 不显示错误提示，只在控制台记录错误
    statistics.value = {
      testcase_status: {},
      testcase_priority: {},
      testplan_status: {},
      testresult_status: {},
      testcase_trend: [],
      testresult_trend: []
    }
  }
}

// 渲染所有图表
const renderCharts = () => {
  renderTestcaseStatusChart()
  renderTestcasePriorityChart()
  renderTestplanStatusChart()
  renderTestresultStatusChart()
}

// 渲染测试用例状态分布图
const renderTestcaseStatusChart = () => {
  if (!testcaseStatusChart.value) return
  
  // 如果已存在实例，销毁它
  if (testcaseStatusChartInstance) {
    testcaseStatusChartInstance.dispose()
  }
  
  // 创建新实例
  testcaseStatusChartInstance = echarts.init(testcaseStatusChart.value)
  
  // 准备数据
  const data = Object.entries(statistics.value.testcase_status || {}).map(([status, count]) => ({
    name: getStatusText(status),
    value: count
  }))
  
  // 设置图表选项
  const option = {
    tooltip: {
      trigger: 'item',
      formatter: '{a} <br/>{b}: {c} ({d}%)'
    },
    legend: {
      orient: 'vertical',
      left: 'left',
      data: data.map(item => item.name)
    },
    series: [
      {
        name: '测试用例状态',
        type: 'pie',
        radius: ['40%', '70%'],
        avoidLabelOverlap: false,
        itemStyle: {
          borderRadius: 10,
          borderColor: '#fff',
          borderWidth: 2
        },
        label: {
          show: false,
          position: 'center'
        },
        emphasis: {
          label: {
            show: true,
            fontSize: '18',
            fontWeight: 'bold'
          }
        },
        labelLine: {
          show: false
        },
        data: data
      }
    ]
  }
  
  // 设置图表
  testcaseStatusChartInstance.setOption(option)
}

// 渲染测试用例优先级分布图
const renderTestcasePriorityChart = () => {
  if (!testcasePriorityChart.value) return
  
  // 如果已存在实例，销毁它
  if (testcasePriorityChartInstance) {
    testcasePriorityChartInstance.dispose()
  }
  
  // 创建新实例
  testcasePriorityChartInstance = echarts.init(testcasePriorityChart.value)
  
  // 准备数据
  const data = Object.entries(statistics.value.testcase_priority || {}).map(([priority, count]) => ({
    name: getPriorityText(priority),
    value: count
  }))
  
  // 设置图表选项
  const option = {
    tooltip: {
      trigger: 'item',
      formatter: '{a} <br/>{b}: {c} ({d}%)'
    },
    legend: {
      orient: 'vertical',
      left: 'left',
      data: data.map(item => item.name)
    },
    series: [
      {
        name: '测试用例优先级',
        type: 'pie',
        radius: ['40%', '70%'],
        avoidLabelOverlap: false,
        itemStyle: {
          borderRadius: 10,
          borderColor: '#fff',
          borderWidth: 2
        },
        label: {
          show: false,
          position: 'center'
        },
        emphasis: {
          label: {
            show: true,
            fontSize: '18',
            fontWeight: 'bold'
          }
        },
        labelLine: {
          show: false
        },
        data: data
      }
    ]
  }
  
  // 设置图表
  testcasePriorityChartInstance.setOption(option)
}

// 渲染测试计划状态分布图
const renderTestplanStatusChart = () => {
  if (!testplanStatusChart.value) return
  
  // 如果已存在实例，销毁它
  if (testplanStatusChartInstance) {
    testplanStatusChartInstance.dispose()
  }
  
  // 创建新实例
  testplanStatusChartInstance = echarts.init(testplanStatusChart.value)
  
  // 准备数据
  const data = Object.entries(statistics.value.testplan_status || {}).map(([status, count]) => ({
    name: getStatusText(status),
    value: count
  }))
  
  // 设置图表选项
  const option = {
    tooltip: {
      trigger: 'item',
      formatter: '{a} <br/>{b}: {c} ({d}%)'
    },
    legend: {
      orient: 'vertical',
      left: 'left',
      data: data.map(item => item.name)
    },
    series: [
      {
        name: '测试计划状态',
        type: 'pie',
        radius: ['40%', '70%'],
        avoidLabelOverlap: false,
        itemStyle: {
          borderRadius: 10,
          borderColor: '#fff',
          borderWidth: 2
        },
        label: {
          show: false,
          position: 'center'
        },
        emphasis: {
          label: {
            show: true,
            fontSize: '18',
            fontWeight: 'bold'
          }
        },
        labelLine: {
          show: false
        },
        data: data
      }
    ]
  }
  
  // 设置图表
  testplanStatusChartInstance.setOption(option)
}

// 渲染测试结果状态分布图
const renderTestresultStatusChart = () => {
  if (!testresultStatusChart.value) return
  
  // 如果已存在实例，销毁它
  if (testresultStatusChartInstance) {
    testresultStatusChartInstance.dispose()
  }
  
  // 创建新实例
  testresultStatusChartInstance = echarts.init(testresultStatusChart.value)
  
  // 准备数据
  const data = Object.entries(statistics.value.testresult_status || {}).map(([status, count]) => ({
    name: getResultStatusText(status),
    value: count
  }))
  
  // 设置图表选项
  const option = {
    tooltip: {
      trigger: 'item',
      formatter: '{a} <br/>{b}: {c} ({d}%)'
    },
    legend: {
      orient: 'vertical',
      left: 'left',
      data: data.map(item => item.name)
    },
    series: [
      {
        name: '测试结果状态',
        type: 'pie',
        radius: ['40%', '70%'],
        avoidLabelOverlap: false,
        itemStyle: {
          borderRadius: 10,
          borderColor: '#fff',
          borderWidth: 2
        },
        label: {
          show: false,
          position: 'center'
        },
        emphasis: {
          label: {
            show: true,
            fontSize: '18',
            fontWeight: 'bold'
          }
        },
        labelLine: {
          show: false
        },
        data: data
      }
    ]
  }
  
  // 设置图表
  testresultStatusChartInstance.setOption(option)
}

// 处理窗口大小变化
const handleResize = () => {
  testcaseStatusChartInstance?.resize()
  testcasePriorityChartInstance?.resize()
  testplanStatusChartInstance?.resize()
  testresultStatusChartInstance?.resize()
}

// 初始化
onMounted(() => {
  fetchSummary()
  fetchStatistics()
  
  // 添加窗口大小变化监听
  window.addEventListener('resize', handleResize)
})

// 清理
onBeforeUnmount(() => {
  // 移除窗口大小变化监听
  window.removeEventListener('resize', handleResize)
  
  // 销毁图表实例
  testcaseStatusChartInstance?.dispose()
  testcasePriorityChartInstance?.dispose()
  testplanStatusChartInstance?.dispose()
  testresultStatusChartInstance?.dispose()
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
    completed: '已完成',
    pending: '待处理',
    running: '运行中',
    paused: '已暂停',
    aborted: '已中止'
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
    skipped: '跳过',
    error: '错误',
    warning: '警告',
    not_run: '未运行',
    in_progress: '执行中'
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
  /* 移除原有的padding，使用fullscreen-container的padding */
  overflow-y: auto; /* 确保滚动条显示 */
  height: 100%; /* 设置高度以激活滚动 */
}

.dashboard-title {
  color: #2c3e50;
  font-size: 28px;
  margin-bottom: 25px;
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

.data-cards {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  margin-bottom: 20px;
}

.data-card {
  flex: 1;
  min-width: 250px;
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
  color: #3498db;
  margin-bottom: 10px;
  text-shadow: 0 0 10px rgba(52, 152, 219, 0.3);
}

.card-footer {
  font-size: 14px;
  color: #7f8c8d;
}

.project-selector {
  display: flex;
  align-items: center;
  margin-bottom: 20px;
  gap: 10px;
  background-color: rgba(255, 255, 255, 0.8);
  padding: 10px 15px;
  border-radius: 6px;
  border: 1px solid #ecf0f1;
}

.chart-container {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  flex: 1;
}

.chart-card {
  flex: 1;
  min-width: 45%;
  margin-bottom: 0;
}

.chart-wrapper {
  height: 300px;
  width: 100%;
}

.chart {
  height: 100%;
  width: 100%;
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
  padding: 15px;
  border-radius: 6px;
  background-color: rgba(255, 255, 255, 0.8);
  border: 1px solid #ecf0f1;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  
  &:hover {
    transform: translateY(-5px);
    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
  }
}

.stat-label {
  font-weight: bold;
  margin-bottom: 10px;
  color: #34495e;
}

.stat-value {
  font-size: 28px;
  background: linear-gradient(to right, #3498db, #2980b9);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  font-weight: bold;
}
</style> 