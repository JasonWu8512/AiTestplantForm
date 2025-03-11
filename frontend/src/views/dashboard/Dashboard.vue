<template>
  <div class="dashboard-container fullscreen-container">
    <div class="title-section">
      <h2 class="dashboard-title">系统概览</h2>
      <p class="page-description">查看测试项目的统计数据、执行状态和测试结果分析</p>
    </div>
    
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
        <span class="selector-label">选择项目:</span>
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
        
        <el-card class="chart-card ocean-card" shadow="hover">
          <template #header>
            <div class="card-header">
              <span>测试用例创建趋势</span>
            </div>
          </template>
          <div class="chart-wrapper">
            <div id="testcaseTrendChart" class="chart"></div>
          </div>
        </el-card>
        
        <el-card class="chart-card ocean-card" shadow="hover">
          <template #header>
            <div class="card-header">
              <span>测试结果趋势</span>
            </div>
          </template>
          <div class="chart-wrapper">
            <div id="testresultTrendChart" class="chart"></div>
          </div>
        </el-card>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount, nextTick } from 'vue'
import { getSummary, getStatistics } from '@/api/dashboard'
import { getProjects } from '@/api/testcase'
import * as echarts from 'echarts/core'
import { PieChart, BarChart, RadarChart } from 'echarts/charts'
import { 
  TitleComponent, 
  TooltipComponent, 
  LegendComponent,
  GridComponent,
  DatasetComponent,
  TransformComponent
} from 'echarts/components'
import { LabelLayout } from 'echarts/features'
import { CanvasRenderer } from 'echarts/renderers'

// 注册必要的组件
echarts.use([
  PieChart,
  BarChart,
  RadarChart,
  TitleComponent,
  TooltipComponent,
  LegendComponent,
  GridComponent,
  DatasetComponent,
  TransformComponent,
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
    
    console.log('获取统计数据，参数:', params)
    const response = await getStatistics(params)
    console.log('统计数据响应:', response)
    
    statistics.value = response || {
      testcase_status: {},
      testcase_priority: {},
      testplan_status: {},
      testresult_status: {},
      testcase_trend: [],
      testresult_trend: []
    }
    
    console.log('处理后的统计数据:', statistics.value)
    
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

// 获取项目列表
const loadProjects = async () => {
  try {
    console.log('加载项目列表')
    const response = await getProjects()
    console.log('项目列表响应:', response)
    
    // 根据实际后端返回的数据结构进行处理
    let projectsData = []
    
    if (response.results) {
      // 如果后端返回的是 { results: [...], count: ... } 格式
      projectsData = response.results
    } else if (response.data && response.data.items) {
      // 如果后端返回的是 { data: { items: [...], total: ... } } 格式
      projectsData = response.data.items
    } else if (Array.isArray(response)) {
      // 如果后端直接返回数组
      projectsData = response
    } else {
      console.error('未知的响应格式:', response)
      projectsData = []
    }
    
    projects.value = projectsData
    console.log('处理后的项目列表:', projects.value)
  } catch (error) {
    console.error('加载项目列表失败:', error)
    projects.value = []
  }
}

// 渲染所有图表
const renderCharts = () => {
  renderTestcaseStatusChart()
  renderTestcasePriorityChart()
  renderTestplanStatusChart()
  renderTestresultStatusChart()
  renderTestcaseTrendChart()
  renderTestresultTrendChart()
}

// 渲染测试用例状态分布图 - 使用饼图
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
    title: {
      text: '测试用例状态分布',
      left: 'center'
    },
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
        radius: '60%',
        center: ['50%', '60%'],
        data: data,
        emphasis: {
          itemStyle: {
            shadowBlur: 10,
            shadowOffsetX: 0,
            shadowColor: 'rgba(0, 0, 0, 0.5)'
          }
        },
        label: {
          show: true,
          formatter: '{b}: {c} ({d}%)'
        }
      }
    ]
  }
  
  // 设置图表
  testcaseStatusChartInstance.setOption(option)
}

// 渲染测试用例优先级分布图 - 使用柱状图
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
  
  // 排序数据（按优先级从高到低）
  const priorityOrder = { '最高': 0, '高': 1, '中': 2, '低': 3 }
  data.sort((a, b) => {
    return (priorityOrder[a.name] || 99) - (priorityOrder[b.name] || 99)
  })
  
  // 设置图表选项
  const option = {
    title: {
      text: '测试用例优先级分布',
      left: 'center'
    },
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'shadow'
      }
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      data: data.map(item => item.name),
      axisTick: {
        alignWithLabel: true
      }
    },
    yAxis: {
      type: 'value'
    },
    series: [
      {
        name: '用例数量',
        type: 'bar',
        barWidth: '60%',
        data: data.map(item => ({
          value: item.value,
          itemStyle: {
            color: getPriorityColor(item.name)
          }
        })),
        label: {
          show: true,
          position: 'top',
          formatter: '{c}'
        }
      }
    ]
  }
  
  // 设置图表
  testcasePriorityChartInstance.setOption(option)
}

