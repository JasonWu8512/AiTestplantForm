<template>
  <div class="testplan-list-container fullscreen-container">
    <div class="page-header">
      <h2>测试计划管理</h2>
      <el-button type="primary" @click="handleAddTestPlan">
        <el-icon><Plus /></el-icon>新建测试计划
      </el-button>
    </div>
    
    <!-- 搜索栏 -->
    <div class="search-bar">
      <el-input
        v-model="searchKeyword"
        placeholder="搜索测试计划名称或描述"
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
      
      <el-select v-model="projectFilter" placeholder="选择项目" clearable @change="handleSearch">
        <el-option
          v-for="item in projectOptions"
          :key="item.value"
          :label="item.label"
          :value="item.value"
        />
      </el-select>
      
      <el-select v-model="statusFilter" placeholder="状态" clearable @change="handleSearch">
        <el-option label="草稿" value="draft" />
        <el-option label="就绪" value="ready" />
        <el-option label="进行中" value="in_progress" />
        <el-option label="已完成" value="completed" />
        <el-option label="已归档" value="archived" />
      </el-select>
    </div>
    
    <div class="content-wrapper">
      <!-- 测试计划列表 -->
      <div class="table-container">
        <el-table
          v-loading="loading"
          :data="testPlanList"
          border
          style="width: 100%"
          height="100%"
        >
          <el-table-column prop="id" label="ID" width="80" />
          <el-table-column prop="name" label="计划名称" min-width="150" show-overflow-tooltip />
          <el-table-column prop="description" label="描述" min-width="200" show-overflow-tooltip />
          <el-table-column prop="status_display" label="状态" width="100">
            <template #default="scope">
              <el-tag :type="getStatusType(scope.row.status)">
                {{ scope.row.status_display || getStatusText(scope.row.status) }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="project_name" label="所属项目" width="150" />
          <el-table-column prop="test_cases_count" label="测试用例数" width="120" />
          <el-table-column prop="creator_name" label="创建者" width="120" />
          <el-table-column label="时间范围" width="180">
            <template #default="scope">
              <div v-if="scope.row.start_time || scope.row.end_time">
                {{ formatDate(scope.row.start_time) }} 至 {{ formatDate(scope.row.end_time) }}
              </div>
              <div v-else>未设置</div>
            </template>
          </el-table-column>
          <el-table-column label="操作" width="250" fixed="right">
            <template #default="scope">
              <el-button size="small" @click="handleViewTestPlan(scope.row)">
                查看
              </el-button>
              <el-button size="small" type="primary" @click="handleEditTestPlan(scope.row)">
                编辑
              </el-button>
              <el-button 
                size="small" 
                type="danger" 
                @click="handleDeleteTestPlan(scope.row)"
              >
                删除
              </el-button>
            </template>
          </el-table-column>
        </el-table>
      </div>
      
      <!-- 分页 -->
      <div class="pagination-container">
        <el-pagination
          v-model:current-page="currentPage"
          v-model:page-size="pageSize"
          :page-sizes="[10, 20, 50, 100]"
          layout="total, sizes, prev, pager, next, jumper"
          :total="total"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        />
      </div>
    </div>
    
    <!-- 测试计划表单对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="dialogType === 'add' ? '新建测试计划' : dialogType === 'edit' ? '编辑测试计划' : '查看测试计划'"
      width="800px"
    >
      <el-form
        ref="testPlanFormRef"
        :model="testPlanForm"
        :rules="testPlanRules"
        label-width="100px"
        :disabled="dialogType === 'view'"
      >
        <el-form-item label="计划名称" prop="name">
          <el-input v-model="testPlanForm.name" placeholder="请输入计划名称" />
        </el-form-item>
        
        <el-form-item label="所属项目" prop="project">
          <el-select v-model="testPlanForm.project" placeholder="请选择项目">
            <el-option
              v-for="item in projectOptions"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            />
          </el-select>
        </el-form-item>
        
        <el-form-item label="状态" prop="status">
          <el-select v-model="testPlanForm.status" placeholder="请选择状态">
            <el-option label="草稿" value="draft" />
            <el-option label="就绪" value="ready" />
            <el-option label="进行中" value="in_progress" />
            <el-option label="已完成" value="completed" />
            <el-option label="已归档" value="archived" />
          </el-select>
        </el-form-item>
        
        <el-form-item label="时间范围">
          <el-date-picker
            v-model="timeRange"
            type="datetimerange"
            range-separator="至"
            start-placeholder="开始时间"
            end-placeholder="结束时间"
            format="YYYY-MM-DD HH:mm:ss"
            value-format="YYYY-MM-DD HH:mm:ss"
          />
        </el-form-item>
        
        <el-form-item label="计划描述" prop="description">
          <el-input
            v-model="testPlanForm.description"
            type="textarea"
            rows="4"
            placeholder="请输入计划描述"
          />
        </el-form-item>
        
        <el-form-item label="测试用例" v-if="dialogType !== 'add'">
          <div class="test-cases-section">
            <div class="test-cases-header">
              <span>已关联测试用例 ({{ testCases.length }})</span>
              <el-button type="primary" size="small" @click="handleAddTestCases" v-if="dialogType === 'edit'">
                <el-icon><Plus /></el-icon>添加测试用例
              </el-button>
            </div>
            
            <el-table
              v-loading="testCasesLoading"
              :data="testCases"
              border
              class="test-cases-table"
              style="width: 100%"
              max-height="300"
              v-if="testCases.length > 0"
              :header-cell-style="{background:'#f5f7fa', color: '#606266'}"
            >
              <el-table-column prop="case_detail.id" label="ID" width="80" />
              <el-table-column prop="case_detail.name" label="用例名称" min-width="150" show-overflow-tooltip />
              <el-table-column prop="case_detail.priority_display" label="优先级" width="100">
                <template #default="scope">
                  <el-tag :type="getPriorityType(scope.row.case_detail.priority)" effect="light">
                    {{ scope.row.case_detail.priority_display }}
                  </el-tag>
                </template>
              </el-table-column>
              <el-table-column prop="order" label="执行顺序" width="100" />
              <el-table-column label="操作" width="150" v-if="dialogType === 'edit'">
                <template #default="scope">
                  <el-button size="small" type="danger" @click="handleRemoveTestCase(scope.row)" text>
                    <el-icon><Delete /></el-icon>移除
                  </el-button>
                </template>
              </el-table-column>
            </el-table>
            
            <div class="no-data" v-else>
              <el-empty description="暂无关联的测试用例" :image-size="80"></el-empty>
            </div>
          </div>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">{{ dialogType === 'view' ? '关闭' : '取消' }}</el-button>
          <el-button type="primary" @click="submitTestPlanForm" v-if="dialogType !== 'view'">确定</el-button>
        </span>
      </template>
    </el-dialog>
    
    <!-- 添加测试用例对话框 -->
    <el-dialog
      v-model="addCasesDialogVisible"
      title="添加测试用例"
      width="800px"
    >
      <div class="search-bar">
        <el-input
          v-model="caseSearchKeyword"
          placeholder="搜索测试用例名称"
          clearable
          @clear="handleCaseSearch"
          @keyup.enter="handleCaseSearch"
        >
          <template #append>
            <el-button @click="handleCaseSearch">
              <el-icon><Search /></el-icon>
            </el-button>
          </template>
        </el-input>
        
        <el-select v-model="casePriorityFilter" placeholder="优先级" clearable @change="handleCaseSearch">
          <el-option label="最高 (P0)" value="P0" />
          <el-option label="高 (P1)" value="P1" />
          <el-option label="中 (P2)" value="P2" />
          <el-option label="低 (P3)" value="P3" />
        </el-select>
      </div>
      
      <el-table
        v-loading="availableCasesLoading"
        :data="availableCases"
        border
        style="width: 100%"
        max-height="400"
        @selection-change="handleSelectionChange"
      >
        <el-table-column type="selection" width="55" />
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="name" label="用例名称" min-width="150" show-overflow-tooltip />
        <el-table-column prop="priority_display" label="优先级" width="100">
          <template #default="scope">
            <el-tag :type="getPriorityType(scope.row.priority)">
              {{ scope.row.priority_display || getPriorityText(scope.row.priority) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="status_display" label="状态" width="100">
          <template #default="scope">
            <el-tag :type="getStatusType(scope.row.status)">
              {{ scope.row.status_display || getStatusText(scope.row.status) }}
            </el-tag>
          </template>
        </el-table-column>
      </el-table>
      
      <div class="pagination-container">
        <el-pagination
          v-model:current-page="casesCurrentPage"
          v-model:page-size="casesPageSize"
          :page-sizes="[10, 20, 50, 100]"
          layout="total, sizes, prev, pager, next, jumper"
          :total="casesTotal"
          @size-change="handleCaseSizeChange"
          @current-change="handleCaseCurrentChange"
        />
      </div>
      
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="addCasesDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="submitAddTestCases" :disabled="selectedCases.length === 0">
            添加所选用例 ({{ selectedCases.length }})
          </el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed, watch } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus, Search, Delete } from '@element-plus/icons-vue'
import { useRouter } from 'vue-router'
import { getTestPlans, createTestPlan, updateTestPlan, deleteTestPlan, getTestPlanById, getTestPlanCases, addCasesToTestPlan, removeCaseFromTestPlan } from '@/api/testplan'
import { getProjects, getTestCases } from '@/api/testcase'

// 路由
const router = useRouter()

// 数据
const loading = ref(false)
const testPlanList = ref([])
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(0)
const searchKeyword = ref('')
const statusFilter = ref('')
const projectFilter = ref('')
const projectOptions = ref([])

// 对话框
const dialogVisible = ref(false)
const dialogType = ref('add') // 'add', 'edit', 'view'
const testPlanFormRef = ref(null)
const testPlanForm = reactive({
  id: null,
  name: '',
  description: '',
  status: 'draft',
  project: null,
  start_time: null,
  end_time: null
})
const timeRange = ref([])

// 测试用例相关
const testCases = ref([])
const testCasesLoading = ref(false)
const addCasesDialogVisible = ref(false)
const availableCases = ref([])
const availableCasesLoading = ref(false)
const selectedCases = ref([])
const caseSearchKeyword = ref('')
const casePriorityFilter = ref('')
const casesCurrentPage = ref(1)
const casesPageSize = ref(10)
const casesTotal = ref(0)

// 表单验证规则
const testPlanRules = {
  name: [
    { required: true, message: '请输入计划名称', trigger: 'blur' },
    { min: 2, max: 200, message: '长度在 2 到 200 个字符', trigger: 'blur' }
  ],
  project: [
    { required: true, message: '请选择项目', trigger: 'change' }
  ],
  status: [
    { required: true, message: '请选择状态', trigger: 'change' }
  ]
}

// 监听时间范围变化
watch(timeRange, (newValue) => {
  if (newValue && newValue.length === 2) {
    testPlanForm.start_time = newValue[0]
    testPlanForm.end_time = newValue[1]
  } else {
    testPlanForm.start_time = null
    testPlanForm.end_time = null
  }
})

// 生命周期钩子
onMounted(async () => {
  // 加载项目选项
  await loadProjectOptions()
  
  // 加载测试计划列表
  fetchTestPlans()
})

// 方法
/**
 * 加载项目选项
 */
const loadProjectOptions = async () => {
  try {
    console.log('加载项目选项')
    const response = await getProjects()
    console.log('项目选项响应:', response)
    
    // 根据实际后端返回的数据结构进行处理
    let projects = []
    
    if (response.results) {
      // 如果后端返回的是 { results: [...], count: ... } 格式
      projects = response.results
    } else if (response.data && response.data.items) {
      // 如果后端返回的是 { data: { items: [...], total: ... } } 格式
      projects = response.data.items
    } else if (Array.isArray(response)) {
      // 如果后端直接返回数组
      projects = response
    } else {
      console.error('未知的响应格式:', response)
      projects = []
    }
    
    projectOptions.value = projects.map(project => ({
      value: project.id,
      label: project.name
    }))
    
    console.log('处理后的项目选项:', projectOptions.value)
  } catch (error) {
    console.error('加载项目选项失败:', error)
    projectOptions.value = []
    ElMessage.error('加载项目选项失败')
  }
}

/**
 * 获取测试计划列表
 */
const fetchTestPlans = async () => {
  loading.value = true
  try {
    const params = {
      page: currentPage.value,
      page_size: pageSize.value,
      search: searchKeyword.value || undefined
    }
    
    if (projectFilter.value) {
      params.project_id = projectFilter.value
    }
    
    if (statusFilter.value) {
      params.status = statusFilter.value
    }
    
    console.log('获取测试计划列表，参数:', params)
    const response = await getTestPlans(params)
    console.log('测试计划列表响应:', response)
    
    // 根据实际后端返回的数据结构进行处理
    if (response.results) {
      // 如果后端返回的是 { results: [...], count: ... } 格式
      testPlanList.value = response.results
      total.value = response.count || 0
    } else if (response.data && response.data.items) {
      // 如果后端返回的是 { data: { items: [...], total: ... } } 格式
      testPlanList.value = response.data.items
      total.value = response.data.total || 0
    } else if (Array.isArray(response)) {
      // 如果后端直接返回数组
      testPlanList.value = response
      total.value = response.length
    } else {
      // 其他情况，记录错误并设置为空数组
      console.error('未知的响应格式:', response)
      testPlanList.value = []
      total.value = 0
    }
    
    console.log('处理后的测试计划列表:', testPlanList.value)
  } catch (error) {
    console.error('获取测试计划列表失败:', error)
    testPlanList.value = []
    total.value = 0
    ElMessage.error('获取测试计划列表失败')
  } finally {
    loading.value = false
  }
}

/**
 * 处理搜索
 */
const handleSearch = () => {
  currentPage.value = 1
  fetchTestPlans()
}

/**
 * 处理页码变化
 */
const handleCurrentChange = (val) => {
  currentPage.value = val
  fetchTestPlans()
}

/**
 * 处理每页条数变化
 */
const handleSizeChange = (val) => {
  pageSize.value = val
  currentPage.value = 1
  fetchTestPlans()
}

/**
 * 处理添加测试计划
 */
const handleAddTestPlan = () => {
  dialogType.value = 'add'
  testPlanForm.id = null
  testPlanForm.name = ''
  testPlanForm.description = ''
  testPlanForm.status = 'draft'
  testPlanForm.project = null
  testPlanForm.start_time = null
  testPlanForm.end_time = null
  timeRange.value = []
  testCases.value = []
  
  dialogVisible.value = true
}

/**
 * 处理查看测试计划
 */
const handleViewTestPlan = (row) => {
  dialogType.value = 'view'
  loadTestPlanDetail(row.id)
}

/**
 * 处理编辑测试计划
 */
const handleEditTestPlan = (row) => {
  dialogType.value = 'edit'
  loadTestPlanDetail(row.id)
}

/**
 * 加载测试计划详情
 */
const loadTestPlanDetail = async (id) => {
  try {
    console.log('加载测试计划详情，ID:', id)
    const response = await getTestPlanById(id)
    console.log('测试计划详情响应:', response)
    
    // 根据实际后端返回的数据结构进行处理
    let testPlan = null
    
    if (response.data) {
      // 如果后端返回的是 { data: ... } 格式
      testPlan = response.data
    } else {
      // 如果后端直接返回对象
      testPlan = response
    }
    
    if (!testPlan) {
      console.error('测试计划详情为空')
      ElMessage.warning('无法加载测试计划详情')
      return
    }
    
    // 填充表单
    testPlanForm.id = testPlan.id
    testPlanForm.name = testPlan.name
    testPlanForm.description = testPlan.description || ''
    // 确保使用正确的属性名
    testPlanForm.project = testPlan.project_id || testPlan.project
    testPlanForm.status = testPlan.status
    
    // 设置时间范围
    if (testPlan.start_time && testPlan.end_time) {
      timeRange.value = [testPlan.start_time, testPlan.end_time]
    } else if (testPlan.start_date && testPlan.end_date) {
      timeRange.value = [testPlan.start_date, testPlan.end_date]
    } else {
      timeRange.value = []
    }
    
    // 加载测试用例
    loadTestCases(id)
    
    dialogVisible.value = true
  } catch (error) {
    console.error('获取测试计划详情失败:', error)
    ElMessage.error('获取测试计划详情失败')
  }
}

/**
 * 加载测试用例
 */
const loadTestCases = async (planId) => {
  testCasesLoading.value = true;
  try {
    console.log('加载测试计划关联的测试用例，计划ID:', planId);
    // 使用getTestPlanById获取测试计划详情，其中包含测试用例
    const response = await getTestPlanById(planId);
    console.log('测试计划详情响应:', response);
    
    // 根据实际后端返回的数据结构进行处理
    let testPlanData = null;
    
    if (response.data) {
      // 如果后端返回的是 { data: ... } 格式
      testPlanData = response.data;
    } else {
      // 如果后端直接返回对象
      testPlanData = response;
    }
    
    if (!testPlanData) {
      console.error('测试计划详情为空');
      testCases.value = [];
      return;
    }
    
    // 从测试计划详情中获取测试用例
    if (testPlanData.test_cases) {
      testCases.value = testPlanData.test_cases;
    } else {
      console.error('测试计划中没有测试用例数据');
      testCases.value = [];
    }
    
    console.log('处理后的测试用例列表:', testCases.value);
  } catch (error) {
    console.error('获取测试用例失败:', error);
    testCases.value = [];
    ElMessage.error('获取测试用例失败');
  } finally {
    testCasesLoading.value = false;
  }
}

/**
 * 处理删除测试计划
 */
const handleDeleteTestPlan = (row) => {
  ElMessageBox.confirm(
    '确定要删除该测试计划吗？删除后不可恢复。',
    '警告',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    }
  ).then(async () => {
    try {
      await deleteTestPlan(row.id)
      ElMessage.success('删除成功')
      fetchTestPlans()
    } catch (error) {
      console.error('删除测试计划失败:', error)
      ElMessage.error('删除测试计划失败')
    }
  }).catch(() => {
    // 取消删除
  })
}

