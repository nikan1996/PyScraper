import Vue from 'vue'
import VueRouter from 'vue-router'
import Index from './components/index.vue'
import Project from './components/projects.vue'
import Databases from './components/databases.vue'
import New_project from './components/project/new_project.vue'
import New_gov_project from './components/project/new_gov_project.vue'
Vue.use(VueRouter);


// 定义路由
const routes = [
    {
        path: '/index',
        component: Index,
    },
    {
        path: '/projects',
        component: Project,
    },
    {
        path: '/project/:project_id',
        component: Project,
    },
    {
        path: '/databases',
        component: Databases
    },
    {
        path: '/database/:database_id',
        component: Databases
    },
    {
        path: '/create_project',
        component: New_project
    },
    {
        path: '/create_gov_project',
        component: New_gov_project
    },

];

// 创建 router 实例，然后传 `routes` 配置
const router = new VueRouter({
    mode: "history",
    routes
});


export {router}