// 渲染测试计划状态分布图 - 使用环形图
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
    title: {
      text: '测试计划状态分布',
      left: 'center'
    },
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
          show: true,
          position: 'outside',
          formatter: '{b}: {c}'
        },
        emphasis: {
          label: {
            show: true,
            fontSize: '18',
            fontWeight: 'bold'
          }
        },
        labelLine: {
          show: true
        },
        data: data.map(item => ({
          name: item.name,
          value: item.value,
          itemStyle: {
            color: getStatusColor(item.name)
          }
        }))
      }
    ]
  }
  
  // 设置图表
  testplanStatusChartInstance.setOption(option)
}

// 渲染测试结果状态分布图 - 使用雷达图
const renderTestresultStatusChart = () => {
  if (!testresultStatusChart.value) return
  
  // 如果已存在实例，销毁它
  if (testresultStatusChartInstance) {
    testresultStatusChartInstance.dispose()
  }
  
  // 创建新实例
  testresultStatusChartInstance = echarts.init(testresultStatusChart.value)
  
  // 准备数据
  const data = Object.entries(statistics.value.testresult_status || {})
  const indicators = data.map(([status, count]) => ({
    name: getResultStatusText(status),
    max: Math.max(...data.map(item => item[1])) * 1.2 // 设置最大值为数据最大值的1.2倍
  }))
  
  // 设置图表选项
  const option = {
    title: {
      text: '测试结果状态分布',
      left: 'center'
    },
    tooltip: {
      trigger: 'item'
    },
    legend: {
      orient: 'vertical',
      left: 'left',
      data: ['测试结果']
    },
    radar: {
      indicator: indicators,
      radius: '65%',
      center: ['50%', '60%'],
      name: {
        textStyle: {
          color: '#333',
          backgroundColor: '#eee',
          borderRadius: 3,
          padding: [3, 5]
        }
      },
      splitArea: {
        areaStyle: {
          color: ['rgba(114, 172, 209, 0.2)', 'rgba(114, 172, 209, 0.4)']
        }
      }
    },
    series: [
      {
        name: '测试结果状态',
        type: 'radar',
        data: [
          {
            value: data.map(item => item[1]),
            name: '测试结果',
            areaStyle: {
              color: 'rgba(52, 152, 219, 0.6)'
            },
            lineStyle: {
              color: 'rgba(52, 152, 219, 0.8)',
              width: 2
            },
            label: {
              show: true,
              formatter: '{c}'
            }
          }
        ]
      }
    ]
  }
  
  // 设置图表
  testresultStatusChartInstance.setOption(option)
}

// 渲染测试用例趋势图
const renderTestcaseTrendChart = () => {
  // 如果没有图表容器，直接返回
  if (!document.getElementById('testcaseTrendChart')) return
  
  // 如果已存在实例，销毁它
  if (window.testcaseTrendChartInstance) {
    window.testcaseTrendChartInstance.dispose()
  }
  
  // 创建新实例
  window.testcaseTrendChartInstance = echarts.init(document.getElementById('testcaseTrendChart'))
  
  // 准备数据
  const dates = statistics.value.testcase_trend.map(item => item.date)
  const counts = statistics.value.testcase_trend.map(item => item.count)
  
  // 设置图表选项
  const option = {
    title: {
      text: '测试用例创建趋势'
    },
    tooltip: {
      trigger: 'axis'
    },
    xAxis: {
      type: 'category',
      data: dates.reverse()
    },
    yAxis: {
      type: 'value'
    },
    series: [
      {
        name: '新增用例数',
        type: 'line',
        data: counts.reverse(),
        smooth: true,
        lineStyle: {
          width: 3,
          color: '#3498db'
        },
        areaStyle: {
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            {
              offset: 0,
              color: 'rgba(52, 152, 219, 0.5)'
            },
            {
              offset: 1,
              color: 'rgba(52, 152, 219, 0.1)'
            }
          ])
        }
      }
    ]
  }
  
  // 设置图表
  window.testcaseTrendChartInstance.setOption(option)
}

