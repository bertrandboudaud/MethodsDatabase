import Vue from 'vue'
import App from './App.vue'
import router from './router'
import vSelect from 'vue-select'
import './registerServiceWorker'
import VueGoodTablePlugin from 'vue-good-table'

import BootstrapVue from 'bootstrap-vue'
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'
import 'vue-select/dist/vue-select.css'
import 'vue-good-table/dist/vue-good-table.css'

import Item from '@/components/Item.vue' 

Vue.use(BootstrapVue)
Vue.component('v-select', vSelect);
Vue.use(VueGoodTablePlugin);

Vue.component('Item', Item);

Vue.config.productionTip = false

new Vue({
  router,
  render: (h) => h(App),
}).$mount('#app')