/**
 * 提交测试计划表单
 */
const submitTestPlanForm = async () => {
  if (!testPlanFormRef.value) return
  
  await testPlanFormRef.value.validate(async (valid) => {
    if (valid) {
      try {
        console.log('提交测试计划表单:', testPlanForm)
        
        // 创建一个新对象，避免修改原始对象
        const formData = {
          name: testPlanForm.name,
          description: testPlanForm.description,
          status: testPlanForm.status,
          project: testPlanForm.project,
          start_time: testPlanForm.start_time,
          end_time: testPlanForm.end_time
        }
        
        let response
        if (dialogType.value === 'add') {
          response = await createTestPlan(formData)
          console.log('创建测试计划成功，响应:', response)
          ElMessage.success('创建成功')
        } else {
          response = await updateTestPlan(testPlanForm.id, formData)
          console.log('更新测试计划成功，响应:', response)
          ElMessage.success('更新成功')
        }
        
        dialogVisible.value = false
        
        // 确保在关闭对话框后重新获取测试计划列表
        await fetchTestPlans()
        console.log('刷新后的测试计划列表:', testPlanList.value)
      } catch (error) {
        console.error('保存测试计划失败:', error)
        ElMessage.error('保存测试计划失败')
      }
    }
  })
}

/**
 * 处理添加测试用例
 */
