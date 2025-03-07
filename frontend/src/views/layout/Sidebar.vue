<template>
  <div class="sidebar-container">
    <el-menu
      :default-active="activeMenu"
      background-color="#304156"
      text-color="#bfcbd9"
      active-text-color="#409EFF"
      router
      unique-opened
    >
      <el-menu-item index="/dashboard">
        <el-icon><odometer /></el-icon>
        <span>仪表盘</span>
      </el-menu-item>
      
      <el-menu-item index="/users" v-if="isAdmin">
        <el-icon><user /></el-icon>
        <span>用户管理</span>
      </el-menu-item>
      
      <!-- 其他菜单项将在后续阶段添加 -->
    </el-menu>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import { useUserStore } from '@/store/user'
import { Odometer, User } from '@element-plus/icons-vue'

const route = useRoute()
const userStore = useUserStore()

// 当前激活的菜单
const activeMenu = computed(() => {
  return route.path
})

// 是否为管理员
const isAdmin = computed(() => {
  return userStore.isAdmin
})
</script>

<style scoped>
.sidebar-container {
  height: 100%;
  overflow-y: auto;
}

.el-menu {
  border-right: none;
  height: 100%;
}
</style> 