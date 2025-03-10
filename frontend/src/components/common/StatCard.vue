<template>
  <div class="stat-card" :class="[`stat-card--${type}`]" @click="handleClick">
    <div class="stat-card__icon" v-if="icon">
      <el-icon>
        <component :is="icon"></component>
      </el-icon>
    </div>
    <div class="stat-card__content">
      <div class="stat-card__title">{{ title }}</div>
      <div class="stat-card__value">
        <count-to
          v-if="animation"
          :start-val="0"
          :end-val="Number(value) || 0"
          :duration="2000"
          :decimals="decimals"
          :decimal="decimal"
          :separator="separator"
          :prefix="prefix"
          :suffix="suffix"
        />
        <template v-else>
          {{ formattedValue }}
        </template>
      </div>
      <div class="stat-card__footer" v-if="$slots.footer || footer">
        <slot name="footer">{{ footer }}</slot>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import CountTo from './CountTo.vue'

const props = defineProps({
  title: {
    type: String,
    required: true
  },
  value: {
    type: [Number, String],
    required: true
  },
  icon: {
    type: String,
    default: ''
  },
  type: {
    type: String,
    default: 'primary',
    validator: (value) => ['primary', 'success', 'warning', 'danger', 'info'].includes(value)
  },
  footer: {
    type: String,
    default: ''
  },
  animation: {
    type: Boolean,
    default: true
  },
  decimals: {
    type: Number,
    default: 0
  },
  decimal: {
    type: String,
    default: '.'
  },
  separator: {
    type: String,
    default: ','
  },
  prefix: {
    type: String,
    default: ''
  },
  suffix: {
    type: String,
    default: ''
  },
  clickable: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['click'])

// 格式化值
const formattedValue = computed(() => {
  let val = props.value
  
  if (typeof val === 'number') {
    val = val.toFixed(props.decimals)
    
    // 添加千位分隔符
    if (props.separator) {
      const parts = val.toString().split('.')
      parts[0] = parts[0].replace(/\B(?=(\d{3})+(?!\d))/g, props.separator)
      val = parts.join(props.decimal)
    }
  }
  
  return `${props.prefix}${val}${props.suffix}`
})

// 处理点击事件
const handleClick = () => {
  if (props.clickable) {
    emit('click')
  }
}
</script>

<style scoped>
.stat-card {
  background-color: var(--card-background);
  border-radius: var(--border-radius-lg);
  box-shadow: var(--shadow-sm);
  padding: var(--spacing-lg);
  display: flex;
  align-items: center;
  gap: var(--spacing-lg);
  transition: all var(--transition-normal);
  height: 100%;
  cursor: pointer;
}

.stat-card:hover {
  box-shadow: var(--shadow-md);
  transform: translateY(-2px);
}

.stat-card__icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 60px;
  height: 60px;
  border-radius: 50%;
  font-size: 24px;
  flex-shrink: 0;
}

.stat-card__content {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: var(--spacing-xs);
}

.stat-card__title {
  font-size: var(--font-size-md);
  color: var(--text-secondary);
  font-weight: 500;
}

.stat-card__value {
  font-size: var(--font-size-xxl);
  font-weight: 600;
  line-height: 1.2;
}

.stat-card__footer {
  font-size: var(--font-size-sm);
  color: var(--text-secondary);
  margin-top: var(--spacing-xs);
}

/* 类型样式 */
.stat-card--primary .stat-card__icon {
  background-color: rgba(37, 99, 235, 0.1);
  color: var(--primary-color);
}

.stat-card--primary .stat-card__value {
  color: var(--primary-color);
}

.stat-card--success .stat-card__icon {
  background-color: rgba(16, 185, 129, 0.1);
  color: var(--success-color);
}

.stat-card--success .stat-card__value {
  color: var(--success-color);
}

.stat-card--warning .stat-card__icon {
  background-color: rgba(245, 158, 11, 0.1);
  color: var(--warning-color);
}

.stat-card--warning .stat-card__value {
  color: var(--warning-color);
}

.stat-card--danger .stat-card__icon {
  background-color: rgba(239, 68, 68, 0.1);
  color: var(--danger-color);
}

.stat-card--danger .stat-card__value {
  color: var(--danger-color);
}

.stat-card--info .stat-card__icon {
  background-color: rgba(99, 102, 241, 0.1);
  color: var(--info-color);
}

.stat-card--info .stat-card__value {
  color: var(--info-color);
}
</style> 