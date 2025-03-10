<template>
  <span>{{ displayValue }}</span>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'

const props = defineProps({
  startVal: {
    type: Number,
    default: 0
  },
  endVal: {
    type: Number,
    default: 0
  },
  duration: {
    type: Number,
    default: 2000
  },
  autoplay: {
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
  useEasing: {
    type: Boolean,
    default: true
  },
  easingFn: {
    type: Function,
    default: (t, b, c, d) => {
      return c * (-Math.pow(2, -10 * t / d) + 1) * 1024 / 1023 + b
    }
  }
})

const emit = defineEmits(['callback', 'start', 'end'])

const localStartVal = ref(props.startVal)
const displayValue = ref('')
const formatValue = ref('')
const animatedValue = ref(props.startVal)
const localDuration = ref(props.duration)
const startTime = ref(null)
const timestamp = ref(null)
const remaining = ref(null)
const rAF = ref(null)
const lastValue = ref(props.startVal)

// 格式化数字
const formatNumber = (num) => {
  const isNegative = num < 0
  const absoluteNum = Math.abs(num)
  let result = absoluteNum.toFixed(props.decimals)
  
  // 添加千位分隔符
  if (props.separator) {
    const parts = result.split('.')
    parts[0] = parts[0].replace(/\B(?=(\d{3})+(?!\d))/g, props.separator)
    result = parts.join(props.decimal)
  }
  
  return (isNegative ? '-' : '') + result
}

// 计算动画
const countUp = () => {
  if (!startTime.value) {
    startTime.value = timestamp.value
  }
  
  const progress = timestamp.value - startTime.value
  remaining.value = localDuration.value - progress
  
  // 使用缓动函数
  if (props.useEasing) {
    if (props.endVal > props.startVal) {
      animatedValue.value = props.startVal + props.easingFn(progress, 0, props.endVal - props.startVal, localDuration.value)
    } else {
      animatedValue.value = props.startVal - props.easingFn(progress, 0, props.startVal - props.endVal, localDuration.value)
    }
  } else {
    animatedValue.value = localStartVal.value + (props.endVal - localStartVal.value) * (progress / localDuration.value)
  }
  
  // 确保不超过目标值
  animatedValue.value = props.endVal > props.startVal
    ? Math.min(props.endVal, animatedValue.value)
    : Math.max(props.endVal, animatedValue.value)
  
  // 格式化显示值
  formatValue.value = formatNumber(animatedValue.value)
  displayValue.value = props.prefix + formatValue.value + props.suffix
  
  // 继续动画或结束
  if (progress < localDuration.value) {
    rAF.value = requestAnimationFrame(count)
  } else {
    emit('end')
  }
}

// 动画帧回调
const count = (timestamp) => {
  if (!startTime.value) startTime.value = timestamp
  timestamp.value = timestamp
  countUp()
}

// 开始动画
const start = () => {
  localStartVal.value = props.startVal
  startTime.value = null
  localDuration.value = props.duration
  emit('start')
  rAF.value = requestAnimationFrame(count)
}

// 重置动画
const reset = () => {
  startTime.value = null
  cancelAnimationFrame(rAF.value)
  animatedValue.value = props.startVal
  formatValue.value = formatNumber(props.startVal)
  displayValue.value = props.prefix + formatValue.value + props.suffix
}

// 更新动画
const update = (newEndVal) => {
  cancelAnimationFrame(rAF.value)
  startTime.value = null
  localDuration.value = props.duration
  localStartVal.value = animatedValue.value
  rAF.value = requestAnimationFrame(count)
}

// 监听endVal变化
watch(() => props.endVal, (newVal) => {
  if (lastValue.value !== newVal) {
    lastValue.value = newVal
    if (props.autoplay) {
      reset()
      start()
    }
  }
})

// 组件挂载时自动开始动画
onMounted(() => {
  if (props.autoplay) {
    start()
  }
  
  // 初始化显示值
  formatValue.value = formatNumber(props.startVal)
  displayValue.value = props.prefix + formatValue.value + props.suffix
})

// 暴露方法
defineExpose({
  start,
  reset,
  update
})
</script> 