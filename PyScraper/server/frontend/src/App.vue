<template>
    <div id="app">
        <el-container id="elcontainer1">
            <el-aside width="200px">
                <el-menu id="elmenu1"
                         :default-active="current_active"
                         class="el-menu-vertical-demo"
                         background-color="#545c64"
                         text-color="#fff"
                         align="left"
                         active-text-color="#ffd04b"
                         router>
                    <el-menu-item index="1" route="/index">
                        <i class="el-icon-menu"></i>
                        <span slot="title">首页</span>
                    </el-menu-item>
                    <el-menu-item index="2" route="/projects">
                        <i class="el-icon-document"></i>
                        <span slot="title">项目管理</span>
                    </el-menu-item>
                    <el-menu-item index="3" route="/databases">
                        <i class="el-icon-setting"></i>
                        <span slot="title">数据库管理</span>
                    </el-menu-item>
                </el-menu>
            </el-aside>
            <el-container id="elcontainer2">

                <router-view></router-view>
            <el-footer height="20px">PyScraper Copyright ©nikan 859905874@qq.com</el-footer>
            </el-container>


        </el-container>
    </div>
</template>

<script>
    export default {
        name: 'app',
        components: {},
        computed: {
            current_active: function () {
                let current_route_path = this.$router.history.current.fullPath;
                let routes_dict = {"/index": "1", "projects": "2", "/databases": "3"};
                return routes_dict[current_route_path]
            }
        }
    }
</script>

<style>

    .el-header {
        background-color: #fff;
        color: #333;
        text-align: center;

        padding-top: 20px;
    }

    .el-footer {
        background-color: #42b983;
        color: #fff;
        text-align: center;
        font-size: 12px;
        line-height: 1.5;
        height: 20px;
        position: absolute;
        bottom: 0;
        left: 200px;
        right: 0px;
    }

    .el-aside {
        background-color: #D3DCE6;
        color: #333;
        text-align: center;
        line-height: 200px;
    }

    .el-main {
        background-color: #E9EEF3;
        color: #333;
        text-align: center;
        line-height: 160px;
        align-items: flex-end;

    }

    #elcontainer1 {
        height: 100%;
    }

    #elcontainer2 {
    }

    #elmenu1 {
        height: 100%;
    }


    /*.el-container{*/
    /*display: ;*/
    /*}*/

    #app {
        font-family: "Helvetica Neue", Helvetica, "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", "微软雅黑", Arial, sans-serif;
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
        /*text-align: center;*/
        /*height: 700px;*/
        color: #2c3e50;
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        /*margin-top: 60px;*/
    }
</style>