<template>
  <div class="detail-panel" :class="{ 'is-editing': isEditing }">
    <!-- 面板头部 -->
    <div class="detail-header">
      <div class="detail-title">
        <slot name="title">
          <h3>{{ title }}</h3>
        </slot>
      </div>
      <div class="detail-actions">
        <slot name="actions">
          <el-button 
            v-if="!isEditing && showEditButton" 
            type="primary" 
            @click="handleEdit"
            :icon="Edit"
            plain
          >
            编辑
          </el-button>
          <template v-if="isEditing">
            <el-button 
              type="primary" 
              @click="handleSave"
              :loading="saveLoading"
              :icon="Check"
            >
              保存
            </el-button>
            <el-button 
              @click="handleCancel"
              :icon="Close"
            >
              取消
            </el-button>
          </template>
        </slot>
      </div>
    </div>
    
    <!-- 面板内容 -->
    <div class="detail-content">
      <el-form
        ref="formRef"
        :model="modelValue"
        :rules="rules"
        :disabled="!isEditing && disableViewMode"
        :label-width="labelWidth"
        :label-position="labelPosition"
        :validate-on-rule-change="false"
      >
        <slot></slot>
      </el-form>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { Edit, Check, Close } from '@element-plus/icons-vue'

const props = defineProps({
  title: {
    type: String,
    default: '详情'
  },
  modelValue: {
    type: Object,
    required: true
  },
  rules: {
    type: Object,
    default: () => ({})
  },
  labelWidth: {
    type: [String, Number],
    default: '120px'
  },
  labelPosition: {
    type: String,
    default: 'right'
  },
  showEditButton: {
    type: Boolean,
    default: true
  },
  disableViewMode: {
    type: Boolean,
    default: true
  },
  saveLoading: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits([
  'update:modelValue',
  'edit',
  'save',
  'cancel',
  'validate'
])

const formRef = ref(null)
const isEditing = ref(false)

// 处理编辑按钮点击
const handleEdit = () => {
  isEditing.value = true
  emit('edit')
}

// 处理保存按钮点击
const handleSave = async () => {
  if (!formRef.value) return
  
  try {
    await formRef.value.validate()
    emit('save')
    emit('validate', true)
  } catch (error) {
    console.error('表单验证失败:', error)
    emit('validate', false)
  }
}

// 处理取消按钮点击
const handleCancel = () => {
  isEditing.value = false
  if (formRef.value) {
    formRef.value.resetFields()
  }
  emit('cancel')
}

// 暴露方法
defineExpose({
  // 获取表单实例
  getForm: () => formRef.value,
  // 设置编辑状态
  setEditing: (value) => {
    isEditing.value = value
  },
  // 验证表单
  validate: async () => {
    if (!formRef.value) return false
    
    try {
      await formRef.value.validate()
      return true
    } catch (error) {
      return false
    }
  },
  // 重置表单
  resetFields: () => {
    if (formRef.value) {
      formRef.value.resetFields()
    }
  }
})
</script>

<style scoped>
.detail-panel {
  background-color: var(--card-background);
  border-radius: var(--border-radius-lg);
  box-shadow: var(--shadow-sm);
  transition: box-shadow var(--transition-normal);
}

.detail-panel:hover {
  box-shadow: var(--shadow-md);
}

.detail-panel.is-editing {
  box-shadow: var(--shadow-md);
  border: 1px solid var(--primary-light);
}

.detail-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: var(--spacing-md) var(--spacing-lg);
  border-bottom: 1px solid var(--border-color);
}

.detail-title h3 {
  font-size: var(--font-size-lg);
  font-weight: 600;
  color: var(--text-primary);
  margin: 0;
}

.detail-actions {
  display: flex;
  gap: var(--spacing-sm);
}

.detail-content {
  padding: var(--spacing-lg);
}

:deep(.el-form-item__label) {
  font-weight: 500;
}

:deep(.el-form-item.is-required .el-form-item__label::before) {
  color: var(--danger-color);
}
</style> 