import Vue from 'vue'
import VueRouter from 'vue-router'
import Index from './components/index.vue'
import Projects from './components/projects.vue'
import Databases from './components/databases.vue'
import New_project from './components/project/new_project.vue'
import New_gov_project from './components/project/new_gov_project.vue'
import Project from './components/project/project_detail.vue'
import Gov_lexicon from './components/gov_lexicon.vue'

Vue.use(VueRouter);


// 定义前端路由
const routes = [
    {
        path: '/',
        redirect: '/index',
    },
    {
        path: '/index',
        component: Index,
    },
    {
        path: '/projects',
        component: Projects,
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
    {
        path: '/gov_lexicon',
        component: Gov_lexicon
    }
];

// 创建 router 实例，然后传 `routes` 配置
const router = new VueRouter({
    mode: "history",
    routes
});


export {router}