<template>
  <div class="status-tag-wrapper">
    <el-tag
      :type="tagType"
      :effect="effect"
      :size="size"
      :class="['status-tag', `status-${status}`]"
    >
      <span v-if="showIcon" class="status-icon">
        <el-icon>
          <component :is="iconName" />
        </el-icon>
      </span>
      <slot>{{ displayText }}</slot>
    </el-tag>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import {
  SuccessFilled,
  WarningFilled,
  CircleCloseFilled,
  InfoFilled,
  Loading,
  Timer,
  VideoPlay,
  VideoPause,
  CircleCheck,
  CircleClose,
  Warning
} from '@element-plus/icons-vue'

const props = defineProps({
  status: {
    type: String,
    required: true
  },
  text: {
    type: String,
    default: ''
  },
  showIcon: {
    type: Boolean,
    default: true
  },
  size: {
    type: String,
    default: 'default'
  },
  effect: {
    type: String,
    default: 'light'
  },
  statusMap: {
    type: Object,
    default: () => ({})
  }
})

// 默认状态映射
const defaultStatusMap = {
  success: { type: 'success', icon: 'SuccessFilled', text: '成功' },
  warning: { type: 'warning', icon: 'WarningFilled', text: '警告' },
  error: { type: 'danger', icon: 'CircleCloseFilled', text: '错误' },
  info: { type: 'info', icon: 'InfoFilled', text: '信息' },
  
  // 通用状态
  active: { type: 'success', icon: 'CircleCheck', text: '活跃' },
  inactive: { type: 'info', icon: 'CircleClose', text: '非活跃' },
  pending: { type: 'warning', icon: 'Timer', text: '待处理' },
  processing: { type: 'primary', icon: 'Loading', text: '处理中' },
  completed: { type: 'success', icon: 'CircleCheck', text: '已完成' },
  failed: { type: 'danger', icon: 'CircleClose', text: '失败' },
  
  // 测试状态
  passed: { type: 'success', icon: 'CircleCheck', text: '通过' },
  failed: { type: 'danger', icon: 'CircleClose', text: '失败' },
  blocked: { type: 'warning', icon: 'Warning', text: '阻塞' },
  skipped: { type: 'info', icon: 'CircleClose', text: '跳过' },
  
  // 执行状态
  running: { type: 'primary', icon: 'VideoPlay', text: '执行中' },
  paused: { type: 'warning', icon: 'VideoPause', text: '已暂停' },
  aborted: { type: 'danger', icon: 'CircleClose', text: '已中止' },
  
  // 项目状态
  draft: { type: 'info', icon: 'InfoFilled', text: '草稿' },
  ready: { type: 'primary', icon: 'CircleCheck', text: '就绪' },
  in_progress: { type: 'primary', icon: 'Loading', text: '进行中' },
  completed: { type: 'success', icon: 'CircleCheck', text: '已完成' },
  archived: { type: 'info', icon: 'CircleClose', text: '已归档' }
}

// 合并状态映射
const mergedStatusMap = computed(() => {
  return { ...defaultStatusMap, ...props.statusMap }
})

// 获取当前状态配置
const statusConfig = computed(() => {
  return mergedStatusMap.value[props.status] || { type: 'info', icon: 'InfoFilled', text: props.status }
})

// 标签类型
const tagType = computed(() => {
  return statusConfig.value.type
})

// 图标名称
const iconName = computed(() => {
  return statusConfig.value.icon
})

// 显示文本
const displayText = computed(() => {
  return props.text || statusConfig.value.text
})
</script>

<style scoped>
.status-tag-wrapper {
  display: inline-flex;
  justify-content: center;
  width: 100%;
}

.status-tag {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 4px;
  padding: 0 10px;
  height: 24px;
  border-radius: 4px;
  font-weight: 500;
  text-align: center;
}

.status-icon {
  display: inline-flex;
  align-items: center;
}

/* 旋转动画 */
.status-running .status-icon,
.status-processing .status-icon,
.status-in_progress .status-icon {
  animation: rotating 2s linear infinite;
}

@keyframes rotating {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}
</style> 