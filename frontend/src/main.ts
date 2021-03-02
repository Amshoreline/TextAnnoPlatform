import Vue from 'vue'
import App from './App.vue'
import store from './store'
// import './plugins/ant-design-vue.js' 报错

import ViewUI from 'view-design'
import 'view-design/dist/styles/iview.css'
import router from './router'

import jsPlumb from 'jsplumb'

Vue.prototype.$jsPlumb = jsPlumb.jsPlumb
Vue.config.productionTip = false

Vue.use(ViewUI)
Vue.use(require('vue-shortkey'))


new Vue({
    store,
    router,
    render: (h) => h(App),
}).$mount('#app')
