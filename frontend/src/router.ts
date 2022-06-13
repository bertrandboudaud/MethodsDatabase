import Vue from 'vue'
import Router from 'vue-router'
import Home from './views/Home.vue'
import Users from './views/Users.vue'
import Instruments from './views/Instruments.vue'
import Compounds from './views/Compounds.vue'
import Eluents from './views/Eluents.vue'
import Columns from './views/Columns.vue'
import Methods from './views/Methods.vue'

Vue.use(Router)

export default new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/',
      name: 'home',
      component: Home,
    },
    {
      path: '/users',
      name: 'users',
      component: Users,
    },
    {
      path: '/instruments',
      name: 'instruments',
      component: Instruments,
    },
    {
      path: '/compounds',
      name: 'compounds',
      component: Compounds,
    },
    {
      path: '/methods',
      name: 'methods',
      component: Methods,
    },
    {
      path: '/eluents',
      name: 'eluents',
      component: Eluents,
    },
    {
      path: '/columns',
      name: 'columns',
      component: Columns,
    },
  ],
})
