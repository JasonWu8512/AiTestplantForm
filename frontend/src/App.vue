<template>
  <router-view />
</template>

<script setup>
import { onMounted } from 'vue'

// App.vue 是应用的根组件

// 设置默认页面标题
onMounted(() => {
  document.title = '测试平台 - AiTestPlantForm'
})
</script>

<style>
:root {
  /* 主色调 */
  --primary-color: #2563eb;
  --primary-light: #3b82f6;
  --primary-dark: #1d4ed8;
  
  /* 辅助色 */
  --success-color: #10b981;
  --warning-color: #f59e0b;
  --danger-color: #ef4444;
  --info-color: #6366f1;
  
  /* 中性色 */
  --text-primary: #1e293b;
  --text-secondary: #64748b;
  --text-disabled: #94a3b8;
  --border-color: #e2e8f0;
  --background-light: #f8fafc;
  --background-dark: #f1f5f9;
  --card-background: #ffffff;
  
  /* 阴影 */
  --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
  --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
  --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
  
  /* 圆角 */
  --border-radius-sm: 4px;
  --border-radius-md: 6px;
  --border-radius-lg: 8px;
  --border-radius-xl: 12px;
  
  /* 间距 */
  --spacing-xs: 4px;
  --spacing-sm: 8px;
  --spacing-md: 16px;
  --spacing-lg: 24px;
  --spacing-xl: 32px;
  
  /* 字体 */
  --font-family: 'PingFang SC', 'Microsoft YaHei', sans-serif;
  --font-size-xs: 12px;
  --font-size-sm: 14px;
  --font-size-md: 16px;
  --font-size-lg: 18px;
  --font-size-xl: 20px;
  --font-size-xxl: 24px;
  
  /* 过渡 */
  --transition-fast: 0.15s ease-in-out;
  --transition-normal: 0.25s ease-in-out;
  --transition-slow: 0.35s ease-in-out;
}

/* 全局样式重置 */
* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

body {
  font-family: var(--font-family);
  font-size: var(--font-size-md);
  color: var(--text-primary);
  background-color: var(--background-light);
  line-height: 1.5;
}

/* Element Plus 主题覆盖 */
:deep(.el-button--primary) {
  --el-button-bg-color: var(--primary-color);
  --el-button-border-color: var(--primary-color);
  --el-button-hover-bg-color: var(--primary-light);
  --el-button-hover-border-color: var(--primary-light);
  --el-button-active-bg-color: var(--primary-dark);
  --el-button-active-border-color: var(--primary-dark);
}

:deep(.el-button--success) {
  --el-button-bg-color: var(--success-color);
  --el-button-border-color: var(--success-color);
}

:deep(.el-button--warning) {
  --el-button-bg-color: var(--warning-color);
  --el-button-border-color: var(--warning-color);
}

:deep(.el-button--danger) {
  --el-button-bg-color: var(--danger-color);
  --el-button-border-color: var(--danger-color);
}

:deep(.el-button--info) {
  --el-button-bg-color: var(--info-color);
  --el-button-border-color: var(--info-color);
}

/* 通用卡片样式 */
.app-card {
  background-color: var(--card-background);
  border-radius: var(--border-radius-lg);
  box-shadow: var(--shadow-sm);
  padding: var(--spacing-lg);
  margin-bottom: var(--spacing-lg);
  transition: box-shadow var(--transition-normal);
}

.app-card:hover {
  box-shadow: var(--shadow-md);
}

/* 通用页面容器 */
.page-container {
  padding: var(--spacing-lg);
  max-width: 1400px;
  margin: 0 auto;
}

