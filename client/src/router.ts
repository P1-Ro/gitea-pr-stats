import Vue from 'vue';
import Router from 'vue-router';
import Login from '@/views/Login.vue';
import NeedLogin from '@/views/NeedLogin.vue';
import Report from '@/views/Report.vue';


Vue.use(Router);

const router = new Router({
  mode: 'hash',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/',
      name: 'home',
      redirect: 'report',
    },
    {
      path: '/report',
      name: 'report',
      component: Report,
      meta: {
        requiresAuth: true,
      },
    },
    {
      path: '/login',
      name: 'login',
      component: Login,
    },
    {
      path: '/need-login',
      name: 'need-login',
      component: NeedLogin,
    },
  ],
});

export default router;
