import Vue from 'vue'
import Router from 'vue-router'
import Home from './views/Home.vue'
import Users from './views/Users.vue'
import InstrumentsList from './views/InstrumentsList.vue'
import CompoundsList from './views/CompoundsList.vue'
import EluentsList from './views/EluentsList.vue'
import ColumnsList from './views/ColumnsList.vue'
import MethodsList from './views/MethodsList.vue'

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
      component: InstrumentsList,
    },
    {
      path: '/compounds',
      name: 'compounds',
      component: CompoundsList,
    },
    {
      path: '/methods',
      name: 'methods',
      component: MethodsList,
    },
    {
      path: '/eluents',
      name: 'eluents',
      component: EluentsList,
    },
    {
      path: '/columns',
      name: 'columns',
      component: ColumnsList,
    },
  ],
})