const handleAddTestCases = () => {
  // 重置搜索条件
  caseSearchKeyword.value = ''
  casePriorityFilter.value = ''
  casesCurrentPage.value = 1
  selectedCases.value = []
  
  // 加载可用的测试用例
  fetchAvailableCases()
  
  addCasesDialogVisible.value = true
}

/**
 * 获取可用的测试用例
 */
const fetchAvailableCases = async () => {
  availableCasesLoading.value = true
  try {
    const params = {
      page: casesCurrentPage.value,
      page_size: casesPageSize.value,
      project: testPlanForm.project,
      status: 'active'
    }
    
    if (caseSearchKeyword.value) {
      params.search = caseSearchKeyword.value
    }
    
    if (casePriorityFilter.value) {
      params.priority = casePriorityFilter.value
    }
    
    console.log('获取可用测试用例，参数:', params)
    const response = await getTestCases(params)
    console.log('可用测试用例响应:', response)
    
    // 根据实际后端返回的数据结构进行处理
    let cases = []
    let totalCount = 0
    
    if (response.results) {
      // 如果后端返回的是 { results: [...], count: ... } 格式
      cases = response.results
      totalCount = response.count || 0
    } else if (response.data && response.data.items) {
      // 如果后端返回的是 { data: { items: [...], total: ... } } 格式
      cases = response.data.items
      totalCount = response.data.total || 0
    } else if (response.data && Array.isArray(response.data)) {
      // 如果后端返回的是 { data: [...] } 格式
      cases = response.data
      totalCount = response.data.length
    } else if (Array.isArray(response)) {
      // 如果后端直接返回数组
      cases = response
      totalCount = response.length
    } else {
      // 其他情况，记录错误并设置为空数组
      console.error('未知的响应格式:', response)
      cases = []
      totalCount = 0
    }
    
    // 过滤掉已经关联的测试用例
    const existingCaseIds = testCases.value.map(item => {
      // 根据实际数据结构获取 case_id
      if (item.case_detail && item.case_detail.id) {
        return item.case_detail.id
      } else if (item.case_id) {
        return item.case_id
      } else if (item.id) {
        return item.id
      }
      return null
    }).filter(id => id !== null)
    
    availableCases.value = cases.filter(item => !existingCaseIds.includes(item.id))
    casesTotal.value = totalCount
    
    console.log('处理后的可用测试用例:', availableCases.value)
  } catch (error) {
    console.error('获取可用测试用例失败:', error)
    availableCases.value = []
    casesTotal.value = 0
    ElMessage.error('获取可用测试用例失败')
  } finally {
    availableCasesLoading.value = false
  }
}

