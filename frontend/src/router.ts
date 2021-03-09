import Vue from 'vue'
import Router from 'vue-router'
import Test from './components/Test.vue'
import TextList from './components/text/TextList.vue'
import LabelList from './components/label/LabelList.vue'
import Annotation from './components/annotation/Annotation.vue'

Vue.use(Router)

export default new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      name: 'test',
      path: '/',
      component: Test,
      redirect: '/text',
      children: [
        {
          name: 'text',
          path: '/text',
          component: TextList,
        },
        {
          name: 'label',
          path: '/label',
          component: LabelList,
        },
        {
          name: 'ann',
          // path: '/ann/:page/:index/',
          path: '/ann',
          component: Annotation,
        },
      ],
    },
  ],
})
