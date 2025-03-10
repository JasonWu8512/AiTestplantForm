<template>
  <div class="data-table-wrapper">
    <!-- 表格工具栏 -->
    <div class="table-toolbar" v-if="$slots.toolbar || showRefresh || showSettings">
      <div class="toolbar-left">
        <slot name="toolbar"></slot>
      </div>
      <div class="toolbar-right">
        <el-tooltip content="刷新数据" v-if="showRefresh">
          <el-button 
            type="primary" 
            :icon="Refresh" 
            circle 
            plain
            :loading="loading"
            @click="$emit('refresh')"
          ></el-button>
        </el-tooltip>
        <el-tooltip content="表格设置" v-if="showSettings">
          <el-dropdown trigger="click" @command="handleCommand">
            <el-button type="primary" :icon="Setting" circle plain></el-button>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item command="density">
                  <span>表格密度</span>
                  <div class="dropdown-item-right">
                    <el-radio-group v-model="tableDensity" size="small">
                      <el-radio-button label="default">默认</el-radio-button>
                      <el-radio-button label="medium">中等</el-radio-button>
                      <el-radio-button label="small">紧凑</el-radio-button>
                    </el-radio-group>
                  </div>
                </el-dropdown-item>
                <el-dropdown-item command="stripe">
                  <span>斑马纹</span>
                  <div class="dropdown-item-right">
                    <el-switch v-model="tableStripe" />
                  </div>
                </el-dropdown-item>
                <el-dropdown-item command="border">
                  <span>表格边框</span>
                  <div class="dropdown-item-right">
                    <el-switch v-model="tableBorder" />
                  </div>
                </el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </el-tooltip>
      </div>
    </div>
    
    <!-- 数据表格 -->
    <el-table
      ref="tableRef"
      v-loading="loading"
      :data="data"
      :border="tableBorder"
      :stripe="tableStripe"
      :size="tableDensity"
      :height="height"
      :max-height="maxHeight"
      :row-key="rowKey"
      :row-class-name="rowClassName"
      @row-click="handleRowClick"
      @selection-change="handleSelectionChange"
      class="data-table"
    >
      <el-table-column
        v-if="showSelection"
        type="selection"
        width="50"
        align="center"
        fixed="left"
      ></el-table-column>
      <el-table-column
        v-if="showIndex"
        type="index"
        width="60"
        label="序号"
        align="center"
      ></el-table-column>
      
      <!-- 表格列 -->
      <slot></slot>
      
      <!-- 操作列 -->
      <el-table-column
        v-if="$slots.actions"
        :label="actionsLabel"
        :width="actionsWidth"
        :fixed="actionsFixed"
        align="center"
      >
        <template #default="scope">
          <div class="table-actions">
            <slot name="actions" :row="scope.row" :index="scope.$index"></slot>
          </div>
        </template>
      </el-table-column>
    </el-table>
    
    <!-- 分页 -->
    <div class="pagination-wrapper" v-if="showPagination">
      <el-pagination
        :current-page="currentPage"
        :page-size="pageSize"
        :page-sizes="pageSizes"
        :layout="paginationLayout"
        :total="total"
        @update:current-page="handleCurrentChange"
        @update:page-size="handleSizeChange"
      ></el-pagination>
    </div>
    
    <!-- 空数据提示 -->
    <el-empty
      v-if="data && data.length === 0 && !loading"
      description="暂无数据"
    ></el-empty>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { Refresh, Setting } from '@element-plus/icons-vue'

const props = defineProps({
  data: {
    type: Array,
    required: true
  },
  loading: {
    type: Boolean,
    default: false
  },
  rowKey: {
    type: String,
    default: 'id'
  },
  height: {
    type: [String, Number],
    default: null
  },
  maxHeight: {
    type: [String, Number],
    default: null
  },
  showSelection: {
    type: Boolean,
    default: false
  },
  showIndex: {
    type: Boolean,
    default: false
  },
  showPagination: {
    type: Boolean,
    default: true
  },
  showRefresh: {
    type: Boolean,
    default: true
  },
  showSettings: {
    type: Boolean,
    default: true
  },
  currentPage: {
    type: Number,
    default: 1
  },
  pageSize: {
    type: Number,
    default: 10
  },
  pageSizes: {
    type: Array,
    default: () => [10, 20, 50, 100]
  },
  total: {
    type: Number,
    default: 0
  },
  paginationLayout: {
    type: String,
    default: 'total, sizes, prev, pager, next, jumper'
  },
  actionsLabel: {
    type: String,
    default: '操作'
  },
  actionsWidth: {
    type: [String, Number],
    default: 'auto'
  },
  actionsFixed: {
    type: String,
    default: 'right'
  },
  rowClassName: {
    type: Function,
    default: () => ''
  }
})

const emit = defineEmits([
  'refresh',
  'row-click',
  'selection-change',
  'update:currentPage',
  'update:pageSize',
  'page-change',
  'size-change'
])

const tableRef = ref(null)

// 表格设置
const tableDensity = ref('default')
const tableStripe = ref(true)
const tableBorder = ref(true)

// 处理表格设置命令
const handleCommand = (command) => {
  console.log('表格设置命令:', command)
}

// 处理行点击
const handleRowClick = (row, column, event) => {
  emit('row-click', row, column, event)
}

// 处理选择变化
const handleSelectionChange = (selection) => {
  emit('selection-change', selection)
}

// 处理分页大小变化
const handleSizeChange = (size) => {
  emit('update:pageSize', size)
  emit('size-change', size)
}

// 处理当前页变化
const handleCurrentChange = (page) => {
  emit('update:currentPage', page)
  emit('page-change', page)
}

// 暴露方法
defineExpose({
  // 获取表格实例
  getTable: () => tableRef.value,
  // 清除选择
  clearSelection: () => {
    if (tableRef.value) {
      tableRef.value.clearSelection()
    }
  },
  // 切换行选择
  toggleRowSelection: (row, selected) => {
    if (tableRef.value) {
      tableRef.value.toggleRowSelection(row, selected)
    }
  },
  // 切换所有行选择
  toggleAllSelection: () => {
    if (tableRef.value) {
      tableRef.value.toggleAllSelection()
    }
  }
})
</script>

<style scoped>
.data-table-wrapper {
  width: 100%;
}

.table-toolbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: var(--spacing-md);
  border-bottom: 1px solid var(--border-color);
}

.toolbar-left {
  display: flex;
  gap: var(--spacing-sm);
  align-items: center;
}

.toolbar-right {
  display: flex;
  gap: var(--spacing-sm);
  align-items: center;
}

.data-table {
  width: 100%;
}

.table-actions {
  display: flex;
  justify-content: center;
  gap: var(--spacing-xs);
  flex-wrap: wrap;
}

.pagination-wrapper {
  padding: var(--spacing-md);
  display: flex;
  justify-content: flex-end;
  border-top: 1px solid var(--border-color);
}

.dropdown-item-right {
  margin-left: var(--spacing-md);
  display: inline-flex;
  align-items: center;
}

:deep(.el-dropdown-menu__item) {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: var(--spacing-sm) var(--spacing-md);
}
</style> 