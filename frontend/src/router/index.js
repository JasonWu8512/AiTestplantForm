import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '@/store/user'

// 路由配置
const routes = [
  {
    path: '/',
    component: () => import('@/views/layout/Layout.vue'),
    redirect: '/dashboard',
    meta: { requiresAuth: true },
    children: [
      {
        path: 'dashboard',
        name: 'Dashboard',
        component: () => import('@/views/dashboard/Dashboard.vue'),
        meta: { title: '仪表盘', icon: 'el-icon-s-home' }
      },
      {
        path: 'projects',
        name: 'ProjectList',
        component: () => import('@/views/testcases/ProjectList.vue'),
        meta: { title: '项目管理', icon: 'el-icon-folder' }
      },
      {
        path: 'testcases',
        name: 'TestCaseList',
        component: () => import('@/views/testcases/TestCaseList.vue'),
        meta: { title: '测试用例管理', icon: 'el-icon-document' }
      },
      {
        path: 'testcases/:id',
        name: 'TestCaseDetail',
        component: () => import('@/views/testcases/TestCaseDetail.vue'),
        meta: { title: '测试用例详情', icon: 'document' }
      },
      {
        path: 'testplans',
        name: 'TestPlanList',
        component: () => import('@/views/testplans/TestPlanList.vue'),
        meta: { title: '测试计划管理', icon: 'el-icon-date' }
      },
      {
        path: 'testplans/:id',
        name: 'TestPlanDetail',
        component: () => import('@/views/testplans/TestPlanDetail.vue'),
        meta: { title: '测试计划详情', icon: 'document' }
      },
      {
        path: 'users',
        name: 'Users',
        component: () => import('@/views/users/UserList.vue'),
        meta: { title: '用户管理', icon: 'el-icon-user' }
      },
      {
        path: 'profile',
        name: 'Profile',
        component: () => import('@/views/users/UserProfile.vue'),
        meta: { title: '个人信息', hidden: true }
      },
      {
        path: 'executions',
        name: 'ExecutionList',
        component: () => import('@/views/executions/ExecutionList.vue'),
        meta: { title: '测试执行管理', icon: 'video-play' }
      },
      {
        path: 'executions/:id',
        name: 'ExecutionDetail',
        component: () => import('@/views/executions/ExecutionDetail.vue'),
        meta: { title: '测试执行详情', icon: 'document' }
      }
    ]
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/users/Login.vue'),
    meta: { title: '登录' }
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('@/views/users/Register.vue'),
    meta: { title: '注册' }
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: () => import('@/views/NotFound.vue'),
    meta: { title: '404' }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 全局前置守卫
router.beforeEach((to, from, next) => {
  // 设置页面标题
  document.title = to.meta.title ? `${to.meta.title} - AiTestPlantForm` : 'AiTestPlantForm'
  
  console.log('路由导航:', from.path, '->', to.path)
  
  const userStore = useUserStore()
  const isLoggedIn = userStore.isLoggedIn
  
  console.log('用户登录状态:', isLoggedIn)
  
  // 检查是否需要登录
  if (to.matched.some(record => record.meta.requiresAuth)) {
    console.log('该路由需要认证')
    // 检查用户是否已登录
    if (!isLoggedIn) {
      console.log('用户未登录，重定向到登录页')
      // 未登录则重定向到登录页
      next({
        path: '/login',
        query: { redirect: to.fullPath }
      })
    } else {
      console.log('用户已登录，允许访问')
      next()
    }
  } else {
    // 如果用户已登录且尝试访问登录或注册页面，重定向到首页
    if (isLoggedIn && (to.path === '/login' || to.path === '/register')) {
      console.log('用户已登录，尝试访问登录/注册页，重定向到首页')
      next('/')
    } else {
      console.log('允许访问非认证路由')
      next()
    }
  }
})

export default router 