<template>
  <div class="app-container layout-container">
    <!-- 海洋背景元素 -->
    <div class="ocean-waves">
      <div class="wave" v-for="i in 3" :key="`w-${i}`"></div>
    </div>
    
    <div class="bubbles">
      <div class="bubble" v-for="i in 30" :key="`b-${i}`"></div>
    </div>
    
    <div class="light-rays">
      <div class="ray" v-for="i in 20" :key="`r-${i}`"></div>
    </div>
    
    <el-container>
      <el-aside width="220px" class="sidebar">
        <Sidebar />
      </el-aside>
      <el-container>
        <el-header height="60px" class="header">
          <Header />
        </el-header>
        <el-main class="main-content">
          <router-view />
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<script setup>
import Header from './Header.vue'
import Sidebar from './Sidebar.vue'
</script>

<style scoped>
.app-container {
  height: 100vh;
}

.el-header {
  padding: 0;
  position: relative;
  z-index: 10;
}

.el-aside {
  overflow: hidden;
  position: relative;
  z-index: 10;
}

.el-main {
  padding: 20px;
  overflow-y: auto;
  position: relative;
  z-index: 5;
}
</style> 