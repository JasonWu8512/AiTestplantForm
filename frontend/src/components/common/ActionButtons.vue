<template>
  <div class="action-buttons" :class="{ 'is-more-mode': isMoreMode }">
    <!-- 主要按钮 -->
    <template v-if="!isMoreMode">
      <template v-for="(button, index) in visibleButtons" :key="index">
        <el-button
          :type="button.type || 'primary'"
          :size="size"
          :icon="button.icon"
          :disabled="button.disabled"
          :loading="button.loading"
          @click.stop="handleButtonClick(button, $event)"
          v-if="!button.hidden"
          :class="['action-button', button.class]"
        >
          {{ button.text }}
        </el-button>
      </template>
    </template>
    
    <!-- 更多按钮下拉菜单 -->
    <el-dropdown v-if="moreButtons.length > 0" trigger="click" @command="handleCommand">
      <el-button :size="size" type="primary" plain class="more-button">
        {{ moreText }}
        <el-icon class="el-icon--right">
          <arrow-down />
        </el-icon>
      </el-button>
      <template #dropdown>
        <el-dropdown-menu>
          <template v-if="isMoreMode">
            <template v-for="(button, index) in visibleButtons" :key="index">
              <el-dropdown-item
                :disabled="button.disabled"
                :command="button.key"
                :class="button.class"
                v-if="!button.hidden"
              >
                <el-icon v-if="button.icon">
                  <component :is="button.icon"></component>
                </el-icon>
                <span class="dropdown-item-text">{{ button.text }}</span>
              </el-dropdown-item>
            </template>
          </template>
          <template v-for="(button, index) in moreButtons" :key="index">
            <el-dropdown-item
              :disabled="button.disabled"
              :command="button.key"
              :class="button.class"
              v-if="!button.hidden"
            >
              <el-icon v-if="button.icon">
                <component :is="button.icon"></component>
              </el-icon>
              <span class="dropdown-item-text">{{ button.text }}</span>
            </el-dropdown-item>
          </template>
        </el-dropdown-menu>
      </template>
    </el-dropdown>
  </div>
</template>

<script setup>
import { computed, ref, watch } from 'vue'
import { ArrowDown } from '@element-plus/icons-vue'

const props = defineProps({
  buttons: {
    type: Array,
    required: true
  },
  size: {
    type: String,
    default: 'small'
  },
  maxVisible: {
    type: Number,
    default: 3
  },
  moreText: {
    type: String,
    default: '更多'
  },
  moreMode: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['click'])

// 是否使用更多模式（所有按钮都放在下拉菜单中）
const isMoreMode = computed(() => {
  return props.moreMode || props.buttons.length > props.maxVisible + 1
})

// 可见按钮
const visibleButtons = computed(() => {
  if (isMoreMode.value) {
    return props.buttons
  } else {
    return props.buttons.slice(0, props.maxVisible)
  }
})

// 更多按钮
const moreButtons = computed(() => {
  if (isMoreMode.value) {
    return []
  } else {
    return props.buttons.slice(props.maxVisible)
  }
})

// 处理按钮点击
const handleButtonClick = (button, event) => {
  if (button.disabled) return
  
  emit('click', button.key, button, event)
  
  if (button.onClick) {
    button.onClick(event)
  }
}

// 处理下拉菜单命令
const handleCommand = (command) => {
  const button = props.buttons.find(btn => btn.key === command)
  if (button) {
    emit('click', button.key, button)
    
    if (button.onClick) {
      button.onClick()
    }
  }
}
</script>

<style scoped>
.action-buttons {
  display: flex;
  gap: 8px;
  flex-wrap: nowrap;
  justify-content: center;
  min-width: 150px;
}

.action-button {
  white-space: nowrap;
  margin: 0 3px;
  min-width: 60px;
}

.is-more-mode {
  justify-content: flex-start;
}

.more-button {
  font-weight: 500;
  color: var(--el-color-primary);
  min-width: 80px;
}

.dropdown-item-text {
  color: var(--el-text-color-primary) !important;
  font-weight: normal;
}

:deep(.el-dropdown-menu__item) {
  display: flex;
  align-items: center;
  gap: 5px;
  padding: 10px 16px;
  min-width: 120px;
  line-height: 1.5;
}

:deep(.el-dropdown-menu__item .el-icon) {
  margin-right: 8px;
}

:deep(.el-dropdown-menu__item span) {
  color: var(--el-text-color-primary);
  font-size: var(--el-font-size-base);
}
</style> 