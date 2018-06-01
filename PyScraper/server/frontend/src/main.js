import Vue from 'vue';
import App from './App.vue';
// import axios from 'axios';

import {router} from './router.js';

import ElementUI from 'element-ui';
import 'element-ui/lib/theme-chalk/index.css';

Vue.use(ElementUI);
// Vue.prototype.axios = axios;
Vue.config.productionTip = false;
new Vue({
    router,
    render: h => h(App)
}).$mount('#app');
