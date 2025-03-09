<template>
  <div class="test-plan-detail-container">
    <el-card class="detail-card">
      <template #header>
        <div class="card-header">
          <h2>{{ testPlan.name }}</h2>
          <el-tag :type="getStatusType(testPlan.status)">{{ testPlan.status }}</el-tag>
        </div>
      </template>
      
      <div class="plan-info">
        <div class="info-item">
          <span class="label">计划ID：</span>
          <span>{{ testPlan.id }}</span>
        </div>
        <div class="info-item">
          <span class="label">创建者：</span>
          <span>{{ testPlan.creator }}</span>
        </div>
        <div class="info-item">
          <span class="label">创建时间：</span>
          <span>{{ formatDate(testPlan.created_at) }}</span>
        </div>
        <div class="info-item">
          <span class="label">开始日期：</span>
          <span>{{ formatDate(testPlan.start_date) }}</span>
        </div>
        <div class="info-item">
          <span class="label">结束日期：</span>
          <span>{{ formatDate(testPlan.end_date) }}</span>
        </div>
        <div class="info-item description">
          <span class="label">描述：</span>
          <span>{{ testPlan.description }}</span>
        </div>
      </div>
    </el-card>

    <el-card class="test-cases-card">
      <template #header>
        <div class="card-header">
          <h3>测试用例列表</h3>
          <el-button type="primary" size="small" @click="showAddCasesDialog">添加测试用例</el-button>
        </div>
      </template>
      
      <el-table :data="testCases" style="width: 100%" v-loading="loading">
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="name" label="用例名称" />
        <el-table-column prop="priority" label="优先级" width="100">
          <template #default="scope">
            <el-tag :type="getPriorityType(scope.row.priority)">{{ scope.row.priority }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="status" label="状态" width="100">
          <template #default="scope">
            <el-tag :type="getStatusType(scope.row.status)">{{ scope.row.status }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="150">
          <template #default="scope">
            <el-button size="small" type="danger" class="remove-button" @click="removeTestCase(scope.row.id)">移除</el-button>
          </template>
        </el-table-column>
      </el-table>
      
      <div class="pagination-container">
        <el-pagination
          background
          layout="prev, pager, next"
          :total="totalCases"
          :page-size="pageSize"
          @current-change="handlePageChange"
        />
      </div>
    </el-card>

    <!-- 添加测试用例对话框 -->
    <el-dialog
      title="添加测试用例"
      v-model="addCasesDialogVisible"
      width="70%"
    >
      <el-table
        :data="availableTestCases"
        style="width: 100%"
        v-loading="loadingAvailableCases"
        @selection-change="handleSelectionChange"
      >
        <el-table-column type="selection" width="55" />
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="name" label="用例名称" />
        <el-table-column prop="priority" label="优先级" width="100">
          <template #default="scope">
            <el-tag :type="getPriorityType(scope.row.priority)">{{ scope.row.priority }}</el-tag>
          </template>
        </el-table-column>
      </el-table>
      
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="addCasesDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="addTestCases">确认</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import { ref, reactive, onMounted, onErrorCaptured } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage, ElMessageBox, ElLoading } from 'element-plus'
import { getTestPlanById, getTestPlanCases, addCasesToTestPlan, removeCaseFromTestPlan } from '@/api/testplan'
import { getTestCases } from '@/api/testcase'

// 日志工具函数
const logInfo = (message, data) => {
  console.info(`[TestPlanDetail] ${message}`, data || '')
}

const logError = (message, error) => {
  console.error(`[TestPlanDetail] ${message}`, error)
  // 可以在这里添加错误上报逻辑
}

export default {
  name: 'TestPlanDetail',
  
  setup() {
    const route = useRoute()
    const router = useRouter()
    const planId = route.params.id
    
    // 验证planId是否为有效数字
    if (!planId || isNaN(Number(planId))) {
      ElMessage.error('无效的测试计划ID')
      router.push('/testplans')
      return {}
    }
    
    logInfo(`加载测试计划详情，ID: ${planId}`)
    
    const testPlan = ref({})
    const testCases = ref([])
    const availableTestCases = ref([])
    const selectedCases = ref([])
    const loading = ref(false)
    const loadingAvailableCases = ref(false)
    const addCasesDialogVisible = ref(false)
    const totalCases = ref(0)
    const pageSize = ref(10)
    const currentPage = ref(1)
    const loadingInstance = ref(null)
    
    // 全局错误处理
    onErrorCaptured((err, instance, info) => {
      logError('组件错误被捕获', { err, info })
      ElMessage.error('操作过程中发生错误，请稍后重试')
      return false // 阻止错误继续传播
    })
    
    // 显示全局加载
    const showFullScreenLoading = (text = '加载中...') => {
      loadingInstance.value = ElLoading.service({
        lock: true,
        text: text,
        background: 'rgba(0, 0, 0, 0.7)'
      })
    }
    
    // 隐藏全局加载
    const hideFullScreenLoading = () => {
      if (loadingInstance.value) {
        loadingInstance.value.close()
      }
    }
    
    // 处理API错误
    const handleApiError = (error, message) => {
      logError(message, error)
      
      // 根据错误类型提供更具体的反馈
      if (error.response) {
        const status = error.response.status
        const data = error.response.data
        
        if (status === 404) {
          ElMessage.error('请求的资源不存在')
        } else if (status === 403) {
          ElMessage.error('您没有权限执行此操作')
        } else if (status === 401) {
          ElMessage.error('会话已过期，请重新登录')
          // 可以在这里添加重定向到登录页的逻辑
        } else if (data && data.message) {
          ElMessage.error(`操作失败: ${data.message}`)
        } else {
          ElMessage.error(message || '操作失败，请稍后重试')
        }
      } else if (error.request) {
        ElMessage.error('网络请求失败，请检查您的网络连接')
      } else {
        ElMessage.error(message || '操作失败，请稍后重试')
      }
    }
    
    // 获取测试计划详情
    const fetchTestPlanDetail = async () => {
      loading.value = true
      logInfo(`开始获取测试计划详情，ID: ${planId}`)
      
      try {
        const response = await getTestPlanById(planId)
        
        // 数据验证
        if (!response || !response.data) {
          throw new Error('返回数据格式不正确')
        }
        
        testPlan.value = response.data
        logInfo('测试计划详情获取成功', testPlan.value)
        
        // 显示成功提示
        ElMessage({
          type: 'success',
          message: '测试计划详情加载成功',
          duration: 2000
        })
      } catch (error) {
        handleApiError(error, '获取测试计划详情失败')
      } finally {
        loading.value = false
      }
    }
    
    // 获取测试计划关联的测试用例
    const fetchTestCases = async () => {
      loading.value = true
      logInfo(`开始获取测试计划关联的测试用例，计划ID: ${planId}，页码: ${currentPage.value}`)
      
      try {
        const response = await getTestPlanCases(planId, {
          page: currentPage.value,
          limit: pageSize.value
        })
        
        // 数据验证
        if (!response || !response.data || !Array.isArray(response.data.items)) {
          throw new Error('返回数据格式不正确')
        }
        
        testCases.value = response.data.items
        totalCases.value = response.data.total || 0
        
        logInfo(`测试用例获取成功，共 ${totalCases.value} 条记录`, testCases.value)
      } catch (error) {
        handleApiError(error, '获取测试用例失败')
      } finally {
        loading.value = false
      }
    }
    
    // 获取可添加的测试用例
    const fetchAvailableTestCases = async () => {
      loadingAvailableCases.value = true
      logInfo('开始获取可添加的测试用例')
      
      try {
        const response = await getTestCases()
        
        // 数据验证
        if (!response || !response.data || !Array.isArray(response.data.items)) {
          throw new Error('返回数据格式不正确')
        }
        
        // 过滤掉已经添加到测试计划的用例
        const currentCaseIds = testCases.value.map(c => c.id)
        availableTestCases.value = response.data.items.filter(
          c => !currentCaseIds.includes(c.id)
        )
        
        logInfo(`可添加的测试用例获取成功，共 ${availableTestCases.value.length} 条记录`, availableTestCases.value)
        
        // 如果没有可添加的测试用例，提示用户
        if (availableTestCases.value.length === 0) {
          ElMessage({
            type: 'info',
            message: '没有可添加的测试用例',
            duration: 3000
          })
        }
      } catch (error) {
        handleApiError(error, '获取可用测试用例失败')
      } finally {
        loadingAvailableCases.value = false
      }
    }
    
    // 显示添加测试用例对话框
    const showAddCasesDialog = () => {
      logInfo('打开添加测试用例对话框')
      addCasesDialogVisible.value = true
      fetchAvailableTestCases()
    }
    
    // 处理选择变化
    const handleSelectionChange = (selection) => {
      selectedCases.value = selection
      logInfo(`已选择 ${selection.length} 个测试用例`)
    }
    
    // 添加测试用例到测试计划
    const addTestCases = async () => {
      // 数据验证
      if (selectedCases.value.length === 0) {
        ElMessage({
          type: 'warning',
          message: '请选择要添加的测试用例',
          duration: 3000
        })
        return
      }
      
      logInfo(`开始添加测试用例到测试计划，选择了 ${selectedCases.value.length} 个测试用例`)
      showFullScreenLoading('正在添加测试用例...')
      
      try {
        const caseIds = selectedCases.value.map(c => c.id)
        
        // 验证caseIds数组
        if (!Array.isArray(caseIds) || caseIds.some(id => !id || isNaN(Number(id)))) {
          throw new Error('测试用例ID无效')
        }
        
        await addCasesToTestPlan(planId, { case_ids: caseIds })
        
        logInfo('测试用例添加成功', caseIds)
        
        ElMessage({
          type: 'success',
          message: `成功添加 ${caseIds.length} 个测试用例`,
          duration: 3000
        })
        
        addCasesDialogVisible.value = false
        await fetchTestCases() // 刷新测试用例列表
      } catch (error) {
        handleApiError(error, '添加测试用例失败')
      } finally {
        hideFullScreenLoading()
      }
    }
    
    // 从测试计划中移除测试用例
    const removeTestCase = async (caseId) => {
      // 数据验证
      if (!caseId || isNaN(Number(caseId))) {
        ElMessage.error('无效的测试用例ID')
        return
      }
      
      logInfo(`准备移除测试用例，ID: ${caseId}`)
      
      try {
        const confirmResult = await ElMessageBox.confirm(
          '确定要从测试计划中移除该测试用例吗？此操作不会删除测试用例本身。',
          '移除确认',
          {
            confirmButtonText: '确定移除',
            cancelButtonText: '取消',
            type: 'warning',
            distinguishCancelAndClose: true
          }
        )
        
        showFullScreenLoading('正在移除测试用例...')
        
        await removeCaseFromTestPlan(planId, caseId)
        
        logInfo(`测试用例移除成功，ID: ${caseId}`)
        
        ElMessage({
          type: 'success',
          message: '测试用例已成功从测试计划中移除',
          duration: 3000
        })
        
        await fetchTestCases() // 刷新测试用例列表
      } catch (error) {
        if (error === 'cancel' || error === 'close') {
          logInfo('用户取消了移除操作')
        } else {
          handleApiError(error, '移除测试用例失败')
        }
      } finally {
        hideFullScreenLoading()
      }
    }
    
    // 处理分页变化
    const handlePageChange = (page) => {
      logInfo(`分页变化，当前页: ${page}`)
      currentPage.value = page
      fetchTestCases()
    }
    
    // 格式化日期
    const formatDate = (dateString) => {
      if (!dateString) return '未设置'
      try {
        const date = new Date(dateString)
        if (isNaN(date.getTime())) {
          return '日期格式错误'
        }
        return date.toLocaleDateString()
      } catch (error) {
        logError('日期格式化错误', { dateString, error })
        return '日期格式错误'
      }
    }
    
    // 获取优先级对应的类型
    const getPriorityType = (priority) => {
      const types = {
        '高': 'danger',
        '中': 'warning',
        '低': 'info'
      }
      return types[priority] || 'info'
    }
    
    // 获取状态对应的类型
    const getStatusType = (status) => {
      const types = {
        '未开始': 'info',
        '进行中': 'warning',
        '已完成': 'success',
        '已取消': 'danger'
      }
      return types[status] || 'info'
    }
    
    onMounted(() => {
      logInfo('组件挂载完成，开始初始化数据')
      fetchTestPlanDetail()
      fetchTestCases()
    })
    
    return {
      testPlan,
      testCases,
      availableTestCases,
      loading,
      loadingAvailableCases,
      addCasesDialogVisible,
      totalCases,
      pageSize,
      currentPage,
      showAddCasesDialog,
      handleSelectionChange,
      addTestCases,
      removeTestCase,
      handlePageChange,
      formatDate,
      getPriorityType,
      getStatusType
    }
  }
}
</script>

<style scoped>
.test-plan-detail-container {
  padding: 20px;
}

.detail-card, .test-cases-card {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.plan-info {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 15px;
}

.info-item {
  display: flex;
}

.info-item.description {
  grid-column: span 2;
}

.label {
  font-weight: bold;
  margin-right: 10px;
  color: #606266;
}

.pagination-container {
  margin-top: 20px;
  display: flex;
  justify-content: center;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
}

/* 移除按钮样式优化 */
.remove-button {
  font-weight: 600;
  color: #fff !important;
  text-shadow: 0 1px 1px rgba(0, 0, 0, 0.2);
  padding: 6px 12px;
}

.remove-button:hover {
  background-color: #f56c6c;
  border-color: #f56c6c;
  color: #fff !important;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}
</style> 