<template>
    <div id="projects">
        <router-link to="/new_project">
            <el-button type="primary">新建项目</el-button>
        </router-link>
        <el-table :data="project_data" stripe style="width: 100%">
            <el-table-column prop="tag" label="标签" width="180">
            </el-table-column>
            <el-table-column prop="name" label="项目名称" width="180">
            </el-table-column>
            <el-table-column prop="status" label="状态">
            </el-table-column>
            <el-table-column
                    fixed="right"
                    label="操作"
                    width="300">
                <template slot-scope="scope">
                    <el-button @click="handleClick(scope.row)" type="text" size="small">查看</el-button>
                    <el-button type="text" size="small">编辑</el-button>
                    <el-button type="text" size="small">开始</el-button>
                    <el-button type="text" size="small">暂停</el-button>
                    <el-button type="text" size="small">停止</el-button>
                </template>
            </el-table-column>
        </el-table>

        <el-pagination @size-change="handleSizeChange" @current-change="handleCurrentChange"
                       :current-page="currentPage" :page-sizes="[10, 20, 50]" :page-size="10"
                       layout="total, sizes, prev, pager, next, jumper" :total="total">
        </el-pagination>
    </div>
</template>

<script>
    export default {
        name: "Projects",
        methods: {
            handleSizeChange(val) {
                console.log(`每页 ${val} 条`);
            },
            handleCurrentChange(val) {
                console.log(`当前页: ${val}`);
            },
        },
        data() {
            return {
                project_data: [{
                    tag: null,
                    name: '温州市科技局',
                    status: '运行'
                }, {
                    tag: '政府数据',
                    name: '温州市科技局',
                    status: '运行'
                }, {
                    tag: '视频数据',
                    name: 'bilibili',
                    status: '暂停'
                }, {
                    tag: '新闻文章',
                    name: '网易新闻',
                    status: '停止'
                },],
                currentPage: 1,
            }
        },
        computed: {
            total: function () {
                return this.project_data.length
            }
        }
    }
</script>


<style scoped>
    #projects{

    }
</style>
