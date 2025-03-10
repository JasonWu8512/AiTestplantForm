<template>
  <div class="page-layout">
    <!-- 页面头部 -->
    <div class="page-header">
      <div class="page-header-left">
        <h1 class="page-title">{{ title }}</h1>
        <p v-if="description" class="page-description">{{ description }}</p>
      </div>
      <div class="page-header-right">
        <slot name="actions"></slot>
      </div>
    </div>
    
    <!-- 页面内容 -->
    <div class="page-content">
      <!-- 搜索区域 -->
      <div v-if="$slots.search" class="search-section app-card">
        <slot name="search"></slot>
      </div>
      
      <!-- 主要内容区域 -->
      <div class="main-content">
        <slot></slot>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  title: {
    type: String,
    required: true
  },
  description: {
    type: String,
    default: ''
  }
})
</script>

<style scoped>
.page-layout {
  padding: var(--spacing-lg);
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: var(--spacing-xl);
}

.page-header-left {
  max-width: 70%;
}

.page-title {
  font-size: var(--font-size-xxl);
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: var(--spacing-xs);
  position: relative;
  padding-bottom: var(--spacing-sm);
}

.page-title::after {
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

.page-header-right {
  display: flex;
  gap: var(--spacing-sm);
  align-items: center;
}

.search-section {
  margin-bottom: var(--spacing-lg);
}

.main-content {
  background-color: var(--card-background);
  border-radius: var(--border-radius-lg);
  box-shadow: var(--shadow-sm);
  overflow: hidden;
}
</style> 