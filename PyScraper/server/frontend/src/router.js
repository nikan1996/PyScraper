import Vue from 'vue'
import VueRouter from 'vue-router'
import Index from './components/index.vue'
import Project from './components/projects.vue'
import Databases from './components/databases.vue'
import New_project from './components/project/new_project.vue'

Vue.use(VueRouter);


// 定义路由
const routes = [
    {
        path: '/index',
        component: Index,
        props: {
            msg: 'index'
        },
        meta: {
            title: '首页'
        }
    },
    {
        path: '/projects',
        component: Project,
        props: {
            msg: 'project'
        },
        meta: {
            title: '项目管理'
        }
    },
    {
        path: '/databases',
        component: Databases
    },
    {
        path: '/new_project',
        component: New_project
    }
];

// 创建 router 实例，然后传 `routes` 配置
const router = new VueRouter({
    mode: "history",
    routes
});


export {router}