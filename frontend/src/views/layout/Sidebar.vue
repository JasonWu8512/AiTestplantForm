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
      
      <el-menu-item index="/projects">
        <el-icon><folder /></el-icon>
        <span>项目管理</span>
      </el-menu-item>
      
      <el-menu-item index="/testcases">
        <el-icon><document /></el-icon>
        <span>测试用例管理</span>
      </el-menu-item>
      
      <el-menu-item index="/testplans">
        <el-icon><calendar /></el-icon>
        <span>测试计划管理</span>
      </el-menu-item>
      
      <el-menu-item index="/executions">
        <el-icon><VideoPlay /></el-icon>
        <span>测试执行管理</span>
      </el-menu-item>
      
      <el-menu-item index="/reports">
        <el-icon><Document /></el-icon>
        <span>测试报告管理</span>
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
import { Odometer, User, Folder, Document, Calendar, VideoPlay } from '@element-plus/icons-vue'

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