/* 通用页面标题 */
.page-title {
  font-size: var(--font-size-xxl);
  font-weight: 600;
  margin-bottom: var(--spacing-lg);
  color: var(--text-primary);
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

/* 通用表格样式增强 */
:deep(.el-table) {
  border-radius: var(--border-radius-md);
  overflow: hidden;
  box-shadow: var(--shadow-sm);
}

:deep(.el-table th) {
  background-color: var(--background-dark) !important;
  font-weight: 600;
}

:deep(.el-table--striped .el-table__body tr.el-table__row--striped td) {
  background-color: var(--background-light);
}

:deep(.el-table__row:hover > td) {
  background-color: rgba(37, 99, 235, 0.05) !important;
}

/* 通用表单样式增强 */
:deep(.el-form-item__label) {
  font-weight: 500;
}

:deep(.el-input__wrapper),
:deep(.el-textarea__wrapper) {
  box-shadow: 0 0 0 1px var(--border-color) inset;
  border-radius: var(--border-radius-md);
  transition: box-shadow var(--transition-fast);
}

:deep(.el-input__wrapper:hover),
:deep(.el-textarea__wrapper:hover) {
  box-shadow: 0 0 0 1px var(--primary-light) inset;
}

:deep(.el-input__wrapper.is-focus),
:deep(.el-textarea__wrapper.is-focus) {
  box-shadow: 0 0 0 2px var(--primary-light) inset !important;
}

/* 通用按钮样式增强 */
:deep(.el-button) {
  border-radius: var(--border-radius-md);
  font-weight: 500;
  transition: all var(--transition-fast);
}

:deep(.el-button:not(.is-text)) {
  box-shadow: var(--shadow-sm);
}

:deep(.el-button:not(.is-text):hover) {
  transform: translateY(-1px);
  box-shadow: var(--shadow-md);
}

:deep(.el-button:not(.is-text):active) {
  transform: translateY(0);
}

/* 通用分页样式增强 */
:deep(.el-pagination) {
  justify-content: flex-end;
  margin-top: var(--spacing-lg);
}

:deep(.el-pagination .el-pagination__jump) {
  margin-left: var(--spacing-md);
}

/* 通用对话框样式增强 */
:deep(.el-dialog) {
  border-radius: var(--border-radius-lg);
  box-shadow: var(--shadow-lg);
  overflow: hidden;
}

:deep(.el-dialog__header) {
  padding: var(--spacing-lg);
  margin-right: 0;
  border-bottom: 1px solid var(--border-color);
}

:deep(.el-dialog__title) {
  font-weight: 600;
  font-size: var(--font-size-lg);
}

:deep(.el-dialog__body) {
  padding: var(--spacing-lg);
}

:deep(.el-dialog__footer) {
  padding: var(--spacing-md) var(--spacing-lg);
  border-top: 1px solid var(--border-color);
}

/* 通用标签样式增强 */
:deep(.el-tag) {
  border-radius: var(--border-radius-sm);
  font-weight: 500;
}

/* 通用下拉菜单样式增强 */
:deep(.el-dropdown-menu) {
  border-radius: var(--border-radius-md);
  box-shadow: var(--shadow-md);
}

:deep(.el-dropdown-menu__item) {
  padding: var(--spacing-sm) var(--spacing-md);
}

/* 通用加载样式增强 */
:deep(.el-loading-mask) {
  background-color: rgba(255, 255, 255, 0.8);
  backdrop-filter: blur(2px);
}

/* 通用消息提示样式增强 */
:deep(.el-message) {
  border-radius: var(--border-radius-lg);
  box-shadow: var(--shadow-md);
  padding: var(--spacing-sm) var(--spacing-md);
}

/* 通用抽屉样式增强 */
:deep(.el-drawer) {
  box-shadow: var(--shadow-lg);
}

:deep(.el-drawer__header) {
  padding: var(--spacing-lg);
  margin-bottom: 0;
  border-bottom: 1px solid var(--border-color);
}

:deep(.el-drawer__body) {
  padding: var(--spacing-lg);
}

/* 通用动画 */
.fade-enter-active,
.fade-leave-active {
  transition: opacity var(--transition-normal);
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

.slide-up-enter-active,
.slide-up-leave-active {
  transition: transform var(--transition-normal), opacity var(--transition-normal);
}

.slide-up-enter-from,
.slide-up-leave-to {
  transform: translateY(20px);
  opacity: 0;
}
</style> 