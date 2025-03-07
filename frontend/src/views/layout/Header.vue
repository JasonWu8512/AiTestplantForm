<template>
  <div class="header-container">
    <div class="left-menu">
      <h2 class="logo">AiTestPlantForm</h2>
    </div>
    <div class="right-menu">
      <el-dropdown trigger="click" @command="handleCommand">
        <div class="avatar-wrapper">
          <el-avatar :size="32" :src="userAvatar">{{ userInitials }}</el-avatar>
          <span class="user-name">{{ userName }}</span>
          <el-icon><arrow-down /></el-icon>
        </div>
        <template #dropdown>
          <el-dropdown-menu>
            <el-dropdown-item command="profile">个人信息</el-dropdown-item>
            <el-dropdown-item command="logout" divided>退出登录</el-dropdown-item>
          </el-dropdown-menu>
        </template>
      </el-dropdown>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/store/user'
import { ArrowDown } from '@element-plus/icons-vue'

const router = useRouter()
const userStore = useUserStore()

// 用户名
const userName = computed(() => {
  return userStore.user.username || '用户'
})

// 用户头像
const userAvatar = computed(() => {
  return userStore.user.avatar || ''
})

// 用户名首字母（用于没有头像时显示）
const userInitials = computed(() => {
  const username = userStore.user.username || ''
  return username.substring(0, 1).toUpperCase()
})

// 处理下拉菜单命令
const handleCommand = (command) => {
  if (command === 'profile') {
    router.push('/profile')
  } else if (command === 'logout') {
    userStore.logout()
  }
}
</script>

<style scoped>
.header-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 100%;
  padding: 0 20px;
}

.logo {
  margin: 0;
  font-size: 20px;
  color: #409EFF;
}

.right-menu {
  display: flex;
  align-items: center;
}

.avatar-wrapper {
  display: flex;
  align-items: center;
  cursor: pointer;
}

.user-name {
  margin: 0 8px;
  font-size: 14px;
}
</style> 