/**
 * 处理测试用例搜索
 */
const handleCaseSearch = () => {
  casesCurrentPage.value = 1
  fetchAvailableCases()
}

/**
 * 处理测试用例页码变化
 */
const handleCaseCurrentChange = (val) => {
  casesCurrentPage.value = val
  fetchAvailableCases()
}

/**
 * 处理测试用例每页条数变化
 */
const handleCaseSizeChange = (val) => {
  casesPageSize.value = val
  casesCurrentPage.value = 1
  fetchAvailableCases()
}

/**
 * 处理选择变化
 */
const handleSelectionChange = (selection) => {
  selectedCases.value = selection
}

/**
 * 提交添加测试用例
 */
const submitAddTestCases = async () => {
  if (selectedCases.value.length === 0) return
  
  try {
    const caseIds = selectedCases.value.map(item => item.id)
    await addCasesToTestPlan(testPlanForm.id, { case_ids: caseIds })
    ElMessage.success('添加成功')
    addCasesDialogVisible.value = false
    
    // 重新加载测试用例
    loadTestCases(testPlanForm.id)
  } catch (error) {
    console.error('添加测试用例失败:', error)
    ElMessage.error('添加测试用例失败')
  }
}

/**
 * 处理移除测试用例
 */
const handleRemoveTestCase = (row) => {
  ElMessageBox.confirm(
    '确定要从测试计划中移除该测试用例吗？',
    '警告',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    }
  ).then(async () => {
    try {
      await removeCaseFromTestPlan(testPlanForm.id, row.case_detail.id)
      ElMessage.success('移除成功')
      
      // 重新加载测试用例
      loadTestCases(testPlanForm.id)
    } catch (error) {
      console.error('移除测试用例失败:', error)
      ElMessage.error('移除测试用例失败')
    }
  }).catch(() => {
    // 取消移除
  })
}

