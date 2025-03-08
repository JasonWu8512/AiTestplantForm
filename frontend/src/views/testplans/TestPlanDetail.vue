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
            <el-button size="small" type="danger" @click="removeTestCase(scope.row.id)">移除</el-button>
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
import { ref, reactive, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { getTestPlanById, getTestPlanCases, addCasesToTestPlan, removeCaseFromTestPlan } from '@/api/testplan'
import { getTestCases } from '@/api/testcase'

export default {
  name: 'TestPlanDetail',
  
  setup() {
    const route = useRoute()
    const planId = route.params.id
    
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
    
    // 获取测试计划详情
    const fetchTestPlanDetail = async () => {
      loading.value = true
      try {
        const response = await getTestPlanById(planId)
        testPlan.value = response.data
      } catch (error) {
        ElMessage.error('获取测试计划详情失败')
        console.error(error)
      } finally {
        loading.value = false
      }
    }
    
    // 获取测试计划关联的测试用例
    const fetchTestCases = async () => {
      loading.value = true
      try {
        const response = await getTestPlanCases(planId, {
          page: currentPage.value,
          limit: pageSize.value
        })
        testCases.value = response.data.items
        totalCases.value = response.data.total
      } catch (error) {
        ElMessage.error('获取测试用例失败')
        console.error(error)
      } finally {
        loading.value = false
      }
    }
    
    // 获取可添加的测试用例
    const fetchAvailableTestCases = async () => {
      loadingAvailableCases.value = true
      try {
        const response = await getTestCases()
        // 过滤掉已经添加到测试计划的用例
        const currentCaseIds = testCases.value.map(c => c.id)
        availableTestCases.value = response.data.items.filter(
          c => !currentCaseIds.includes(c.id)
        )
      } catch (error) {
        ElMessage.error('获取可用测试用例失败')
        console.error(error)
      } finally {
        loadingAvailableCases.value = false
      }
    }
    
    // 显示添加测试用例对话框
    const showAddCasesDialog = () => {
      addCasesDialogVisible.value = true
      fetchAvailableTestCases()
    }
    
    // 处理选择变化
    const handleSelectionChange = (selection) => {
      selectedCases.value = selection
    }
    
    // 添加测试用例到测试计划
    const addTestCases = async () => {
      if (selectedCases.value.length === 0) {
        ElMessage.warning('请选择要添加的测试用例')
        return
      }
      
      try {
        const caseIds = selectedCases.value.map(c => c.id)
        await addCasesToTestPlan(planId, { case_ids: caseIds })
        ElMessage.success('添加测试用例成功')
        addCasesDialogVisible.value = false
        fetchTestCases() // 刷新测试用例列表
      } catch (error) {
        ElMessage.error('添加测试用例失败')
        console.error(error)
      }
    }
    
    // 从测试计划中移除测试用例
    const removeTestCase = async (caseId) => {
      try {
        await ElMessageBox.confirm('确定要从测试计划中移除该测试用例吗？', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        })
        
        await removeCaseFromTestPlan(planId, caseId)
        ElMessage.success('移除测试用例成功')
        fetchTestCases() // 刷新测试用例列表
      } catch (error) {
        if (error !== 'cancel') {
          ElMessage.error('移除测试用例失败')
          console.error(error)
        }
      }
    }
    
    // 处理分页变化
    const handlePageChange = (page) => {
      currentPage.value = page
      fetchTestCases()
    }
    
    // 格式化日期
    const formatDate = (dateString) => {
      if (!dateString) return '未设置'
      const date = new Date(dateString)
      return date.toLocaleDateString()
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
</style> 