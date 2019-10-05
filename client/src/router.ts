import Vue from 'vue';
import Router from 'vue-router';
import Home from '@/views/Home.vue';
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
      redirect: 'report'
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

/*
router.beforeEach((to, from, next) => {
  if (to.matched.some(record => record.meta.requiresAuth)) {
    const loggedIn = sessionStorage.getItem('isLoggedIn');
    if (loggedIn) {
      next();
    } else {
      next({
        path: '/need-login',
        params: { nextUrl: to.fullPath },
      });
    }
  } else {
    next();
  }
});
*/

export default router;
