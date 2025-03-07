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
body {
  margin: 0;
  padding: 0;
  font-family: 'Helvetica Neue', Helvetica, 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', '微软雅黑', Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

#app {
  height: 100vh;
}
</style> 