/**
 * 获取状态类型
 */
const getStatusType = (status) => {
  const statusMap = {
    draft: 'info',
    ready: 'warning',
    in_progress: 'primary',
    completed: 'success',
    archived: 'danger'
  }
  return statusMap[status] || 'info'
}

/**
 * 获取状态文本
 */
const getStatusText = (status) => {
  const statusMap = {
    draft: '草稿',
    ready: '就绪',
    in_progress: '进行中',
    completed: '已完成',
    archived: '已归档'
  }
  return statusMap[status] || status
}

/**
 * 获取优先级类型
 */
const getPriorityType = (priority) => {
  const priorityMap = {
    P0: 'danger',
    P1: 'warning',
    P2: 'success',
    P3: 'info'
  }
  return priorityMap[priority] || 'info'
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
 * 格式化日期
 */
const formatDate = (dateString) => {
  if (!dateString) return ''
  const date = new Date(dateString)
  return date.toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  })
}
</script>

<style scoped>
.testplan-list-container {
  /* 移除原有的padding，使用fullscreen-container的padding */
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.search-bar {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-bottom: 20px;
  background-color: #f5f7fa;
  padding: 15px;
  border-radius: 4px;
}

.search-bar .el-input {
  width: 300px;
}

.pagination-container {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}

/* 确保表单项内容宽度一致 */
:deep(.el-form-item__content) {
  width: calc(100% - 100px); /* 100px是label的宽度 */
  box-sizing: border-box;
}

/* 确保输入框和选择框宽度一致 */
:deep(.el-input),
:deep(.el-select) {
  width: 100%;
}

/* 确保日期选择器宽度一致 */
:deep(.el-date-editor.el-input__wrapper) {
  width: 100%;
  max-width: 100%;
}

.test-cases-section {
  border: 1px solid #e4e7ed;
  border-radius: 8px;
  padding: 16px;
  background-color: #f9fafc;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.05);
  transition: all 0.3s ease;
  width: 100%;
  box-sizing: border-box;
}

.test-cases-section:hover {
  box-shadow: 0 4px 16px 0 rgba(0, 0, 0, 0.1);
}

.test-cases-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
  padding-bottom: 12px;
  border-bottom: 1px solid #ebeef5;
}

.test-cases-header span {
  font-size: 16px;
  font-weight: 600;
  color: #303133;
  display: flex;
  align-items: center;
}

.test-cases-header span::before {
  content: '';
  display: inline-block;
  width: 4px;
  height: 16px;
  background-color: #409EFF;
  margin-right: 8px;
  border-radius: 2px;
}

.test-cases-table {
  margin-top: 8px;
  width: 100%;
}

.no-data {
  text-align: center;
  color: #909399;
  padding: 30px 0;
  background-color: #fff;
  border-radius: 4px;
  border: 1px dashed #e0e0e0;
  margin-top: 8px;
}

/* 确保对话框内的表单项布局一致 */
:deep(.el-dialog__body) {
  padding: 20px 30px;
}

:deep(.el-form) {
  width: 100%;
}
</style> 