// 渲染测试结果趋势图
const renderTestresultTrendChart = () => {
  // 如果没有图表容器，直接返回
  if (!document.getElementById('testresultTrendChart')) return
  
  // 如果已存在实例，销毁它
  if (window.testresultTrendChartInstance) {
    window.testresultTrendChartInstance.dispose()
  }
  
  // 创建新实例
  window.testresultTrendChartInstance = echarts.init(document.getElementById('testresultTrendChart'))
  
  // 准备数据
  const dates = statistics.value.testresult_trend.map(item => item.date)
  const passedCounts = statistics.value.testresult_trend.map(item => item.passed)
  const failedCounts = statistics.value.testresult_trend.map(item => item.failed)
  
  // 设置图表选项
  const option = {
    title: {
      text: '测试结果趋势'
    },
    tooltip: {
      trigger: 'axis'
    },
    legend: {
      data: ['通过', '失败']
    },
    xAxis: {
      type: 'category',
      data: dates.reverse()
    },
    yAxis: {
      type: 'value'
    },
    series: [
      {
        name: '通过',
        type: 'line',
        data: passedCounts.reverse(),
        smooth: true,
        lineStyle: {
          width: 3,
          color: '#2ecc71'
        },
        areaStyle: {
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            {
              offset: 0,
              color: 'rgba(46, 204, 113, 0.5)'
            },
            {
              offset: 1,
              color: 'rgba(46, 204, 113, 0.1)'
            }
          ])
        }
      },
      {
        name: '失败',
        type: 'line',
        data: failedCounts.reverse(),
        smooth: true,
        lineStyle: {
          width: 3,
          color: '#e74c3c'
        },
        areaStyle: {
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            {
              offset: 0,
              color: 'rgba(231, 76, 60, 0.5)'
            },
            {
              offset: 1,
              color: 'rgba(231, 76, 60, 0.1)'
            }
          ])
        }
      }
    ]
  }
  
  // 设置图表
  window.testresultTrendChartInstance.setOption(option)
}

// 处理窗口大小变化
const handleResize = () => {
  testcaseStatusChartInstance?.resize()
  testcasePriorityChartInstance?.resize()
  testplanStatusChartInstance?.resize()
  testresultStatusChartInstance?.resize()
  window.testcaseTrendChartInstance?.resize()
  window.testresultTrendChartInstance?.resize()
}

// 初始化
onMounted(() => {
  fetchSummary()
  fetchStatistics()
  loadProjects()
  
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
  window.testcaseTrendChartInstance?.dispose()
  window.testresultTrendChartInstance?.dispose()
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

/**
 * 获取优先级颜色
 */
const getPriorityColor = (priority) => {
  const priorityColorMap = {
    '最高': '#e74c3c',
    '高': '#e67e22',
    '中': '#f1c40f',
    '低': '#3498db'
  }
  return priorityColorMap[priority] || '#95a5a6'
}

/**
 * 获取状态颜色
 */
const getStatusColor = (status) => {
  const statusColorMap = {
    '草稿': '#95a5a6',
    '活跃': '#2ecc71',
    '不活跃': '#7f8c8d',
    '已归档': '#34495e',
    '就绪': '#f1c40f',
    '进行中': '#3498db',
    '已完成': '#2ecc71',
    '待处理': '#e67e22',
    '运行中': '#3498db',
    '已暂停': '#f39c12',
    '已中止': '#e74c3c'
  }
  return statusColorMap[status] || '#95a5a6'
}
</script>

<style scoped>
.dashboard-container {
  padding: 20px;
  height: 100%;
}

.title-section {
  max-width: 70%;
  margin-bottom: 20px;
}

.dashboard-title {
  font-size: 24px;
  font-weight: 600;
  margin-bottom: 8px;
  position: relative;
  padding-bottom: 10px;
}

.dashboard-title::after {
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
  font-size: var(--font-size-md, 14px);
  margin-top: var(--spacing-sm, 8px);
  line-height: 1.5;
}

.content-wrapper {
  flex: 1;
  overflow-y: auto; /* 内容区域也可滚动 */
  padding-bottom: 20px; /* 底部添加一些内边距 */
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
  gap: 15px;
  background-color: rgba(255, 255, 255, 0.8);
  padding: 12px 15px;
  border-radius: 6px;
  border: 1px solid #ecf0f1;
  flex-wrap: nowrap; /* 防止换行 */
}

.selector-label {
  white-space: nowrap; /* 防止文本换行 */
  min-width: 70px; /* 给标签一个最小宽度 */
  font-weight: 500; /* 稍微加粗文字 */
  color: #606266; /* 使用Element Plus默认文字颜色 */
}

.project-selector .el-select {
  flex: 1; /* 让下拉框占据剩余空间 */
  min-width: 200px; /* 设置最小宽度 */
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