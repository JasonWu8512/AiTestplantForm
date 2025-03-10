<template>
  <div class="search-panel">
    <div class="search-panel-header" v-if="title">
      <h3 class="search-panel-title">
        <el-icon><Search /></el-icon>
        {{ title }}
      </h3>
      <el-button 
        v-if="showToggle" 
        type="text" 
        @click="toggleExpand"
      >
        {{ isExpanded ? '收起' : '展开' }}
        <el-icon>
          <component :is="isExpanded ? 'ArrowUp' : 'ArrowDown'" />
        </el-icon>
      </el-button>
    </div>
    
    <div class="search-panel-body" :class="{ 'is-expanded': isExpanded }">
      <el-form :inline="true" :model="modelValue" class="search-form">
        <slot></slot>
        
        <div class="search-actions">
          <el-button type="primary" @click="handleSearch">
            <el-icon><Search /></el-icon>
            搜索
          </el-button>
          <el-button @click="handleReset">
            <el-icon><RefreshRight /></el-icon>
            重置
          </el-button>
        </div>
      </el-form>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { Search, RefreshRight, ArrowUp, ArrowDown } from '@element-plus/icons-vue'

const props = defineProps({
  title: {
    type: String,
    default: '搜索条件'
  },
  modelValue: {
    type: Object,
    required: true
  },
  showToggle: {
    type: Boolean,
    default: false
  },
  defaultExpanded: {
    type: Boolean,
    default: true
  }
})

const emit = defineEmits(['search', 'reset', 'update:modelValue'])

const isExpanded = ref(props.defaultExpanded)

const toggleExpand = () => {
  isExpanded.value = !isExpanded.value
}

const handleSearch = () => {
  emit('search')
}

const handleReset = () => {
  emit('reset')
}
</script>

<style scoped>
.search-panel {
  width: 100%;
}

.search-panel-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--spacing-md);
}

.search-panel-title {
  font-size: var(--font-size-md);
  font-weight: 500;
  color: var(--text-primary);
  margin: 0;
  display: flex;
  align-items: center;
  gap: var(--spacing-xs);
}

.search-panel-body {
  transition: max-height var(--transition-normal);
  overflow: hidden;
}

.search-panel-body.is-expanded {
  max-height: 1000px;
}

.search-panel-body:not(.is-expanded) {
  max-height: 60px;
}

.search-form {
  display: flex;
  flex-wrap: wrap;
  gap: var(--spacing-md);
  align-items: flex-end;
}

.search-actions {
  display: flex;
  gap: var(--spacing-sm);
  margin-left: auto;
}

:deep(.el-form-item) {
  margin-bottom: var(--spacing-sm);
  margin-right: 0;
}

:deep(.el-form-item__label) {
  font-weight: 500;
}
</style> 